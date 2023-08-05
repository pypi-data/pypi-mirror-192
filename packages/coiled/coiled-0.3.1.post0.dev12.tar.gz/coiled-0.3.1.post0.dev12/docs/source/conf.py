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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

from datetime import date

from coiled import AWSOptions, Cluster, FirewallOptions, GCPOptions

# Shenanigans to trick autodoc
Cluster.__module__ = __name__
Cluster.__name__ = "Cluster"

AWSOptions.__module__ = __name__
AWSOptions.__name__ = "AWSOptions"

GCPOptions.__module__ = __name__
GCPOptions.__name__ = "GCPOptions"

FirewallOptions.__module__ = __name__
FirewallOptions.__name__ = "FirewallOptions"

project = "Coiled"
author = "Coiled"
year = date.today().year
copyright = "2020-{}, Coiled Computing Inc".format(year)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_click.ext",
    "sphinx_copybutton",
    "sphinx_panels",
    "sphinx_reredirects",
    "myst_nb",
    "sphinx_tabs.tabs",
]

# these are for myst_nb
myst_enable_extensions = ["colon_fence"]

# don't execute jupyter notebooks on build
nb_execution_mode = "off"

# disable predefined CSS style for sphinx_tabs
# sphinx_tabs_disable_css_loading = True


# Add pages to redirects if they get moved
# Uses the sphinx-reredirects extension
# "<old-docname>": "<new-url>"
redirects = {
    "user_guide/beta.html": "v2.html",
    "user_guide/jupyter": "user_guide/examples/jupyterlab.html",
    "user_guide/example-prefect": "examples/prefect.html",
    "user_guide/example-optuna": "examples/dask-optuna-hpo.html",
    "user_guide/examples/optuna": "examples/dask-optuna-hpo.html",
    "user_guide/backends_aws.html": "aws_configure.html",
    "user_guide/backends_gcp.html": "gcp_configure.html",
    "user_guide/tutorials/set_threads_per_worker": "cluster_creation#set-threads-per-worker.html",
    "user_guide/cluster": "getting_started.html",
}

autosummary_generate = True
autodoc_typehints = "none"

panels_add_bootstrap_css = False

panels_css_variables = {
    "tabs-color-label-active": "rgba(0,120,213,1)",
    "tabs-color-label-inactive": "rgba(0,120,213,0.8)",
    "tabs-color-overline": "rgb(207, 236, 238)",
    "tabs-color-underline": "rgb(0, 120, 213)",
    "tabs-size-label": "1rem",
}

copybutton_prompt_text = "$ "
linkcheck_retries = 3
# TODO: Figure out why linkcheck is breaking on Coiled's Twitter.
# Navigating to this link in a browser works.
linkcheck_ignore = [
    "https://twitter.com/coiledhq",
    "https://docs.github.com",
    "https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#temporary-access-keys",
]

intersphinx_mapping = {
    "distributed": ("https://distributed.dask.org/en/latest/", None),
    "dask_kubernetes": ("https://kubernetes.dask.org/en/latest/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["user_guide/backends_k8s.rst", "user_guide/examples/optuna.rst"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_logo = "_static/Coiled-Logo.svg"

html_theme_options = {
    "icon_links": [
        {"name": "GitHub", "url": "https://github.com/coiled", "icon": "fab fa-github"},
        {
            "name": "Twitter",
            "url": "https://twitter.com/CoiledHQ",
            "icon": "fab fa-twitter",
        },
    ],
    "show_prev_next": True,
    "show_toc_level": 2,
    "external_links": [
        {"name": "Login", "url": "https://cloud.coiled.io/login"},
        {"name": "Sign Up", "url": "https://cloud.coiled.io/signup"},
        {
            "name": "Support",
            "url": "https://docs.coiled.io/user_guide/support.html",
        },
        {"name": "Pricing", "url": "https://coiled.io/pricing"},
        {"name": "coiled.io", "url": "https://coiled.io"},
    ],
    "google_analytics_id": "G-FRTJW3G4X5",
    "navbar_align": "right",
    "footer_items": ["copyright"],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# Setting the baseurl will add the canonical link to the <header> of our pages
html_baseurl = "https://docs.coiled.io/"

# Needed to set language in the html tag
language = "en"

html_css_files = ["custom.css"]
