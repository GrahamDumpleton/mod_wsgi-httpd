Overview
--------

The ``mod_wsgi-httpd`` package is a companion to
``mod_wsgi-standalone``. It downloads, compiles and installs a
private copy of the Apache HTTP Server inside your Python
environment, which ``mod_wsgi-standalone`` then builds ``mod_wsgi``
against and runs ``mod_wsgi-express`` on top of.

``mod_wsgi-standalone`` is the alternative to a regular
``pip install mod_wsgi`` for hosts that need their own Apache/httpd
install: either because no system Apache is available, or because
using the system Apache is not desirable. Typical cases are managed
hosts where you have no root access to install system packages, and
container base images that ship Python but not Apache or its
development headers.

You normally do not need to install ``mod_wsgi-httpd`` yourself;
``pip install mod_wsgi-standalone`` declares it as a dependency and
``pip`` will pull in a compatible version automatically.

**Note:** If your operating system's Apache and the matching Apache
development packages are available, prefer those over
``mod_wsgi-standalone``. Building ``mod_wsgi-httpd`` compiles
Apache, APR, APR-util and PCRE2 from source, which can take several
minutes; if ``pip install -v mod_wsgi-standalone`` looks like it is
hanging, it is almost certainly still compiling ``mod_wsgi-httpd``.

The version of ``mod_wsgi-httpd`` is the version of the Apache HTTP
Server it installs, followed by a build number. For example, version
``2.4.68.2`` is the second build of this package for Apache 2.4.68.
Each release of ``mod_wsgi-standalone`` requires one exact version of
``mod_wsgi-httpd``, so the Apache version you get is decided by the
``mod_wsgi-standalone`` release you install.

Listing mod_wsgi-httpd as a separate dependency
-----------------------------------------------

Use ``mod_wsgi-standalone`` in a ``requirements.txt`` file, or in the
dependencies of a ``pyproject.toml`` file. Listing ``mod_wsgi-httpd``
and ``mod_wsgi`` as two separate dependencies does not give the same
result, for two reasons:

* ``mod_wsgi`` is compiled against ``mod_wsgi-httpd``, so
  ``mod_wsgi-httpd`` has to be installed before ``mod_wsgi`` is built.
  When both are named in the one ``pip install`` command, or the one
  requirements file, ``pip`` builds ``mod_wsgi`` first.

* Packaging tools build each package in an isolated environment by
  default, and a package installed in the target environment cannot be
  seen from inside it.

The installation succeeds either way, which makes the problem easy to
miss. If the host has some other Apache installation, ``mod_wsgi`` is
built against that and ``mod_wsgi-httpd`` goes unused. Otherwise the
result can be a ``mod_wsgi-express`` which fails when started.

If you do need to list them separately, and you use `uv
<https://docs.astral.sh/uv/>`_, name ``mod_wsgi-httpd`` as an extra
build dependency of ``mod_wsgi`` in ``pyproject.toml``, using the same
version in both places::

    [project]
    dependencies = [
        "mod_wsgi-httpd==2.4.68.2",
        "mod_wsgi",
    ]

    [tool.uv.extra-build-dependencies]
    mod-wsgi = ["mod_wsgi-httpd==2.4.68.2"]

With ``pip`` it takes separate commands, the last with build isolation
disabled, which in turn needs ``setuptools`` to be installed already::

    pip install setuptools
    pip install mod_wsgi-httpd
    pip install --no-build-isolation mod_wsgi

This cannot be expressed in a requirements file, as ``pip`` does not
accept the ``--no-build-isolation`` option there.

To check which Apache ``mod_wsgi-express`` is going to run::

    python -c "from mod_wsgi.express import apxs_config; print(apxs_config.HTTPD)"

The path printed should be inside the ``mod_wsgi_packages/httpd``
directory of your Python environment.

Documentation
-------------

Documentation for ``mod_wsgi``, ``mod_wsgi-standalone`` and
``mod_wsgi-express`` lives at https://www.modwsgi.org/. Pages of
particular relevance to ``mod_wsgi-httpd`` users:

* `The mod_wsgi-standalone Package
  <https://www.modwsgi.org/en/latest/user-guides/mod-wsgi-standalone-package.html>`_
  covers how ``mod_wsgi-httpd``, ``mod_wsgi-standalone`` and
  ``mod_wsgi`` relate, what the host needs in order to compile this
  package, how support for HTTPS depends on the OpenSSL development
  files being present at that time, and how security fixes for Apache
  reach you.
* `Installation from PyPI
  <https://www.modwsgi.org/en/latest/user-guides/installation-from-pypi.html>`_
  covers ``pip install mod_wsgi``, the ``mod_wsgi-express`` command,
  and the companion ``mod_wsgi-standalone`` package.
* `mod_wsgi-express quickstart
  <https://www.modwsgi.org/en/latest/user-guides/mod-wsgi-express-quickstart.html>`_
  covers running ``mod_wsgi-express`` for a WSGI application in
  production or in a container.
