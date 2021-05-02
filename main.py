# extracting_text.py
import os
import re
import shutil

from PyPDF2 import PdfFileReader


def reinitDirectory(path, parserDirectory, fileDirectory):
    """
    Détruit et recrée les dossiers indiqués par parserDirectory et txtDirectory ou xmlDirectory
    :param path: pathfile du dossier traité
    :param parserDirectory: pathfile relatif au path du dossier des fichiers parsés par pdf2txt
    :param fileDirectory: pathfile relatif au path du dossier des fichiers de sortie
    :return: None
    """
    ### Destruction et Creation du repertoire txt
    if not os.path.exists(path + fileDirectory):
        os.mkdir(path + fileDirectory)
    else:
        shutil.rmtree(path + fileDirectory)
        os.mkdir(path + fileDirectory)
    ### Destruction et Creation du repertoire parser
    if not os.path.exists(path + parserDirectory):
        os.mkdir(path + parserDirectory)
    else:
        shutil.rmtree(path + parserDirectory)
        os.mkdir(path + parserDirectory)


def getAuthor(path, file, parserDirectory):
    """
    TODO A COMPLETER
    Récupère les auteurs d'un PDF
    :param path: pathfile du dossier traité
    :param file: fichier en cours de traitement par get_info()
    :param parserDirectory: pathfile relatif au path du dossier des fichiers parsés par pdf2txt
    :return: Tableau contenant les auteurs
    """
    author = "None"

    return author


def getEmail(path, file, parserDirectory):
    """
    Récupère tout les emails trouvés dans le fichier parsé
    :param path: pathfile du dossier traité
    :param file: fichier en cours de traitement par get_info()
    :param parserDirectory: pathfile relatif au path du dossier des fichiers parsés par pdf2txt
    :return: Tableau contenant tout les emails trouvés dans le pdf
    """
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.findall(r'[\w.-]+@[\w.-]+', content)
        parse.close()
        if regex:
            return regex
        else:
            return ["EMAIL NOT FOUND"]


def getReferences(path, file, parserDirectory):
    """
    Méthode pour récupérer les références du PDF
    :param path: pathfile du dossier traité
    :param file: fichier en cours de traitement par get_info()
    :param parserDirectory: pathfile relatif au path du dossier des fichiers parsés par pdf2txt
    :return: String contenant la Reference
    """
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.findall(r'(?<=References).*', content, flags=re.IGNORECASE | re.DOTALL)
        parse.close()
        if regex:
            return regex[-1]
        else:
            return "REFERENCES NOT FOUND "


def getTitle(path, file, parserDirectory):
    """
    Méthode pour récupérer le titre du PDF
    :param path: pathfile du dossier traité
    :param file: fichier en cours de traitement par get_info()
    :param parserDirectory: pathfile relatif au path du dossier des fichiers parsés par pdf2txt
    :return: Titre du PDF
    """
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        title = parse.readline() + parse.readline();
        if title:
            return str(title)
        else:
            return "TITLE NOT FOUND"


def getAffiliation(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        parse.close()
        ###TODO AFFILIATION


def getIntroduction(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.findall(r'(?<=Introduction).*', content, flags=re.IGNORECASE | re.DOTALL)
        parse.close()
        if regex:
            return regex[0]
        else:
            return "INTRODUCTION NOT FOUND"


def getConclusion(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.search(r'(^.{0,15}(?<=Conclusion).{0,30}$)(.*?)((?=^.{0,30}[^\.\:]$)).*', content,
                          flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if regex:
            parse.close()
            return regex.group(0)
        else:
            regex = re.search(r'(^.{0,15}(?<=Results).{0,30}$)(.*?)((?=^.{0,30}[^\.\:]$)).*', content,
                              flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
            parse.close()
            if regex:
                return regex.group(0)
        return "CONCLUSION NOT FOUND"


def getDiscussion(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.search(r"((^.{0,15}(?<=Discussion).{0,30}$))(.*?)((?=^.{0,30}[^\.\:]$))", content,
                          flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
        parse.close()
        if regex:
            return regex.group(0)
        else:
            return "DISCUSSION NOT FOUND"


def getCorps(path, file, parserDirectory):
    with open(path + parserDirectory + '/' + (file.removesuffix(".pdf") + ".txt"), 'rb') as parse:
        content = parse.read().decode("utf-8")
        regex = re.search(r"((?<=^II)|(?<=^2 [A-Z]))(.*)((?=([0-9]|).Conclusion.+$)|(?=[0-9].Results.+$))", content,
                          flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
        parse.close()
        if regex:
            return regex.group(0)
        else:
            return "CORPS NOT FOUND"


def writeFile(path, fileDirectory, file, parameter, dictionnaire):
    """
     Ecrit le fichier de sortie en .txt ou .xml selon la variable parameter
     :param path: pathfile du dossier traité
     :param fileDirectory: pathfile relatif au path du dossier des sorties
     :param file: nom du fichier
     :param parameter: arguments -> -t || -x
     :param dictionnaire: dictionnaire contenant les parties recherchées du PDF
     :return: None
     """
    if parameter == "-t":
        my_file = open(path + fileDirectory + '/' + file.removesuffix(".pdf") + ".txt", "w+")
        for i in dictionnaire:
            my_file.write(i)
            my_file.write(dictionnaire[i] + '\n')
        my_file.close()
    elif parameter == "-x":
        find = True
        my_file = open(path + fileDirectory + '/' + file.removesuffix(".pdf") + ".xml", "w+")
        my_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        my_file.write("<article>\n")
        my_file.write("<preamble>" + dictionnaire["Nom du PDF : "].replace("\n", " ") + "</preamble>\n")
        my_file.write("<titre>" + dictionnaire["Titre du PDF : "].replace("\n", " ") + "</titre>\n")
        my_file.write("<auteurs>" + dictionnaire["Auteur du PDF : "].replace("\n", " ") + "</auteurs>\n")
        ite = 1
        while find == True:
            if "Email " + str(ite) + " : " in dictionnaire:
                my_file.write("<email>" + dictionnaire["Email " + str(ite) + " : "].replace("\n", " ") + "</email>\n")
                ite = ite + 1
            else:
                find = False
        # my_file.write("<affiliation>" + dictionnaire[""].replace("\n", " ") + "</affiliation>")
        my_file.write("<abstract>" + dictionnaire["Abstract"].replace("\n", " ") + "</abstract>\n")
        my_file.write("<introduction>" + dictionnaire["Introduction:"].replace("\n", " ") + "</introduction>\n")
        my_file.write("<corps>" + dictionnaire["Corps :"].replace("\n", " ") + "</corps>\n")
        my_file.write("<conclusion>" + dictionnaire["Conclusion:"].replace("\n", " ") + "</conclusion>\n")
        my_file.write("<discussion>" + dictionnaire["Discussion :"].replace("\n", " ") + "</discussion>")
        my_file.write("<biblio>" + dictionnaire["References : "].replace("\n", " ") + "</biblio>\n")
        my_file.write("\n</article>")
        my_file.close()


def get_info(path, directory):
    """
    Méthode principale pour récupérer toutes les informations présentes dans un fichier PDF
    :param path: Chemin absolu ou relatif du dossier de PDF
    param parameter: -t ou -x pour construire le fichier de sortie en .txt ou .xml
    """
    parserDirectory = "parsers"
    outputDirectory = "ParserOutput"

    ###
    if path[-1] != '/':
        path += '/'  # Rajoute le / si absent au path afin d'eviter les problemes de chemin

    # choix du type de conversion
    parameters = str(input("Choix du type de conversion : (-t pour .txt ou -x pour .xml) \n"))
    reinitDirectory(path, parserDirectory, outputDirectory)

    ###
    # Récuperation des fichiers pdfs
    for file in directory:
        dictionnaire = {}
        ## Appel pdftotext pour convertir les pdf en txt vers le dossier parserDirectory
        os.system("pdftotext " + '"' + path + file + '"' + ' ' + '"' + path + parserDirectory + "/" + (
                file.removesuffix(".pdf") + ".txt") + '"' + " -raw -nopgbrk")
        with open(path + file, 'rb') as f:
            reader = PdfFileReader(f)
            info = reader.getDocumentInfo()
            number_of_pages = reader.getNumPages()
            page = reader.getPage(0)
            page_content = page.extractText()
            # print(page_content)

        ## Ecriture nom du fichier
        name = file
        dictionnaire["Nom du PDF : "] = name  # Stockage du nom du PDF dans le dictionnaire
        ###

        ## Ecriture Titre du pdf
        title = info.title
        if title is None or not title:
            title = getTitle(path, file, parserDirectory)
        dictionnaire["Titre du PDF : "] = title
        ###

        ## Ecriture information auteur
        author = info.author
        if author is None or not author:
            author = getAuthor(path, file, parserDirectory)
        dictionnaire["Auteur du PDF : "] = author
        ###

        ## Ecriture emails
        ite = 1
        for i in getEmail(path, file, parserDirectory):
            dictionnaire["Email " + str(ite) + " : "] = i
            ite = ite + 1
        ###
        ##Recherche introduction
        introduction = " " + getIntroduction(path, file, parserDirectory)
        if introduction:
            dictionnaire["Introduction:"] = introduction
        ## Recherche conclusion
        conclusion = " " + getConclusion(path, file, parserDirectory)
        if conclusion:
            dictionnaire["Conclusion:"] = conclusion
        ##Recherche corps
        corps = " " + getCorps(path, file, parserDirectory)
        if corps:
            dictionnaire["Corps :"] = corps
        ## Recherche Discussion
        discussion = " " + getDiscussion(path, file, parserDirectory)
        if discussion:
            dictionnaire["Discussion :"] = discussion
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
        # Ecriture du fichier
        writeFile(path, outputDirectory, file, parameters, dictionnaire)


def getPdfs(path):
    """
    Récupère tout les PDF présents dans le dossier indiqué
    :param path: pathfile du dossier traité
    :return: dictionnaire (clé : int(id),pathfile du PDF)
    """
    if path[-1] != '/':
        path += '/'  # Rajoute le / si absent au path afin d'eviter les problemes de chemin
    directory = [fichiers for fichiers in os.listdir(path) if
                 os.path.isfile(path + fichiers) and fichiers.endswith(".pdf")]
    dictionary = {}
    counter = 1
    for pdf in directory:
        dictionary[counter] = pdf
        counter += 1
    return dictionary


def showPdfs(dictionary):
    """
    Print tout les PDF et les clés du dictionnaire des PDF trouvés dans le dossier traité
    :param dictionary: dictionnaire de tout les PDF présents dans le dossier traité
    :return: None
    """
    for item in dictionary:
        print('{0:40} {1}'.format(dictionary[item][0:40], item))


def getTablePdf(dictionary, id):
    """
    Méthode utilisée pour récupérer les PDF voulus par l'utilisateur
    :param dictionary: dictionnaire des fichiers PDF trouvés dans le dossier
    :param id: tableau d'id récupéré de l'utilisateur pour traiter seulement les PDF voulus
    :return: table contenant les pdf a traiter
    """
    table = []
    if id == '*':
        for item in dictionary:
            table.append(dictionary[item])
    else:
        id = id.replace(" ", ",")
        id = id.split(",")
        try:
            for i in id:
                try:
                    table.append(
                        dictionary[int(i)])  # passage de i de str en int car les clés du dictionnaire sont de type int
                except:
                    pass
        except KeyError:
            print("Wrong id : " + i)
    return table


if __name__ == '__main__':
    path = input("Tapez le chemin du dossier (exemple '../Corpus_2021' : \n")
    dict = getPdfs(path)
    showPdfs(dict)
    id = input("Tapez les identifiants des pdf a convertir (1 2 3 ou 1,2,3) (* pour tous) : \n")
    directory = getTablePdf(dict, id.lstrip())
    get_info(path, directory)
