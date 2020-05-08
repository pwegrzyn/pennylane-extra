import unittest

import pennylane_extra
from pennylane_qiskit.qiskit_device import QiskitDevice


class TestInitializer(unittest.TestCase):

    def test_globally_enable_qiskit_measurement_error_mitigation(self):
        # given
        current_method = QiskitDevice.generate_samples

        # when
        pennylane_extra.globally_enable_qiskit_measurement_error_mitigation()

        # then
        self.assertNotEqual(current_method, QiskitDevice.generate_samples)

        pennylane_extra.globally_disable_qiskit_measurement_error_mitigation()
        self.assertEqual(current_method, QiskitDevice.generate_samples)


    def test_qiskit_measurement_error_mitigation(self):
        # given
        current_method = QiskitDevice.generate_samples

        # when/then
        with pennylane_extra.qiskit_measurement_error_mitigation():
            self.assertNotEqual(current_method, QiskitDevice.generate_samples)
        
        self.assertEqual(current_method, QiskitDevice.generate_samples)
