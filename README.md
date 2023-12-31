
# Prerequisites

## Python >= 3.10

## Java 17

### Install on Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-17-jdk openjdk-17-jre
```
### Install on Windows

https://www.oracle.com/java/technologies/downloads/#java17

## SSH keys to access github.com

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

# For users

## Installation

```bash
    pip install git+ssh://git@github.com:ed-rhilbert/cpagent.git
```
or

```bash
pip install --upgrade git+ssh://git@github.com:ed-rhilbert/cpagent.git
```

## Getting started

```python3
>>> from rlway.pyosrd import OSRD
>>> from rlway_cpagent.cp_agent import CPAgent
>>> sim = OSRD(use_case='point_switch', dir='point_switch')
>>> regulated = sim.regulate(agent=CPAgent("cp_agent"))
```

## Custom Java binary path

Create a file name `.env` at the root of your projet, containing 
```bash
JAVA="<Your custon Java Path>"
```
On Windows, it is recommanded to use triple double quotes (especially if the path contains spaces), e.g.:
```bash
JAVA="""C:\Program Files\Common Files\Oracle\Java\javapath\java"""
```
# For contributors

```bash
git clone git@github.com:ed-rhilbert/cpagent.git
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```