#!/bin/bash

python manage.py migrate
newrelic-admin generate-config $NEW_RELIC_LICENSE_KEY newrelic.ini
