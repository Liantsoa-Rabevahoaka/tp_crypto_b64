from Crypto.Cipher import AES
import base64

# Instance AES (Même clé, même mode)
objet_de_dechiffrement = AES.new("cle16 octets AES".encode(), AES.MODE_ECB)

# Lecture du fichier chiffré
contenu_chiffre = open("crypte.jpg", "rb").read()

# (A FAIRE 1) Déchiffrer avec AES
Message_Encode = objet_de_dechiffrement.decrypt(contenu_chiffre)

# (A FAIRE 2) Décoder avec Base64
contenu_decode = base64.b64decode(Message_Encode)

# Écriture du fichier clair
with open("fichier_claire_decrypte.jpg", "wb") as fichier_sortie:
    fichier_sortie.write(contenu_decode)