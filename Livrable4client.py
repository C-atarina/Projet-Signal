# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 08:56:49 2020

@author: Catarina RORIZ
"""
from heapq import heappush, heappop, heapify
from collections import defaultdict
import socket 

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Huffmann 

def dec2bin(valeur,taille):
    listeval = list(bin(valeur))
    for i in range(2):
        listeval.pop(0)
    return "".join(listeval).zfill(taille)

def encode(bibliotheque):
    arbre = [[wt, [sym, ""]] for sym, wt in bibliotheque.items()]
    heapify(arbre)
    while len(arbre) > 1:
        bas = heappop(arbre)
        haut = heappop(arbre)
        for pair in bas[1:]:
            pair[1] = '0' + pair[1]
        for pair in haut[1:]:
            pair[1] = '1' + pair[1]
        heappush(arbre, [bas[0] + haut[0]] + bas[1:] + haut[1:])
    return sorted(heappop(arbre)[1:] for key in range(len(arbre)))

#------------------------------------ Ouverture fichier à envoyer 
fichier = open("message.txt","rb")
contenue=fichier.read()
print(contenue)
print(" ")

#------------------------------------ Impression de la bibliothèque Huffmann
bibliotheque = defaultdict(int)
for i in contenue:
    bibliotheque[i] += 1
huff = encode(bibliotheque)

diconul = {}
for p in huff:
    for i in p:
        diconul[str(i[0])] = i[1]
print(diconul)
print("")

#------------------------------------ Fichier codé avec la bibliothèque
message = ""
for a in contenue:
    message += diconul[str(a)]
print (message)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& CRC + socket

data = message

# -----------------------------------------Fonction XOR
def xor(a, b): 

	# tableau de résultat
	result = [] 

	# analyse des bits pour calcul XOR
	for i in range(1, len(b)): 
		if a[i] == b[i]: 
			result.append('0') 
		else: 
			result.append('1') 

	return ''.join(result) 


# --------------------------------- de calcul modulo 2 pour CRC 
def mod2div(divident, divisor): 

	pick = len(divisor) 

	
	tmp = divident[0 : pick] 

	while pick < len(divident): 

		if tmp[0] == '1': 

			 
			# Rabaisse les bits pour calculer 
			tmp = xor(divisor, tmp) + divident[pick] 

		else: # si le bit restant est 0
            
			tmp = xor('0'*pick, tmp) + divident[pick] 

		# incrementation
		pick += 1


	if tmp[0] == '1': 
		tmp = xor(divisor, tmp) 
	else: 
		tmp = xor('0'*pick, tmp) 

	checkword = tmp 
	return checkword 

# -------------------------------------Fonction de codage
def encodeData(data, key): 

	l_key = len(key) 

	# Utilisation du reste de la division modulo 2
	appended_data = data + '0'*(l_key-1) 
	remainder = mod2div(appended_data, key) 

	# Envoie le message + le reste de la division
	codeword = data + remainder 
	return codeword	 
	
# ------------------------------Creation socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		 

port = 12345			

s.connect(('127.0.0.1', port)) 

key = "1001"
MessageAenvoyer = ""
#diconul = str(diconul)
#dico = diconul.encode()
for i in diconul:
    kek=""
    val=""
    for y in i:
        kek += dec2bin(ord(y),8)
        
    for y in diconul[i]:
        val += dec2bin(ord(y),8)

    MessageAenvoyer += kek + "11111111"+val+"11111111"


s.send(MessageAenvoyer.encode())

ans = encodeData(data,key)  
ans = ans.encode()
s.sendall(ans)


print (s.recv(1024)) 

s.close() 
