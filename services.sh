#!/bin/bash

/etc/init.d/postgresql start
/etc/init.d/memcached start

./manage.py runserver 0.0.0.0:8000

exec "$@"