#!/bin/bash

python manage.py migrate
newrelic-admin generate-config $NEWRELIC_LICENSE_KEY newrelic.ini
