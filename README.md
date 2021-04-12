# PDFTOTXT

Réalisé par Romain Le Talour, Corentin Leconte, Thibaut Quilleré dans le cadre de l'UE Projet de développement.

**Attention**, ce programme est dans un but scolaire et n'est pas destiné à être utilisé par le grand public.

## Fonctionnalités:

- Prise en charge de fichier PDF.

- Prend en entrée un dossier contenant un ou des fichiers PDF et créé un sous-dossier pour y déposer les fichier PDF convertis en TXT ou XML (du même nom).

- Si un sous-dossier est déjà existant, il sera supprimé et remplacé par le nouveau.
  
## Comment l'utiliser:

Avec pdftotxt vous pouvez convertir un fichier PDF de type scientifique vers un fichier TXT ou XML.
Pour l'utiliser, taper la commande :

  `$ python pdftotxt.py`
  
  A l'exécution, entrez le répertoire contenant le ou les PDF à traiter.
  
  ```
  $ python pdftotxt.py
  Tapez le chemin du dossier (exemple '../Corpus_2021' :
  ../directory
  ```
  
  Ensuite un menu listera les PDF disponibles à la conversion dans le répertoire courant.
  
  ```
  example1.pdf             1
  example2.pdf             2
  example3.pdf             3
  example4.pdf             4
  
  Tapez les identifiants des pdf a convertir (1 2 3 ou 1,2,3) (* pour tous) : 
  1
  ['example1.pdf']
  ```
  
## Syntaxe:
Après le choix du/des PDF à convertir, choisir le format de sortie : 
  
  ```
  [-t] Pour convertir le PDF en un fichier TXT
  ```
  ```
  [-x] Pour convertir le PDF en un fichier XML sous la forme :
  
  <article>      
      <preamble> Le nom du fichier d’origine </preamble>
      <titre> Le titre du papier </titre>
      <auteurs>
      <auteur> L’auteur A et son adresse courriel</auteur>
      <affiliation> L’affiliation de l’auteur A et son adresse</affiliation>
      <auteur> L’auteur B et son adresse courriel</auteur>
      <affiliation> L’affiliation de l’auteur B et son adresse</affiliation>
      ...
      <auteurs/>
      <abstract> Le résumé de l’article</abstract>
      <introduction> La introduction</introduction>
      <corps> Le développement du papier</corps>
      <conclusion> La conclusion du papier</conclusion>
      <discussion> La discussion du papier</discussion>
      <biblio> Les références bibliographiques du papier</biblio>
  </article>
  ```
