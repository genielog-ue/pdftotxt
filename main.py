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


def getAuthor(path, parserDirectory):
    author = ""

    return author


def get_info(path):
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
        ## Appel pdftotext pour convertir les pdf en txt vers le dossier parserDirectory
        os.system("pdftotext " + '"' + path + file + '"' + " " + path + parserDirectory + "/" + '"' + (
                file.removesuffix(".pdf") + ".txt") + '"')
        with open(path + file, 'rb') as f:
            reader = PdfFileReader(f)
            info = reader.getDocumentInfo()
            number_of_pages = reader.getNumPages()
            page = reader.getPage(0)
            page_content = page.extractText()
            print(page_content)
        my_file = open("tmp.txt", "w+")  # creation d'un fichier temporaire

        ## Ecriture nom du fichier
        name = file
        print("Nom du PDF")
        print(name, '\n')
        my_file.write("Nom du PDF : " + name + '\n')
        ###
        ## Ecriture Titre du pdf
        title = info.title
        if title is None or not title:
            title = "None"
        print("Titre du PDF")
        print(title, '\n')
        my_file.write("Titre du PDF : " + title + '\n')
        ###
        ## Ecriture information auteur
        author = info.author
        if author is None or not author:
            author = getAuthor(path,parserDirectory)
        print("Auteur du PDF")
        print(author, '\n')
        my_file.write("Auteur du PDF : " + author + '\n')
        ###
        ## Ecriture Contenu fichier PDF
        content = ""
        with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
            content = parse.read().decode("utf-8")
            regex = re.search('Abstract(.+?)(Introduction|1)', content, flags=re.IGNORECASE | re.DOTALL)
            try:
                if regex:
                    my_file.write("Abstract : " + regex.group(1))
                else:
                    regex = re.search('\n\n(.+?)(Introduction|1)', content, flags=re.IGNORECASE | re.DOTALL)
                    my_file.write("Abstract : " + regex.group(1))
            except AttributeError:
                my_file.write("Abstract : NOT FOUND")
            parse.close()
        ###

        my_file.close()  # fermeture du fichier

        name = name.removesuffix(".pdf")  # va servir pour créer le .txt ainsi que le sous répertoire
        txt_name = name + ".txt"  # pour renommer le fichier
        os.rename("tmp.txt", txt_name)  # appel systeme pour renommer le fichier pour en faire un txt
        shutil.move(txt_name, path + txtDirectory)  # deplacer le fichier dans le sous répertoire


if __name__ == '__main__':
    path = input("Tapez le chemin du dossier (exemple '../Corpus_2021' : \n")
    get_info(path)
