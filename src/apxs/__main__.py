from __future__ import print_function

import os
import re
import sys

from ..httpd import __file__ as PACKAGES_ROOTDIR

PACKAGES_ROOTDIR = os.path.dirname(PACKAGES_ROOTDIR)
CONFIG_FILE = os.path.join(PACKAGES_ROOTDIR, 'build/config_vars.mk')

CONFIG = {}

with open(CONFIG_FILE) as fp:
    for line in fp.readlines():
        name, value = line.split('=', 1)
        name = name.strip()
        value = value.strip()
        CONFIG[name] = value

_varprog = re.compile(r'\$(\w+|(?:\{[^}]*\}|\([^)]*\)))')

def expand_vars(value):
    if '$' not in value:
        return value

    i = 0
    while True:
        m = _varprog.search(value, i)
        if not m:
            break
        i, j = m.span(0)
        name = m.group(1)
        if name.startswith('{') and name.endswith('}'):
            name = name[1:-1]
        elif name.startswith('(') and name.endswith(')'):
            name = name[1:-1]
        if name in CONFIG:
            tail = value[j:]
            value = value[:i] + CONFIG.get(name, '')
            i = len(value)
            value += tail
        else:
            i = j

    return value

def get_vars(name):
    value = CONFIG.get(name, '')
    sub_value = expand_vars(value)
    while value != sub_value:
        value = sub_value
        sub_value = expand_vars(value)
    return sub_value.replace('/mod_wsgi.httpd', PACKAGES_ROOTDIR)

CONFIG['mod_wsgi_httpd_prefix'] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'httpd')

CONFIG['PREFIX'] = get_vars('prefix')
CONFIG['TARGET'] = get_vars('target')
CONFIG['SYSCONFDIR'] = get_vars('sysconfdir')
CONFIG['INCLUDEDIR'] = get_vars('includedir')
CONFIG['LIBEXECDIR'] = get_vars('libexecdir')
CONFIG['BINDIR'] = get_vars('bindir')
CONFIG['SBINDIR'] = get_vars('sbindir')
CONFIG['PROGNAME'] = get_vars('progname')

def main():
    if len(sys.argv) <= 1 or sys.argv[1] != '-q':
        print('Usage: mod_wsgi-apxs -q <query> ...')

    else:
        result = []
        for name in sys.argv[2:]:
            result.append(get_vars(name))
        print(';;'.join(result))
