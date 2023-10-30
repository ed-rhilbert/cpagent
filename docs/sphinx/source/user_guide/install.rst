Installation
============

Prerequisites
-------------

Python >= 3.10
""""""""""""""

Java 17
"""""""

Install on Ubuntu
`````````````````

.. code:: bash

    sudo apt update && sudo apt upgrade -y
    sudo apt install openjdk-17-jdk openjdk-17-jre

Install on Windows
``````````````````

https://www.oracle.com/java/technologies/downloads/#java17

SSH keys to access github.com
"""""""""""""""""""""""""""""

`Add a new ssh key to your github account <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account>`_

Minizinc >= 2.9.6
"""""""""""""""""

For Windows
````````````

You can download the installer `here <https://www.minizinc.org/>`_.
Then ensure that the **Minizinc** executable is located in a folder in the **$PATH** environmental variable.

For Linux
``````````

.. code:: bash

    snap install minizinc --classic


Package installation
--------------------

For Users
"""""""""

.. code:: bash

    pip install git+ssh://git@github.com:ed-rhilbert/cpagent.git

or

.. code:: bash

    pip install --upgrade git+ssh://git@github.com:ed-rhilbert/cpagent.git


For Contributors
""""""""""""""""

.. code:: bash

    git clone git@github.com:ed-rhilbert/cpagent.git
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt