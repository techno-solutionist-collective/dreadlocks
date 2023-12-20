project = 'dreadlocks'
copyright = '2023, Pid Zwei'
author = 'Pid Zwei'

release = '0.0'
version = '0.0.1'

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_automodapi.automodapi',
    'sphinx_multiversion',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = [
    'std'
]

templates_path = [
    '_templates'
]

html_theme = 'sphinx_rtd_theme'

epub_show_urls = 'footnote'

smv_tag_whitelist = r'^v\d+\.\d+\.\d+$|latest'  # all tags of form v*.*.x and latest
# Whitelist pattern for branches (set to '' to ignore all branches)
smv_branch_whitelist = r'^.*$'
smv_released_pattern = r'^.*$'
smv_latest_version = 'v0.0.1'
smv_remote_whitelist = None
smv_outputdir_format = '{ref.name}'
