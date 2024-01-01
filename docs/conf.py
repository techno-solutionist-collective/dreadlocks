import tomllib
import re
from os import getenv
from datetime import datetime
from pathlib import Path

pyproject_path = Path(__file__).parent.parent.joinpath('pyproject.toml')

with open(pyproject_path, 'rb') as fp:
    pyproject = tomllib.load(fp)

now = datetime.now()

project = pyproject['tool']['poetry']['name']

author_re = re.compile(r'^(\w+(?: \w+)*)(?: \(([^)]+)\))?(?: <([^>]+)>)?$')

author = ', '.join(
    map(
        lambda author: author_re.search(author).group(1),
        pyproject['tool']['poetry']['authors']
    )
)
copyright = '{}, {}'.format(now.year, author)

release = pyproject['tool']['poetry']['version']

def _version(release: str, sep: str = '.'):
    return sep.join(release.split(sep)[:2])

version = _version(release)

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

smv_tag_whitelist = r'^(v\d+\.\d+\.\d+(-(alpha|beta|rc)\.\d+)?|latest)$'  # all tags of form v*.*.x and latest
# Whitelist pattern for branches (set to '' to ignore all branches)
smv_branch_whitelist = getenv('BUILD_BRANCHES', r'^.*$')
smv_released_pattern = r'^(refs/tags/(v\d+\.\d+\.\d+|latest))$'
smv_remote_whitelist = getenv('BUILD_REMOTE_BRANCHES')
smv_outputdir_format = '{ref.name}'
