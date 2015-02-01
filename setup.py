from __future__ import print_function

import os
import shutil
import re
import hashlib

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

from setuptools import setup
from distutils.core import Extension

def download_url(url):
    package = os.path.basename(url)
    if not os.path.isfile(package):
        print('Downloading', url)
        urlretrieve(url, package+'.download')
        os.rename(package+'.download', package)
    return package

ASF_URL = 'http://www.us.apache.org/dist/'

APR_VERSION = '1.5.1'
APR_UTIL_VERSION = '1.5.4'
HTTPD_VERSION = '2.4.12'

APR_URL = ASF_URL + 'apr/apr-%s.tar.gz' % APR_VERSION
APR_UTIL_URL = ASF_URL + 'apr/apr-util-%s.tar.gz' % APR_UTIL_VERSION
HTTPD_URL = ASF_URL + 'httpd/httpd-%s.tar.gz' % HTTPD_VERSION

download_url(APR_URL)
download_url(APR_UTIL_URL)
download_url(HTTPD_URL)

SF_URL = 'http://downloads.sourceforge.net/project/'

PCRE_VERSION = '8.36'

PCRE_URL = SF_URL + 'pcre/pcre/%s/pcre-%s.tar.gz' % (PCRE_VERSION,
        PCRE_VERSION)

download_url(PCRE_URL)

VERSIONS_HASH = ':'.join([APR_VERSION, APR_UTIL_VERSION,
        PCRE_VERSION, HTTPD_VERSION])

if not isinstance(VERSIONS_HASH, bytes):
    VERSIONS_HASH = VERSIONS_HASH.encode('UTF-8')

VERSIONS_HASH = hashlib.md5(VERSIONS_HASH).hexdigest()

VERSION_HASH_FILE = os.path.join('build', VERSIONS_HASH)

if not os.path.isfile(VERSION_HASH_FILE):
    if not os.path.isdir('build'):
        os.mkdir('build')

    shutil.rmtree('build/httpd', ignore_errors=True)

    builddir = os.path.join(os.getcwd(), 'build/httpd')

    shutil.rmtree('src/httpd', ignore_errors=True)

    destdir = os.path.join(os.getcwd(), 'src/httpd')

    res = os.system('rm -rf build/apr-%(version)s && '
            'tar -x -v -C build -f apr-%(version)s.tar.gz && '
            'cd build/apr-%(version)s && '
            './configure --prefix=%(builddir)s && '
            'make && make install' % dict(builddir=builddir,
            version=APR_VERSION))

    if res:
        raise RuntimeError('Failed to build APR.')

    res = os.system('rm -rf build/apr-util-%(version)s && '
            'tar -x -v -C build -f apr-util-%(version)s.tar.gz && '
            'cd build/apr-util-%(version)s && '
            './configure --prefix=%(builddir)s '
            '--with-apr=%(builddir)s/bin/apr-1-config && '
            'make && make install' % dict(builddir=builddir,
            version=APR_UTIL_VERSION))

    if res:
        raise RuntimeError('Failed to build APR-UTIL.')

    res = os.system('rm -rf build/pcre-%(version)s && '
            'tar -x -v -C build -f pcre-%(version)s.tar.gz && '
            'cd build/pcre-%(version)s && '
            './configure --prefix=%(builddir)s && '
            'make && make install' % dict(builddir=builddir,
            version=PCRE_VERSION))

    if res:
        raise RuntimeError('Failed to build PCRE.')

    res = os.system('rm -rf build/httpd-%(version)s && '
            'tar -x -v -C build -f httpd-%(version)s.tar.gz && '
            'cd build/httpd-%(version)s && '
            './configure --prefix=%(builddir)s '
            '--enable-mpms-shared=all --enable-so --enable-rewrite '
            '--with-apr=%(builddir)s/bin/apr-1-config '
            '--with-apr-util=%(builddir)s/bin/apu-1-config '
            '--with-pcre=%(builddir)s/bin/pcre-config && '
            'make && make install' % dict(builddir=builddir,
            version=HTTPD_VERSION))

    if res:
        raise RuntimeError('Failed to build HTTPD.')

    shutil.rmtree('build/httpd/build-1', ignore_errors=True)
    shutil.rmtree('build/httpd/cgi-bin', ignore_errors=True)
    shutil.rmtree('build/httpd/error', ignore_errors=True)
    shutil.rmtree('build/httpd/htdocs', ignore_errors=True)
    shutil.rmtree('build/httpd/icons', ignore_errors=True)
    shutil.rmtree('build/httpd/man', ignore_errors=True)
    shutil.rmtree('build/httpd/manual', ignore_errors=True)
    shutil.rmtree('build/httpd/share', ignore_errors=True)

    with open('build/httpd/build/config_vars.mk') as fpin:
        config_vars = fpin.readlines()

    with open('build/httpd/build/config_vars.mk', 'w') as fpout:
        prefix = os.path.join(os.getcwd(), 'build/httpd')
        for line in config_vars:
            line = re.sub(prefix, '${mod_wsgi_httpd_prefix}', line)
            print(line, end='', file=fpout)

    shutil.move(builddir, destdir)

    open('src/httpd/__init__.py', 'a').close()

    open(VERSION_HASH_FILE, 'a').close()

package_files = []

for root, dirs, files in os.walk('src/httpd', topdown=False):
    for name in files:
        path = os.path.join(root, name).split('/', 1)[1]
        package_files.append(path)
        print('adding ', path)

setup(name = 'mod_wsgi-httpd',
    version = '%s.1' % HTTPD_VERSION,
    description = 'Installer for Apache httpd server.',
    author = 'Graham Dumpleton',
    author_email = 'Graham.Dumpleton@gmail.com',
    maintainer = 'Graham Dumpleton',
    maintainer_email = 'Graham.Dumpleton@gmail.com',
    url = 'http://www.modwsgi.org/',
    #bugtrack_url = 'https://github.com/GrahamDumpleton/mod_wsgi/issues',
    license = 'Apache License, Version 2.0',
    platforms = [],
    download_url = None,
    classifiers= [
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
    ],
    packages = ['mod_wsgi', 'mod_wsgi.httpd', 'mod_wsgi.apxs'],
    package_dir = {'mod_wsgi': 'src'},
    package_data = {'mod_wsgi': package_files},
    ext_modules = [Extension("mod_wsgi.apxs._dummy", ["_module.c"])],
    entry_points = { 'console_scripts':
            ['mod_wsgi-apxs = mod_wsgi.apxs.__main__:main'],},
)
