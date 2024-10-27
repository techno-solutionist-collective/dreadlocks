from sys import argv, stdout
from os import listdir
from typing import Iterable
from json import dump

prefix = argv[1]
separator = argv[2]
endpoints = argv[3]


def flags(prefix: str, separator: str, endpoints: str) -> Iterable[str]:
    for file in listdir(endpoints):
        assert file.startswith(prefix)
        raw_flags = file[len(prefix) :]
        yield from raw_flags.split(separator)


dump(sorted(set(flags(prefix, separator, endpoints))), stdout)
