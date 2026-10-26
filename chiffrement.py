from Crypto.Cipher import AES
import base64

# Correction: La clé doit être encodée en bytes, et PyCryptodome exige un mode (ECB ici)
# Le PDF omet le mode, ce qui plante sur les versions modernes.
objet_de_chiffrement = AES.new("cle16 octets AES".encode(), AES.MODE_ECB)

# Lecture du fichier
Message_claire = open("fichier_claire.jpg", "rb").read()

# (A FAIRE 1) Encoder le contenu avec Base64
Message_Ecode = base64.b64encode(Message_claire)

# (A FAIRE 2) Calculer le padding (le PDF met "b='", c'est une erreur)
if len(Message_Ecode) % 16 > 0:
    padding = 16 - (len(Message_Ecode) % 16)
else:
    padding = 0 # Sécurité si c'est déjà un multiple de 16

# Correction de la syntaxe du PDF : padding * b'=' (et non b=' )
Message_Ecode = Message_Ecode + padding * b'='

# Chiffrement
contenu_chiffre = objet_de_chiffrement.encrypt(Message_Ecode)

# Écriture du fichier chiffré
with open("crypte.jpg", "wb") as fichier_sortie:
    fichier_sortie.write(contenu_chiffre)