# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import subprocess
import os

### adresse du serveur de TP
BASE_URL = "http://pac.bouillaguet.info/TP1"
ENCODING = 'utf-8'

class DecryptionError(Exception):
    pass

def server_query( url, parameters=None ):
     try:
        request = urllib.request.Request(url)
        data = None
        if parameters is not None:
            data = json.dumps(parameters).encode(ENCODING)
            request.add_header('Content-type', 'application/json')
        with urllib.request.urlopen(request, data) as connexion:
            result = connexion.read().decode(ENCODING)
            if connexion.info()['Content-Type'] == "application/json":
                result = json.loads(result)
        return result
     except urllib.error.HTTPError as e:
        print('error while accessing {2} : [{0}] {1}'.format(e.code, e.reason, url))
        print('the server also says: ' + e.read().decode(ENCODING))

if __name__ == '__main__':
    # echo "Hi, how are you?" > msg2send
    # openssl pkeyutl -encrypt -pubin -inkey server_public_key -in msg2send | base64 > msg2send_enc
    
    """with open('msg2send_enc', 'r') as file:
        msg2send_enc = file.read()

    parameters = {'ciphertext': msg2send_enc}

    response = server_query(BASE_URL + '/public-key-101/submit/sommerard', parameters)

    print(response, "\n")

    #-----------------------------------------------------------------------------

    # openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out my_private_key
    # openssl pkey -in my_private_key -pubout -out my_public_key

    with open('my_public_key', 'r') as file:
        my_public_key = file.read()
    
    parameters = {'public-key': my_public_key}
    
    response = server_query(BASE_URL + '/public-key-101/query/sommerard', parameters)

    with open('response_enc_b64', 'w') as file:
        file.write(response)

    # base64 -d response_enc_b64 > response_enc
    os.system("base64 -d response_enc_b64 > response_enc")
    
    # openssl pkeyutl -decrypt -inkey my_private_key -in response_enc -out response_dec
    os.system("openssl pkeyutl -decrypt -inkey my_private_key -in response_enc -out response_dec")

    # /public-key-101/magic/53616C7465645F5F38979F37A28738996ADCB33950DF1C7BEBA9784E5AED39EE
    with open('response_dec', 'r') as file:
        response_dec = file.read()

    print(response_dec, "\n")"""

    #-----------------------------------------------------------------------------

    # openssl rand 128 | base64 > K

    # MO4f73kpRLo0L7Nk74WhQnapDfO0CIS9mOiV89JeHUIvVtSj1pMQH8+BGT2Vhoj/JPloBV++suL2
    # UhFSILtpATq1btrntvVrTh5/D2FfpyUv6h+zEpR12E9lDZmcNAveIDW+qzYNkvvsQvqDRY3nt8lh
    # UlVDFUcOUpN6m6puZ4E=

    # openssl pkeyutl -encrypt -pubin -inkey server_public_key -in K | base64 > sessionkey2send
    os.system('openssl pkeyutl -encrypt -pubin -inkey server_public_key -in K | base64 > sessionkey2send')

    with open('sessionkey2send', 'r') as file:
        sessionkey2send = file.read()

    with open('my_public_key', 'r') as file:
        my_public_key = file.read()

    parameters = {'public-key': my_public_key, 'session-key': sessionkey2send}

    response = server_query(BASE_URL + '/public-key-101/hybrid/sommerard', parameters)

    with open('response_sessionkey_enc_b64', 'w') as file:
       file.write(response['session-key'])

    # base64 -d response_sessionkey_enc_b64 > response_sessionkey_enc
    os.system("base64 -d response_sessionkey_enc_b64 > response_sessionkey_enc")
    
    # openssl pkeyutl -decrypt -inkey my_private_key -in response_sessionkey_enc -out response_sessionkey_dec
    os.system("openssl pkeyutl -decrypt -inkey my_private_key -in response_sessionkey_enc -out response_sessionkey_dec")

    with open('response_ciphertext_enc_b64', 'w') as file:
       file.write(response['ciphertext'])

    # base64 -d response_ciphertext_enc_b64 > response_ciphertext_enc
    os.system("base64 -d response_ciphertext_enc_b64 > response_ciphertext_enc")

    # openssl enc -aes-128-cbc -d -kfile response_sessionkey_dec -in response_ciphertext_enc > response_ciphertext_dec
    os.system("openssl enc -aes-128-cbc -d -kfile response_sessionkey_dec -in response_ciphertext_enc > response_ciphertext_dec")

    with open('response_ciphertext_dec', 'r') as file:
        response_ciphertext_dec = file.read()

    print(response_ciphertext_dec)

    


    os.system("openssl rand 128 | base64 > K2")

    os.system('openssl pkeyutl -encrypt -pubin -inkey server_public_key -in K2 | base64 > sessionkey2send2')

    os.system("openssl enc -aes-128-cbc -kfile K2 -in msg2send2 > msg2send2_enc")

    os.system("base64 msg2send2_enc > msg2send2_enc_b64")

    with open('msg2send2_enc_b64', 'r') as file:
        msg2send2_enc_b64 = file.read()

    with open('sessionkey2send2', 'r') as file:
        sessionkey2send2 = file.read()

    print(sessionkey2send2)

    parameters = {'session-key': sessionkey2send2, 'ciphertext': msg2send2_enc_b64}

    response = server_query(BASE_URL + '/public-key-101/validate', parameters)

    print(response)
