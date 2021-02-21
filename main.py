# extracting_text.py
import errno
import os
import shutil
from PyPDF2 import PdfFileReader


def get_info(path):
    with open(path, 'rb') as f:
        reader = PdfFileReader(f)
        info = reader.getDocumentInfo()
        number_of_pages = reader.getNumPages()
        page = reader.getPage(0)
        page_content = page.extractText()
        print(page_content)

    my_file = open("tmp.txt", "w+")  # creation d'un fichier temporaire

    name = os.path.basename(path)
    if name is None:
        name = "None"
    print("Nom du PDF")
    print(name, '\n')
    my_file.write("Nom du PDF : " + name + '\n')

    title = info.title
    if title is None:
        title = "None"
    print("Titre du PDF")
    print(title, '\n')
    my_file.write("Titre du PDF : " + title + '\n')

    author = info.author
    if author is None:
        author = "None"
    print("Auteur du PDF")
    print(author, '\n')
    my_file.write("Auteur du PDF : " + author + '\n')

    my_file.write("Contenu : \n " + page_content)

    my_file.close()  # fermeture du fichier

    name = name.removesuffix(".pdf")  # va servir pour créer le .txt ainsi que le sous répertoire
    txt_name = name + ".txt"  # pour renommer le fichier
    os.rename("tmp.txt", txt_name)  # appel systeme pour renommer le fichier pour en faire un txt

    create_dir = name  # répertoire au nom du fichier (sans l'extension)
    droits_acces = 0o755
    try:
        os.makedirs(create_dir, droits_acces)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    shutil.move(txt_name, create_dir)  # deplacer le fichier dans le sous répertoire


if __name__ == '__main__':
    path = input("Tapez le chemin du PDF (exemple '../Corpus_2021/Torres.pdf' : \n")
    get_info(path)
