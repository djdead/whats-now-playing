# pylint: disable=all

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
import sys

sys.path.insert(0, os.path.abspath('..'))

import nowplaying.version


def get_last_tag():
    cfg = nowplaying.version.get_config()
    root = os.path.realpath(__file__)
    pieces = {}
    # versionfile_source is the relative path from the top of the source
    # tree (where the .git directory might live) to this file. Invert
    # this to find the root from __file__.
    for _ in cfg.versionfile_source.split('/'):
        root = os.path.dirname(root)
        try:
            pieces = nowplaying.version.git_pieces_from_vcs(
                cfg.tag_prefix, root, cfg.verbose)
            if pieces.get('closest-tag'):
                break
        except Exception as error:
            print(f'Tried {root} and failed: {error}')
    if not pieces:
        raise ValueError
    return pieces["closest-tag"]


# -- Project information -----------------------------------------------------

project = 'What\'s Now Playing'
copyright = '2021-2023, Allen Wittenauer'
author = 'Allen Wittenauer'

# The full version, including alpha/beta/rc tags
release = nowplaying.version.get_versions()['version']
# last released version
lasttag = get_last_tag()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages',
    'sphinx.ext.extlinks',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

#make some variables available to RST
#variables_to_export = [
#    "release",
#    "lasttag",
#]

#frozen_locals = dict(locals())
#rst_prolog = '\n'.join(map(lambda x: f".. |{x}| replace:: {frozen_locals[x]}", variables_to_export))
#del frozen_locals

basedownload = 'https://github.com/whatsnowplaying/whats-now-playing/releases/download'

extlinks = {
    'lasttagdownloadlink':
    (f'{basedownload}/{lasttag}/NowPlaying-{lasttag}-%s.zip', '%s')
}
