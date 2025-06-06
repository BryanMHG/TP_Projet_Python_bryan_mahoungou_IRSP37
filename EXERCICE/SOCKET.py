#import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("example.com", 80))
# s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

# #Recevoir et afficher réponse du serveur
# response = s.recv(1024)
# print("sortie brute\n", response)

# # Afficher réponse formatée
# print("\nsortie formatée\n")
# print(response.decode("utf-8"))

# s.close()

#--------------------------------------------------------------------------------------------------------------------------------------------
import socket

s=socket.socket()

try:
    s.connect(("192.168.56.104",22))
    print("Port 22 Ouvert")
except socket.timeout:
    print("Timeout !")
except socket.error:
    print("Port fermé")
    
#--------------------------------------------------------------------------------------------------------------------------------------------

import argparse
