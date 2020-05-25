import types
import random
from typing import Callable, Any
from contextlib import contextmanager
from functools import wraps
from dataclasses import dataclass

import numpy as np
import pennylane as qml
import qiskit
from pennylane_qiskit.qiskit_device import QiskitDevice
from qiskit.ignis.mitigation.measurement import complete_meas_cal, CompleteMeasFitter

NUMBER_OF_SHOTS_FOR_QISKIT_ERROR_MITIGATION = 1024


@dataclass
class _SwappedItemsMap:
    """
      Mainly to avoid a unnecessary global, but can be extended if more functionalities would
      need to be swapped out temporarily
    """

    old_generate_samples_global: Callable[..., Any]


def _qiskit_generate_samples_MEM(self: QiskitDevice) -> np.array:
    """
        This function is used to overrite the default QiskitDevice.generate_samples method.
        It adds a simple mechanism to perform measurement error mitigation on the results of
        the computation.
    """
    # branch out depending on the type of backend
    if self.backend_name in self._state_backends:
        # software simulator: need to sample from probabilities
        return super().generate_samples()

    # hardware or hardware simulator

    # ***here we actully perform the measurement error mitigation***
    meas_calibs, state_labels = complete_meas_cal(qr=self._reg, circlabel="mcal")
    mitigation_run_args = self.run_args.copy()
    mitigation_run_args["shots"] = NUMBER_OF_SHOTS_FOR_QISKIT_ERROR_MITIGATION
    meas_job = qiskit.execute(meas_calibs, backend=self.backend, **mitigation_run_args)

    # TODO: Adding a cache here is a free performance boost
    meas_fitter = CompleteMeasFitter(meas_job.result(), state_labels, circlabel="mcal")
    mitigated_results = meas_fitter.filter.apply(self._current_job.result())
    current_job_shots = sum(self._current_job.result().get_counts().values())
    summed_counts = sum(mitigated_results.get_counts().values())
    probs = [value / summed_counts for value in mitigated_results.get_counts().values()]
    samples = np.random.choice(
        np.array(list(mitigated_results.get_counts().keys())),
        current_job_shots,
        p=probs,
        replace=True,
    )

    # reverse qubit order to match PennyLane convention
    return np.vstack([np.array([int(i) for i in s[::-1]]) for s in samples])


def _check_if_generate_samples_is_defined(func: Callable[..., Any]) -> Any:
    """
        Simple decorator to at least partially guard against API changes in the
        PennyLane-Qiskit dependency
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        method = getattr(QiskitDevice, "generate_samples", None)
        if method is None:
            raise Exception("Cannot perform this action - PennyLane-Qiskit API has changed.")
        return func(*args, **kwargs)

    return wrap


@_check_if_generate_samples_is_defined
def globally_enable_qiskit_measurement_error_mitigation() -> None:
    """
        Makes it so that every measurement operation on a Qiskit device from now on
        is measurement-error-mitigated (i.e. we apply the filter from CompleteMeasFitter
        to the result of the computation).
    """
    _SwappedItemsMap.old_generate_samples_global = QiskitDevice.generate_samples
    QiskitDevice.generate_samples = _qiskit_generate_samples_MEM


@_check_if_generate_samples_is_defined
def globally_disable_qiskit_measurement_error_mitigation() -> None:
    """
        Undo the effect of globally_enable_qiskit_measurement_error_mitigation()
    """
    if _SwappedItemsMap.old_generate_samples_global is None:
        raise Exception("The global context has been corrupted! Cannot undo the operation.")
    QiskitDevice.generate_samples = _SwappedItemsMap.old_generate_samples_global


@contextmanager
def qiskit_measurement_error_mitigation() -> None:
    """
        The same as globally_enable_qiskit_measurement_error_mitigation() but in the form
        of a context manager
    """
    old_generate_samples = QiskitDevice.generate_samples
    QiskitDevice.generate_samples = _qiskit_generate_samples_MEM

    try:
        yield
    finally:
        QiskitDevice.generate_samples = old_generate_samples
