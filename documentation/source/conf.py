# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import pathlib
import sys

if os.path.exists('/app'):
  sys.path.insert(0, os.path.abspath('/app'))
if os.path.exists('../../mac_maker'):
  sys.path.insert(0, os.path.abspath('../..'))
  sys.path.insert(0, os.path.abspath('../../mac_maker'))

# -- Project information -----------------------------------------------------
project = 'mac_maker'
copyright = '2020, Niall Byrne'
author = 'Niall Byrne'
os.environ['PROJECT_NAME'] = project

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_autopackagesummary',
    'sphinx_click.ext',
    'sphinx-jsonschema',
    'sphinxcontrib.spelling',
    'myst_parser',
]

# sphinx.ext.autosummary
autoclass_content = 'both'

# sphinx_autodoc_typehints
always_document_param_types = True
typehints_fully_qualified = False
typehints_defaults = "comma"
typehints_document_rtype = True

# sphinxcontrib.spelling
spelling_lang = 'en_US'
tokenizer_lang = 'en_US'
spelling_word_list_filename = 'spelling_wordlist.txt'


def detect_tests():
  """Create a list of import paths with tests."""

  test_paths = []
  for root, dirs, _ in os.walk('../../pi_portal'):
    for name in dirs:
      if name == 'tests':
        directory = pathlib.Path(os.path.join(root, name).replace('../../', ''))
        test_paths.append('.'.join(directory.with_suffix('').parts))
  return test_paths


# Exclude tests from sphinx_autopackagesummary here
autosummary_mock_imports = detect_tests()

source_suffix = {
    '.rst': 'restructuredtext',
}

typehints_fully_qualified = False
always_document_param_types = True
typehints_defaults = "comma"
typehints_document_rtype = True

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
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/overrides.css',
]
