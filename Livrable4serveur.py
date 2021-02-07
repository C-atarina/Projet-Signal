# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:16:34 2020

@author: Catarina Roriz
"""

import socket 

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

# ----------------------------------Fonction décodage, si le résultat est 0 alors le message n'est pas érroner
def decodemessage(message, key):     

    l_key = len(key) 


    appended_message = message + '0'*(l_key-1)
    reste = mod2div(appended_message, key) 

    return reste 

# ---------------------------------Création du socket 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ("Socket crée") 


port = 12345

s.bind(('', port)) 
print ("socket binded to %s" % (port)) 


while True: 

	message = (s.recv(65507)).decode() 

	print(message) 

	if not message: 
		break

	key = "1001"

	ans = decodemessage(message, key)
	print("Le reste après le décodage est->"+ans) 
s.close() 
