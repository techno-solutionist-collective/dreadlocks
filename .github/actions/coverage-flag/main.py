from sys import argv, stdout
from os import listdir
from typing import Iterable
from json import dump

prefix = argv[1]
separator = argv[2]
endpoints = argv[3]
suffix = argv[4]
flag = argv[5]


def flags(prefix: str, separator: str, endpoint: str) -> list[str]:
    assert endpoint.startswith(prefix)
    raw_flags = endpoint[len(prefix) :]
    return raw_flags.split(separator)


def files(endpoints: str) -> Iterable[str]:
    for endpoint in listdir(endpoints):
        if flag == "all" or flag in flags(prefix, separator, endpoint):
            yield f"{endpoints}/{endpoint}{suffix}"


dump(sorted(files(endpoints)), stdout)
