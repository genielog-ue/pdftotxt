# extracting_text.py
import errno
import os
import shutil
from PyPDF2 import PdfFileReader


def get_info(path):
    if path[-1] != '/':
        path += '/'
    if not os.path.exists(path + "txt"):
        os.mkdir(path + "txt")
    else:
        shutil.rmtree(path + "txt")
        os.mkdir(path + "txt")

    directory = [fichiers for fichiers in os.listdir(path) if os.path.isfile(path + fichiers)]
    print(directory)
    for file in directory:
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
        if title is None:
            title = "None"
        print("Titre du PDF")
        print(title, '\n')
        my_file.write("Titre du PDF : " + title + '\n')
        ###
        ## Ecriture information auteur
        author = info.author
        if author is None:
            author = "None"
        print("Auteur du PDF")
        print(author, '\n')
        my_file.write("Auteur du PDF : " + author + '\n')
        ###
        ## Ecriture Contenu fichier PDF
        my_file.write("Contenu : \n " + page_content)
        ###
        my_file.close()  # fermeture du fichier

        name = name.removesuffix(".pdf")  # va servir pour créer le .txt ainsi que le sous répertoire
        txt_name = name + ".txt"  # pour renommer le fichier
        os.rename("tmp.txt", txt_name)  # appel systeme pour renommer le fichier pour en faire un txt
        shutil.move(txt_name, path + "txt")  # deplacer le fichier dans le sous répertoire


if __name__ == '__main__':
    path = input("Tapez le chemin du dossier (exemple '../Corpus_2021' : \n")
    get_info(path)
