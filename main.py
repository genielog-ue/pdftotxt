# extracting_text.py
import os
import re
import shutil

from PyPDF2 import PdfFileReader


def reinitDirectory(path, parserDirectory, txtDirectory):
    ### Destruction et Creation du repertoire txt
    if not os.path.exists(path + txtDirectory):
        os.mkdir(path + txtDirectory)
    else:
        shutil.rmtree(path + txtDirectory)
        os.mkdir(path + txtDirectory)
    ### Destruction et Creation du repertoire parser
    if not os.path.exists(path + parserDirectory):
        os.mkdir(path + parserDirectory)
    else:
        shutil.rmtree(path + parserDirectory)
        os.mkdir(path + parserDirectory)


def getAuthor(path, file, parserDirectory):
    author = "None"

    return author


def getEmail(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.findall(r'[\w.-]+@[\w.-]+', content)
        parse.close()
        return regex


def getReferences(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.findall(r'(?<=References).*', content, flags=re.IGNORECASE | re.DOTALL)
        parse.close()
        if regex:
            return regex[-1]
        else:
            return "REFERENCES NOT FOUND "


def getTitle(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        parse.close()
        regex = re.search("TODO ", content, flags=re.IGNORECASE | re.DOTALL)
        if regex:
            return regex
        else:
            return "TITLE NOT FOUND "


def writeFile(path, txtDirectory, file, parameter, dictionnaire):
    if parameter == "-t":
        my_file = open(path + txtDirectory + '/' + file.removesuffix(".pdf") + ".txt", "w+")
        for i in dictionnaire:
            my_file.write(i)
            my_file.write(dictionnaire[i] + '\n')
        my_file.close()
    elif parameter == "-x":
        my_file = open(file.removesuffix(".pdf") + ".xml", "w+")
        my_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        my_file.write("<article>\n")
        my_file.write("<preamble>"+dictionnaire["Titre du PDF : "].replace("\n"," ")+"</preamble>")
        my_file.write("<titre>"+dictionnaire["Titre du PDF : "].replace("\n"," ")+"</titre>")
        my_file.write("<auteur>"+dictionnaire["Auteur du PDF : "].replace("\n"," ")+"</titre>")
        my_file.write("<biblio>"+dictionnaire["References : "].replace("\n"," ")+"</biblio>")
        my_file.write("\n</article>")
        my_file.close()


def get_info(path):
    """

    :param path: Chemin absolu ou relatif du dossier de PDF
    param parameter: -t ou -x pour construire le fichier de sortie en .txt ou .xml
    """
    parserDirectory = "parsers"
    txtDirectory = "txt"

    ###
    if path[-1] != '/':
        path += '/'  # Rajoute le / si absent au path afin d'eviter les problemes de chemin
    ### Reinitialisation des sous-repertoires parsers et txt du dossier path
    reinitDirectory(path, parserDirectory, txtDirectory)
    ###
    # Récuperation des fichiers pdfs

    directory = [fichiers for fichiers in os.listdir(path) if
                 os.path.isfile(path + fichiers) and fichiers.endswith(".pdf")]
    print(directory)
    for file in directory:
        dictionnaire = {}
        ## Appel pdftotext pour convertir les pdf en txt vers le dossier parserDirectory
        os.system("pdftotext " + '"' + path + file + '"' + " " + path + parserDirectory + "/" + '"' + (
                file.removesuffix(".pdf") + ".txt") + '"')
        with open(path + file, 'rb') as f:
            reader = PdfFileReader(f)
            info = reader.getDocumentInfo()
            number_of_pages = reader.getNumPages()
            page = reader.getPage(0)
            page_content = page.extractText()
            # print(page_content)

        ## Ecriture nom du fichier
        name = file
        dictionnaire["Nom : "] = name  # Stockage du nom du PDF dans le dictionnaire
        ###

        ## Ecriture Titre du pdf
        title = info.title
        if title is None or not title:
            title = "None"
        dictionnaire["Titre du PDF : "]=title
        ###

        ## Ecriture information auteur
        author = info.author
        if author is None or not author:
            author = getAuthor(path, file, parserDirectory)
        dictionnaire["Auteur du PDF : "] = author
        ###

        ## Ecriture emails
        for i in getEmail(path, file, parserDirectory):
            ite = 1
            dictionnaire["Email " + str(ite) + " : "] = i
        ###
        ## Ecriture Contenu fichier PDF
        content = ""
        with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
            content = parse.read().decode("utf-8")
            regex = re.search('Abstract(.+?)(Introduction|1)', content, flags=re.IGNORECASE | re.DOTALL)
            try:
                if not regex:
                    regex = re.search('\n\n(.+?)(Introduction|1)', content, flags=re.IGNORECASE | re.DOTALL)
                dictionnaire["Abstract"] = regex.group(1)
            except AttributeError:
                dictionnaire["Abstract"] = "Abstract : NOT FOUND"
            parse.close()
        ###
        # Ecriture references
        dictionnaire["References : "] = getReferences(path, file, parserDirectory)
        writeFile(path, txtDirectory, file, "-t", dictionnaire)


if __name__ == '__main__':
    path = input("Tapez le chemin du dossier (exemple '../Corpus_2021' : \n")
    get_info(path)
