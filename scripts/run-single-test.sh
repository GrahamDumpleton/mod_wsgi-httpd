#!/bin/bash

# Runs a WSGI hello world application under mod_wsgi-express, using
# the Apache httpd installed by the mod_wsgi-httpd package. Requires
# that mod_wsgi-httpd was installed first and that mod_wsgi was then
# installed into the same Python environment, so that mod_wsgi was
# built against the httpd from mod_wsgi-httpd.

END=$((SECONDS+15))

mod_wsgi-express setup-server tests/hello.wsgi \
    --server-root httpd-test --log-level info

# Guard against mod_wsgi having been built against some other Apache
# installation present on the host.

if ! grep -q 'mod_wsgi_packages/httpd/bin/httpd' httpd-test/apachectl; then
    echo 'Failed: mod_wsgi-express is not using httpd from mod_wsgi-httpd'
    exit 1
fi

trap "httpd-test/apachectl stop" EXIT

touch httpd-test/error_log

tail -f httpd-test/error_log &

httpd-test/apachectl start

while [ ! -f httpd-test/httpd.pid ]; do
    if [ $SECONDS -gt $END ]; then
        echo 'Failed'
        exit 1
    fi

    echo 'Waiting...'
    sleep 1
done

sleep 2

curl --silent --verbose --fail --show-error http://localhost:8000
