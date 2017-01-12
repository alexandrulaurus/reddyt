#!/bin/sh

set -e
db=$1
shift
cmd=$@

PORT=27017

until nc -v -z $db $PORT; do
    >&2 echo "Service not yet started. Waiting..."
    sleep 5
done

>&2 echo "Service started."
exec $cmd
