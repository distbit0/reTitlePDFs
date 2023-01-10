from os import path
import json
from pathlib import Path
import requests
import re


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


def get_id_type(paper_id):
    # Check if the given string is a valid arXiv ID
    if re.match(r"^\d+\.\d+$", paper_id):
        return "arxiv"

    # Check if the given string is a valid DOI
    if paper_id.startswith("10."):
        return "doi"

    # If the string is neither an arXiv ID nor a DOI, return False
    return False


def getDOITitle(doi):

    # Make a request to the CrossRef API to get the metadata for the paper
    headers = {"Accept": "application/json"}
    res = requests.get(f"https://api.crossref.org/v1/works/{doi}", headers=headers)

    # Check if the request was successful
    if res.status_code != 200:
        return "Error: Could not retrieve paper information"

    # Extract the title from the response
    data = res.json()
    title = data["message"]["title"][0]
    return title


def getArxivTitle(arxiv_id):
    # Make a request to the arXiv API to get the metadata for the paper
    print(arxiv_id)
    res = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")

    # Check if the request was successful
    if res.status_code != 200:
        return "Error: Could not retrieve paper information"

    # Extract the title from the response
    data = res.text.replace("\n", "").replace("\t", "")
    # print(data)
    start = data.index("</published>    <title>") + len("</published>    <title>")
    end = data.index("</title>    <summary>")
    # print(start, end)
    title = data[start:end]
    return title


# print(getArxivTitle("2212.14024"))
