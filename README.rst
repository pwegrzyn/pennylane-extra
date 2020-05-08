PennyLane Extra
#########################

The PennyLane Extra plugin adds some new features to PennyLane.

`PennyLane <https://pennylane.readthedocs.io>`_ is a machine learning library for optimization
and automatic differentiation of hybrid quantum-classical computations.


Features
========

* Measurement error mitigation on Qiskit devices


Installation
============

PennyLane Extra requires both PennyLane and Qiskit. It can be installed via ``pip``:

.. code-block:: bash

    $ python -m pip install .

Please refer to the `plugin documentation <https://pennylane-extra.readthedocs.io/>`_ as
well as to the `PennyLane documentation <https://pennylane.readthedocs.io/>`_ for further reference.

Getting started
===============

Once PennyLane Extra is installed, you can start using it's featrues.

.. code-block:: python

    import pennylane as qml
    import pennylane_extra

    @qml.qnode(dev)
    def circuit(params):
        qml.RX(params[0], wires=0)
        qml.RY(params[1], wires=0)
        return qml.expval(qml.PauliZ(0))

    with.pennylane_extra.qiskit_measurement_error_mitigation():
        print(circuit(np.array([0, 0]))

For more details, see the
`plugin usage guide <https://pennylane-extra.readthedocs.io/en/latest/usage.html>`_ and refer
to the PennyLane documentation.


Contributing
============

We welcome contributions - simply fork the PennyLane Extra repository, and then make a
`pull request <https://help.github.com/articles/about-pull-requests/>`_ containing your contribution.
All contributers to PennyLane-SF will be listed as authors on the releases.

We also encourage bug reports, suggestions for new features and enhancements, and even links to cool
projects or applications built on PennyLane and Target Framework.


Authors
=======

The plugin is created by G. Frejek and P. Wegrzyn. The original excellent PennyLane framework was 
started at Xanadu Quantum Technologies Inc.

    Ville Bergholm, Josh Izaac, Maria Schuld, Christian Gogolin, and Nathan Killoran.
    *PennyLane: Automatic differentiation of hybrid quantum-classical computations.* 2018.
    `arXiv:1811.04968 <https://arxiv.org/abs/1811.04968>`_

    Maria Schuld, Ville Bergholm, Christian Gogolin, Josh Izaac, and Nathan Killoran.
    *Evaluating analytic gradients on quantum hardware.* 2018.
    `Phys. Rev. A 99, 032331 <https://journals.aps.org/pra/abstract/10.1103/PhysRevA.99.032331>`_


Support
=======

- **Source Code:** https://github.com/pwegrzyn/pennylane-extra
- **Issue Tracker:** https://github.com/pwegrzyn/pennylane-extra/issues

If you are having issues, please let us know by posting the issue on our GitHub issue tracker.


License
=======

PennyLane Extra is **free** and **open source**, released under the Apache License, Version 2.0.