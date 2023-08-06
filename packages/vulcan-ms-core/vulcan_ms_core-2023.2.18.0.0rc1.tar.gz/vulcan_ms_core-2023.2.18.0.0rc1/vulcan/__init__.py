"""Vulcan Microservice Core Library"""
import datetime
import hashlib
import os

from pytz import timezone


def generate_datetime_with_timezone():
    format = "{dt.year}.{dt.month}.{dt.day}.{dt.hour}.{dt.minute}"
    return format.format(dt=datetime.datetime.now(timezone("America/Sao_Paulo")))


def generate_version(name: str):
    print("Generating version for: " + name)
    date = generate_datetime_with_timezone()
    if name == "main":
        return date + "rc1"
    elif name.startswith("feature-"):
        return date + ".dev1"
    else:
        return name


def hash_branch_name(branch_name):
    return hashlib.md5(branch_name.encode("utf-8")).hexdigest()


version = os.getenv("VERSION")
__version__ = generate_version(version)
