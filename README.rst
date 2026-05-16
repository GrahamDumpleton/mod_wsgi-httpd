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
Apache, APR, APR-util and PCRE from source, which can take several
minutes; if ``pip install -v mod_wsgi-standalone`` looks like it is
hanging, it is almost certainly still compiling ``mod_wsgi-httpd``.

Documentation
-------------

Documentation for ``mod_wsgi``, ``mod_wsgi-standalone`` and
``mod_wsgi-express`` lives at https://www.modwsgi.org/. Pages of
particular relevance to ``mod_wsgi-httpd`` users:

* `Installation from PyPI
  <https://www.modwsgi.org/en/latest/user-guides/installation-from-pypi.html>`_
  covers ``pip install mod_wsgi``, the ``mod_wsgi-express`` command,
  and the companion ``mod_wsgi-standalone`` package.
* `mod_wsgi-express quickstart
  <https://www.modwsgi.org/en/latest/user-guides/mod-wsgi-express-quickstart.html>`_
  covers running ``mod_wsgi-express`` for a WSGI application in
  production or in a container.
