Overview
--------

The ``mod_wsgi-httpd`` package is a companion to ``mod_wsgi``. It
downloads, compiles and installs a private copy of the Apache HTTP
Server inside your Python environment. Once installed, a subsequent
``pip install mod_wsgi`` builds against that private Apache, and the
``mod_wsgi-express`` command shipped by ``mod_wsgi`` also uses it.

This is intended for environments where the system Apache is not
available and you cannot install it yourself; for example, managed
hosts where you have no root access, or container base images that
ship Python but not Apache or its development headers (``apache2-dev``
on Debian-derived distributions, ``httpd-devel`` on RHEL-derived
distributions, and the ``apxs`` build tool that they provide).

**Note:** If your operating system's Apache and the matching Apache
development packages are available, prefer those over
``mod_wsgi-httpd``. Building this package compiles Apache, APR,
APR-util and PCRE from source, which can take several minutes; if
``pip install -v mod_wsgi-httpd`` looks like it is hanging, it is
almost certainly still compiling.

Installation
------------

Install the private Apache build first::

    pip install -v mod_wsgi-httpd

The ``-v`` flag prints build progress so you can confirm it is
working.

Then install ``mod_wsgi`` itself::

    pip install mod_wsgi

The two installs must be run as separate ``pip install`` invocations.
``pip`` resolves ``requirements.txt`` entries as a dependency graph
rather than in textual order, so listing both packages in the same
file usually ends up building ``mod_wsgi`` against the system Apache
(or failing entirely when no system Apache is present).

If you need to install from a ``requirements.txt`` file, use the
``mod_wsgi-standalone`` package instead. It is a wrapper that pulls
``mod_wsgi-httpd`` and ``mod_wsgi`` in the right order::

    pip install mod_wsgi-standalone

Running mod_wsgi-express
------------------------

Once ``mod_wsgi`` is installed, start a server with::

    mod_wsgi-express start-server

The default URL is http://localhost:8000/.

For the full set of command-line options run::

    mod_wsgi-express start-server --help

Documentation
-------------

Documentation for ``mod_wsgi`` and ``mod_wsgi-express`` lives at
https://www.modwsgi.org/. Pages of particular relevance to
``mod_wsgi-httpd`` users:

* `Installation from PyPI
  <https://www.modwsgi.org/en/latest/user-guides/installation-from-pypi.html>`_
  covers ``pip install mod_wsgi``, the ``mod_wsgi-express`` command,
  and the companion ``mod_wsgi-standalone`` package.
* `mod_wsgi-express quickstart
  <https://www.modwsgi.org/en/latest/user-guides/mod-wsgi-express-quickstart.html>`_
  covers running ``mod_wsgi-express`` for a WSGI application in
  production or in a container.
