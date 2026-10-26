# TP Cryptographie Appliquée - Partie 3 : Encodage Base64 & AES

Ce projet contient l'implémentation complète du TP de cryptographie portant sur l'encodage Base64, le chiffrement symétrique (AES) et la communication sécurisée via sockets entre un client et un serveur.

## 📋 Prérequis

- **Système d'exploitation** : Ubuntu (ou toute distribution Linux basée sur Debian)
- **Python** : Version 3.8 ou supérieure
- **Bibliothèque cryptographique** : `pycryptodome` (l'équivalent moderne et maintenu de `Crypto`)

## 🚀 Installation et Configuration (depuis zéro)

Suivez ces étapes pour configurer l'environnement virtuel et installer les dépendances nécessaires.

### 1. Mise à jour du système et installation des outils Python
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### 2. Création et activation de l'environnement virtuel
Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances de ce projet.
```bash
# Se placer dans le dossier du projet
cd tp_crypto_b64

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement (à faire à chaque nouvelle session de terminal)
source venv/bin/activate
```

### 3. Installation des dépendances
```bash
pip install pycryptodome
```

---

## 📂 Structure du projet

```
tp_crypto_b64/
├── gen_keys.py           # Script de génération des clés RSA (à lancer en premier)
├── chiffrement.py        # Script de chiffrement AES + Base64 d'une image
├── dechiffrement.py      # Script de déchiffrement d'une image
├── serveur.py            # Serveur socket (reçoit les messages chiffrés)
├── client.py             # Client socket (envoie les messages chiffrés)
├── fichier_claire.jpg    # Image d'origine (à fournir)
├── fichier_cle_publique.pem   # Clé publique RSA (générée)
├── fichier_cle_privee.pem     # Clé privée RSA (générée)
└── README.md             # Ce fichier
```

---

## 🛠️ Guide d'utilisation

### Partie 1 : Chiffrement et Déchiffrement d'image (Local)

Cette partie permet de chiffrer une image en utilisant AES, avec un encodage préalable en Base64 pour gérer le padding.

**Étape 1** : Placez une image nommée `fichier_claire.jpg` dans le dossier du projet.

**Étape 2** : Lancez le chiffrement.
```bash
python chiffrement.py
```
*Cela génère un fichier `crypte.jpg` (le contenu chiffré).*

**Étape 3** : Lancez le déchiffrement.
```bash
python dechiffrement.py
```
*Cela génère un fichier `fichier_claire_decrypte.jpg` qui doit être identique à l'original.*

---

### Partie 2 : Communication Client/Serveur Sécurisée

Cette partie met en place une communication où le client génère une clé AES, la transmet chiffrée avec RSA au serveur, puis échange des messages chiffrés en AES + Base64.

**Étape 1 : Générer les clés RSA**
Obligatoire avant de lancer le serveur. Lancez ce script **une seule fois**.
```bash
python gen_keys.py
```
*Cela crée `fichier_cle_publique.pem` et `fichier_cle_privee.pem`.*

**Étape 2 : Lancer le Serveur**
Dans un **premier terminal** (avec le venv activé) :
```bash
python serveur.py
```
*Le serveur affiche `Lancement serveur...` et attend les connexions sur le port 9500.*

**Étape 3 : Lancer le Client**
Dans un **second terminal** (avec le venv activé) :
```bash
python client.py
```
*Le client se connecte au serveur. Vous pouvez taper des messages.*
*Tapez `Fin` pour clôturer la session.*

**Exemple de session :**
- **Client** : `Message > Bonjour`
- **Serveur** : `Client ('127.0.0.1', 33170) a dit : Bonjour`
- **Client** : `Message > Fin`

---

## 📝 Réponses aux questions théoriques du TP

### 1. Encodage Base64
**Q1. Décoder la phrase `QnJhdm8sIHZvdXMgYXZleiBkw6ljb2TDqSBsZSBtZXNzYWdlLg==`**
> **Réponse** : `Bravo, vous avez décodé le message.`

**Q2. Ajouter plusieurs `=` à la fin et décoder. Quel est l'effet ?**
> **Réponse** : Une erreur `binascii.Error` est levée. Le caractère `=` est un caractère de bourrage strict qui indique la fin du flux Base64. On ne peut pas en ajouter arbitrairement sans casser la structure des blocs de 4 caractères.

**Q3. L'encodage Base64 offre-t-il la propriété de diffusion ? Pourquoi ?**
> **Réponse** : **Non**. Base64 est un simple encodage (transformation bijective réversible), et non un algorithme de chiffrement. Il ne possède pas de clé secrète et ne modifie pas massivement les bits de sortie en cas de changement d'un bit d'entrée, contrairement à AES ou aux fonctions de hachage.

### 2. Chiffrement AES + Base64 sur image
**Q1 & Q2. Compléter le programme de chiffrement/déchiffrement**
> **Réponse** : Voir les fichiers `chiffrement.py` et `dechiffrement.py`. Le point clé est l'utilisation de `base64.b64encode()` pour l'encodage, puis l'ajout d'octets `b'='` pour que la taille soit un multiple de 16 avant le chiffrement AES.

**Q3. Quelle est l'image en résultat ?**
> **Réponse** : L'image `fichier_claire_decrypte.jpg` est **strictement identique** à l'image d'origine `fichier_claire.jpg`. Le processus de chiffrement/déchiffrement est symétrique et sans perte.

### 3. Communication Client/Serveur
**Q. Compléter le code Serveur (A FAIRE 1, 2, 3) et Client (A FAIRE 1, 2)**
> **Réponse** : Voir les fichiers `serveur.py` et `client.py`.
> - **Côté Client** : Envoi de la clé AES chiffrée avec RSA (`SocketClient.send(cle_AES_chiffre)`), puis encodage Base64 du message avant chiffrement AES.
> - **Côté Serveur** : Déchiffrement de la clé AES avec la clé privée RSA, puis déchiffrement AES du message et décodage Base64.

---
