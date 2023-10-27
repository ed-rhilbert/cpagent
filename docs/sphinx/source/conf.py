# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
from platform import release
import sys
from datetime import date

# sys.path.insert(0, os.path.abspath('../..'))
import rlway_cpagent

# -- Project information -----------------------------------------------------

project = 'rlway-cpagent'
copyright = f"2023-{date.today().year}, EURODECISION"
author = 'EURODECISION'

# The full version, including alpha/beta/rc tags
version = rlway_cpagent.__version__
release = rlway_cpagent.__version__

# -- General configuration ---------------------------------------------------
source_suffix = ['.rst', '.md']

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc", # required extension for automatic doc generation
    'sphinx.ext.viewcode',  # Add a link to the Python source code for classes, functions etc.
    'sphinx.ext.napoleon',  # handle numpy & google style docstrings
    'sphinx.ext.coverage', # find undocumented code
    "m2r2",  # md to rst
    "sphinx_copybutton",
    'sphinx.ext.autosummary', # automatic generation of API Reference
    # "sphinx_automodapi.automodapi",  # can be used to customize documentation by creating separate pages at will :
    #                                 # .. automodapi:: rlway_cpagent.subpackage.module
    #                                 #    :no-inheritance-diagram:
    # "sphinx_automodapi.smart_resolver"
    "sphinx.ext.mathjax",
]

# numpydoc_show_class_members = False
autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "class"  # If "both", adds __init__ doc to class summary
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
add_module_names = True # Include namespaces in signatures
autodoc_member_order = "groupwise" # automatically documented members are sorted by member type
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = "_static/logoed.jpg"
html_favicon = "_static/logoed.jpg"

html_theme_options = {
    "icon_links": [
            {
                "name": "GitLab",
                "url": "https://github.com/chpombet/rlway-cpagent",
                "icon": "fab fa-gitlab",
            },
            {
                "name": "EURODECISION",
                "url": "https://eurodecision.com",
                "icon": "_static/logo_ed_star.png",
                "type": "local"
            },
        ],
}

html_sidebars = {
    "**": ["search-field.html", "sidebar-nav-bs.html", "logo"]
}
