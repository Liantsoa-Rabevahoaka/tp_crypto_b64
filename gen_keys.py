from Crypto.PublicKey import RSA

key = RSA.generate(2048)
with open("fichier_cle_privee.pem", "wb") as f:
    f.write(key.export_key())
with open("fichier_cle_publique.pem", "wb") as f:
    f.write(key.publickey().export_key())
print("Clés RSA générées.")