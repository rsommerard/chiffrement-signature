# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os

### adresse du serveur de TP
BASE_URL = "http://pac.bouillaguet.info/TP1"
ENCODING = 'utf-8'

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
    """with open('public_key.pem', 'r') as file:
        public_key = file.read()

    with open('secret_key.pem', 'r') as file:
        secret_key = file.read()

    os.system('openssl pkeyutl -sign -inkey secret_key.pem -in public_key.pem | base64 > signed_key')

    with open('signed_key', 'r') as file:
        signed_key = file.read()

    parameters = {'public-key': public_key, 'auth': signed_key}

    response = server_query(BASE_URL + '/web-of-trust/put/sommerard', parameters)

    print(response, "\n")"""

    with open('sommerard_signed_by_duthoit.sign', 'r') as file:
        sommerard_signed_by_duthoit = file.read()

    #os.system('openssl pkeyutl -sign -inkey secret_key.pem -in sommerard_signed_by_duthoit.sign | base64 > sommerard_signed_by_duthoit_signed.sign')

    with open('sommerard_signed_by_duthoit_signed.sign', 'r') as file:
        sommerard_signed_by_duthoit_signed = file.read()

    parameters = {"signer": "duthoit", "signature": sommerard_signed_by_duthoit, "auth": sommerard_signed_by_duthoit_signed}

    response = server_query(BASE_URL + '/web-of-trust/sign/sommerard', parameters)

    print(response, "\n")
