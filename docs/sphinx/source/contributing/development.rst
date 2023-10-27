Development
===========

How to contribute to developments ?

Clone the project
-----------------

.. code-block:: bash

   git@edgitlab.eurodecision.com:/rlway-cpagent.git

Virtual environment
-------------------

Create a virtual environment

.. code-block:: bash

   python3 -m venv venv

Activate the created virtual environment

.. code-block:: bash

   . venv/bin/activate

On windows

.. code-block:: bash

   source venv/scripts/activate``

Install dependencies
--------------------

The list of the dependencies is provided in the requirements.txt file.
These dependencies can be easily installed using pip :

.. code-block:: bash

   pip install -r requirements.txt

Install rlway_cpagent

.. code-block:: bash

   pip install -e .

Unit tests
----------

You can run the unit tests using the command:

.. code-block:: bash

   pytest
