Installation
============

.. warning::
    To install rlway_cpagent, you have to be connected to EURODECISION's VPN


Pip configuration
-----------------

If not already done for your account, type these two commands in the terminal:

.. code:: bash
    
    pip config set global.trusted-host "pypi.org packages.fr.eurodecision.com"
    pip config set global.extra-index-url https://packages.fr.eurodecision.com/nexus/repository/pypi-ed/simple

This will write the required informations in the pip configuration file ```~/.config/pip/pip.conf``

.. note::
    
    This has to be done only once for any account on a given machine.

Package Installation
--------------------

Once connected to the VPN, you just have to type:

.. code:: bash

    pip install rlway_cpagent

You can use the classical pip options (version, upgrade ...) or indicate the package in a `requirements.txt` file.