# RAMvenom

RAMvenom est un outil permettant de générer un fichiers Python ou EXE contenant un payload qui égorge la mémoire vive (RAM) et du processeur (CPU).

ATTENTION ! VEILLEZ A MANIPULER AVEC PRUDENCE LE FICHIER GÉNÉRÉ ET NE PAS L'OUVRIR. SI ÉXÉCUTER PAR ACCIDENT VEUILLEZ SUPPRIMER WINDOWS.
(COMPATIBLE SEULEMENT POUR WINDOWS, UPDATE A VOIR...)

## Fonctionnalités

- Encodage du payload :
  - Base64
  - XOR
  - AES
  - ROT13
  - Zlib
- Génération de fichiers :
  - Fichier Python (.py)
  - Fichier exécutable (.exe) via PyInstaller
- Interface en ligne de commande avec affichage en ASCII art

## Dépendances

- `pycryptodome` pour le chiffrement AES
- `pyinstaller` pour la compilation en exécutable

### Installation des dépendances

pip install pycryptodome pyinstaller

