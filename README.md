
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
pip install git+ssh://git@github.com/ed-rhilbert/cpagent.git
```
or

```bash
pip install --upgrade git+ssh://git@github.com/ed-rhilbert/cpagent.git
```

## Getting started

```python3
>>> from pyosrd.osrd import OSRD
>>> from cpagent.cp_agent import CpAgent
>>> sim = OSRD(use_case='station_capacity2', dir='tmp')
>>> sim.add_delay('train0', time_threshold=150, delay=800.)
>>> regulated = sim.regulate(agent=CpAgent("ortools_agent"))
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
cd cpagent
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
