import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import time
import os

# Création clé AES
cle_AES = os.urandom(16)

SocketClient = socket.socket()
port = 9500
SocketClient.connect(("127.0.0.1", port)) # Correction: Tuple requis

cle_publique = b""
while True:
    recu = SocketClient.recv(1024)
    cle_publique += recu
    if b'---END PUBLIC KEY---' in cle_publique:
        break

cle_publique = RSA.importKey(cle_publique)
objet_cle_rsa_publique = PKCS1_OAEP.new(cle_publique)

# Chiffre la clé AES avec RSA
cle_AES_chiffre = objet_cle_rsa_publique.encrypt(cle_AES)

# (A FAIRE 1) Envoyer la clé chiffrée au serveur
SocketClient.send(cle_AES_chiffre)

time.sleep(1)
objet_de_chiffrement = AES.new(cle_AES, AES.MODE_ECB)

while True:
    # Correction syntaxe du PDF: input().encode()
    MessageATransmettre = input("Message > ").encode()
    
    # (A FAIRE 2) Encoder le message en Base64
    Message_Encode = base64.b64encode(MessageATransmettre)
    
    # Padding (s'il y a besoin)
    Message_Encode = Message_Encode + (16 - (len(Message_Encode) % 16)) % 16 * b'=' 
    
    SocketClient.send(objet_de_chiffrement.encrypt(Message_Encode))
    
    # Correction: == au lieu de :=
    if MessageATransmettre == b"Fin":
        break

SocketClient.close()