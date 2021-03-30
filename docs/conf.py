# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)


# -- Project information -----------------------------------------------------

project = "pymetager"
copyright = "2021, BuildNN Team"
author = "BuildNN Team"

# The full version, including alpha/beta/rc tags
release = "0.0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_click.ext",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    'myst_parser',
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# ---------------

html_theme = "sphinx_book_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"

html_theme_options = {
    "repository_url": "https://github.com/buildnn/pymetager",
    "use_issues_button": True,
    "use_repository_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "./docs",
    "home_page_in_toc": True,
    "extra_navbar": """
    <div style="height: 100%; vertical-align: bottom; margin: auto;">
    <p>---</p>
    <a href="https://www.buildnn.com">
    <div style="background-image: url(\
        'https://www.buildnn.com/assets/img/SVG/full_logo.svg'); \
        width: 100%; height: 100px; background-size: 200px 50px; \
        background-position: center bottom; background-repeat: no-repeat"></div>
    <p>about BuildNN</p>
    </a>
    </div>
    """,
}