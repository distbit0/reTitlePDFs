import utils
from utils import getConfig
import os
import glob


def getPDFTitle(pdfPath):
    pdfTitle = ""
    originalFileName = pdfPath.split("/")[-1]
    pdfTitle = os.popen('pdftitle -p "' + pdfPath + '"').read()
    if not pdfTitle:
        pdfTitle = originalFileName
    else:
        pdfTitle = pdfTitle.strip()
        pdfTitle += ".pdf"
    return pdfTitle


def reTitlePDF(pdfPath):
    pdfTitle = getPDFTitle(pdfPath)
    newPath = "/".join(pdfPath.split("/")[:-1]) + "/" + pdfTitle
    os.rename(pdfPath, newPath)
    return


def retitlePDFsInFolder(folderPath):
    for pdfPath in glob.glob(folderPath + "**/*", recursive=True):
        isPdf = pdfPath.lower()[-4:] == ".pdf"
        if isPdf:
            reTitlePDF(pdfPath)


def retitleAllPDFs():
    PDFFolders = getConfig()["PDFFolders"]
    for folderPath in PDFFolders:
        retitlePDFsInFolder(folderPath)

    return


if __name__ == "__main__":
    retitleAllPDFs()
