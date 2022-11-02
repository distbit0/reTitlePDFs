import utils
from utils import getConfig
import os
import glob
import shutil


def removeIllegalChars(pdfTitle):
    illegalChars = getConfig()["illegalFileNameChars"]
    for char in illegalChars:
        pdfTitle = pdfTitle.replace(char, "")

    return pdfTitle


def getPDFTitle(pdfPath):
    pdfTitle = ""
    originalFileName = pdfPath.split("/")[-1]
    pdfTitle = os.popen('pdftitle -p "' + pdfPath + '"').read()
    if not pdfTitle:
        pdfTitle = originalFileName
    else:
        pdfTitle = pdfTitle.strip()
        pdfTitle += ".pdf"

    pdfTitle = removeIllegalChars(pdfTitle)
    return pdfTitle


def reTitlePDF(pdfPath):
    pdfTitle = getPDFTitle(pdfPath)
    newPath = "/".join(pdfPath.split("/")[:-1]) + "/" + pdfTitle
    os.rename(pdfPath, newPath)
    return


def getDocsInFolder(folderPath, formats=["pdf"]):
    docPaths = []
    for filePath in glob.glob(folderPath + "/*", recursive=True):
        isDoc = filePath.lower()[-3:] in formats
        if isDoc:
            docPaths.append(filePath)

    return docPaths


def retitlePDFsInFolder(folderPath):
    pdfPaths = getDocsInFolder(folderPath, formats=["pdf"])
    for pdfPath in pdfPaths:
        reTitlePDF(pdfPath)


def retitleAllPDFs():
    PDFFolders = getConfig()["PDFFolders"]
    for folderPath in PDFFolders:
        retitlePDFsInFolder(folderPath)

    return


def moveDocsToTargetFolder():
    docPaths = []
    PDFFolders = getConfig()["PDFFolders"]
    docFormatsToMove = getConfig()["docFormatsToMove"]
    targetFolder = getConfig()["targetFolder"]
    for folderPath in PDFFolders:
        docPaths += getDocsInFolder(folderPath, formats=docFormatsToMove)

    for docPath in docPaths:
        docName = docPath.split("/")[-1]
        shutil.move(docPath, targetFolder + "/" + docName)


if __name__ == "__main__":
    retitleAllPDFs()
    moveDocsToTargetFolder()
