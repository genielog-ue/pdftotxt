# PDFTOTXT

Réalisé par Romain Le Talour, Corentin Leconte, Thibaut Quilleré dans le cadre de l'UE Projet de développement.

**Attention**, ce programme est dans un but scolaire et n'est pas destiné à être utilisé par le grand public.

## Fonctionnalités:

- Prise en charge de fichier PDF.

- Prend en entrée un dossier contenant des fichiers PDF et créé un sous-dossier pour y déposer les fichier PDF convertis en PDF (au même nom).

- Si un sous-dossier est déjà existant, il sera supprimé et remplacé par le nouveau.
  
## Comment l'utiliser:

  `$ pdftotxt.py [-option] abc.pdf`
  Si le PDF cible n'est pas dans le répertoire du programme taper :
  `$ pdftotxt.py [-option] ../path/to/abc.pdf`
  
## Syntaxe:
  
  ```
  [-x] Pour convertir le PDF en un fichier TXT
  ```
  ```
  [-t] Pour convertir le PDF en un fichier XML sous la forme :
  <article>      
    <preamble> Le nom du fichier d’origine </preamble>
    <titre> Le titre du papier </titre>
    <auteur> La section auteurs et leur adresse </auteur>
    <abstract> Le résumé de l’article </abstract>
    <biblio> Les références bibliographiques du papier</biblio>
  </article>
  ```
