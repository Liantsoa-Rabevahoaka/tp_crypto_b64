import socket
import _thread as thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64

def Traiter_Connexion(connexion_avec_client, adresse_client):
    global objet_cle_rsa_prive, contenu_clepublique
    
    print("Connexion de la machine =", adresse_client)
    connexion_avec_client.send(contenu_clepublique)
    
    # Reçoit la clé AES chiffrée
    cle_AES_chiffre = connexion_avec_client.recv(1024)
    
    # (A FAIRE 1) Déchiffrer la clé AES avec la clé privée
    cle_AES = objet_cle_rsa_prive.decrypt(cle_AES_chiffre)
    
    # Création de l'objet AES
    objet_de_dechiffrement = AES.new(cle_AES, AES.MODE_ECB)
    
    try:
        while True:
            Message_Chiffre = connexion_avec_client.recv(1024)
            
            # (A FAIRE 2) Déchiffrer le message avec AES
            Message_Decode = objet_de_dechiffrement.decrypt(Message_Chiffre)
            
            # (A FAIRE 3) Décoder avec Base64
            MessageRec = base64.b64decode(Message_Decode)
            
            if MessageRec == b"Fin":
                break
            
            print("Client", adresse_client, "a dit :", MessageRec.decode())
            
    except Exception as e:
        print("Déconnexion ou erreur :", e)
        
    print("Déconnexion de :", adresse_client)
    try:
        connexion_avec_client.close()
    except:
        pass

SocketServeur = socket.socket()
host = socket.gethostname()
port = 9500
SocketServeur.bind(("127.0.0.1", port)) # Correction: Tuple
SocketServeur.listen(5)

contenu_clepublique = open("fichier_cle_publique.pem", "rb").read()

# Correction du nom de fichier (le PDF disait "prise" au lieu de "privee")
contenu_cleprivee = RSA.importKey(open("fichier_cle_privee.pem", "rb").read())
objet_cle_rsa_prive = PKCS1_OAEP.new(contenu_cleprivee)

print("Lancement serveur...")
while True:
    ConnexionAUnClient, addrclient = SocketServeur.accept()
    thread.start_new_thread(Traiter_Connexion, (ConnexionAUnClient, addrclient))