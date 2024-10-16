import setuptools
import re

# c.f. https://packaging.python.org/tutorials/packaging-projects/

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSIONFILE = "src/cpagent/__version__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    version_str = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name="cpagent",
    version=version_str,
    author="Charles Pombet",
    author_email="charles.pombet@eurodecision.com",
    description="Regulation agent using constraint programming",
    long_description=long_description,
    long_description_content_type="text/x-md",
    url="https://github.com/ed-rhilbert/cpagent",
    project_urls={
        "Documentation":
        "https://github.com/ed-rhilbert/cpagent/blob/main/README.md",
        "Source Code":
        "https://github.com/ed-rhilbert/cpagent",
        "Bug Tracker":
        "https://github.com/ed-rhilbert/cpagent/-/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"": ['models/*.mzn']},

    python_requires=">=3.10",
    setup_requires=["wheel"],
    install_requires=[
        'ortools',
        'pyosrd @ git+ssh://git@github.com/y-plus/pyosrd.git',
        'importlib-resources'
        ],
)
