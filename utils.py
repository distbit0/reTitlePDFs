from os import path
import json
from pathlib import Path


def mkdirAndParents(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def getAbsPath(relPath):
    basepath = path.dirname(__file__)
    fullPath = path.abspath(path.join(basepath, relPath))

    return fullPath


def getConfig():
    configFileName = getAbsPath("config.json")
    with open(configFileName) as config:
        config = json.loads(config.read())

    return config
