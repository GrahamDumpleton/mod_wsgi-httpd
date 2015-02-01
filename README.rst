================
MOD_WSGI (HTTPD)
================

The mod_wsgi-httpd package is a companion package for mod_wsgi. It will
compile and install a copy of the Apache httpd server into your Python
installation. If this is done, when the mod_wsgi package is subsequently
installed, it will be compiled against the Apache httpd server installed by
this package. When mod_wsgi-express from the mod_wsgi package is then run,
it will also use the same Apache httpd server.

This package therefore allows you to side step the fact that most Linux
distributions and MacOS X ship out of date versions of the Apache httpd
server, allowing you to use the very latest version. It also allows you to
install mod_wsgi-express where you don't control your operating system and
so don't have root access, and the Apache httpd server is not installed, or
its companion 'dev' packages are not installed, which are a prerequsite for
being able to build mod_wsgi from source code.

Installation
------------

To install the Apache httpd server::

    pip install mod_wsgi-httpd

To install the mod_wsgi package and mod_wsgi-express::

    pip install mod_wsgi

To run mod_wsgi-express::

    mod_wsgi-express start-server

You can then access the server at::

    http://localhost:8000/

For more help on mod_wsgi-express see the documentation for the mod_wsgi
package and/or run::

    mod_wsgi-express start-server --help
