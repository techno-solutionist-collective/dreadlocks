#!/usr/bin/env sh

if [ "$#" -eq 0 ] ; then
	printf '%s\n' 'You need to specify a tox unit to run, e.g.:' >&2
	printf '%s\n' './s type-check-watch' >&2
	exit 1
fi

unit="$1"
shift

if [ "$#" -eq 0 ] ; then
	poetry run tox -e "${unit}"
else
	poetry run tox -e "${unit}" -- -- "$@"
fi
