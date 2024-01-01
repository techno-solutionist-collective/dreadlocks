import tomllib
import re
from os import getenv
from datetime import datetime
from pathlib import Path
from subprocess import Popen, PIPE

branch_lines = Popen(['git', 'branch'], stdout=PIPE).stdout

assert branch_lines is not None

checked_out_line = next(
    filter(
        lambda line: line.startswith('* '),
        map(lambda line: line.decode(), branch_lines)
    )
)

checked_out = checked_out_line[2:-1]

detached_head_re = re.compile(r'^\(HEAD detached at (.*)\)$')

if (m := detached_head_re.search(checked_out)) is not None:
    version = m.group(1)
else:
    version = checked_out

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

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(vars())
