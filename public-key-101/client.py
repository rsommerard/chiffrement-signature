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

#pkfn: PubKeyFileName
#fnte: FileNameToEncrypt
#def enc(pkfn, fnte):
#    cmd = ["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey " + pkfn, "-in " + fnte]
#    result = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    stdout, stderr = result.communicate()
#    if stderr == "bad decrypt\n":
#        raise DecryptionError()
#    return stdout.decode(ENCODING)

#pkfn: PrivateKeyFileName
#fntd: FileNameToDecrypt
#def dec(pkfn, fntd):
#    cmd = ["openssl", "pkeyutl", "-decrypt", "-inkey " + pkfn, "-in " + fntd]
#    result = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    stdout, stderr = result.communicate()
#    if stderr == "bad decrypt\n":
#        raise DecryptionError()
#    return stdout.decode(ENCODING)

def server_query( url, parameters=None ):
     """Charge l'url demandÃ©e. Si aucun paramÃ¨tre n'est spÃ©cifiÃ©, une requÃªte
        HTTP GET est envoyÃ©e. Si des paramÃ¨tres sont prÃ©sents, ils sont encodÃ©s
        en JSON, et une requÃªte POST est envoyÃ©e.

        La mÃ©thode prÃ©conisÃ©e pour envoyer des paramÃ¨tres consiste Ã  les stocker
        dans un dictionnaire. Ceci permet de nommer les champs. Par exemple :

        #    sans paramÃ¨tres
        >>> response = server_query(BASE_URL + '/client-demo')
        >>> print(response)
        Je n'ai pas reÃ§u de paramÃ¨tres

        #    avec paramÃ¨tres
        >>> parameters = {'login': 'toto', 'id': 1337}
        >>> response = server_query(BASE_URL + '/client-demo', parameters)
        >>> print(response)
        Dans les paramÃ¨tres j'ai trouvÃ© :
        *) ``login'' : ``toto''
        *) ``id'' : ``1337''
        <BLANKLINE>
        """
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
    #parameters = {'ciphertext': 'CkbXv0IMmsENZDaa9RoVujTOhSqCiS7cFsCh5yEqt6V8j0rf1ZbZ91BAniU8hMvtsbXTwgm5Q7106mXFAi+gesQ8NVNvsfoMds0kz6rMVeuIAfbJxRDKK/7h3ACM1JFYuyq7yn93Zi6fSQpM2iXamzCcgtYtADjEFll9ToimcI3TLY4UncOSCbbwgwsJaIM+K73z7qViQfbPB34zU+so70qlAYwoLryEKUL6cmlEMpG85eyiBK6s6SnRRS7qjqMuASLteiGHGsVLUUDd0zEz3Y6wC0/cCxVVE78MRQp05G1qt/clUaK4tbOYynNtzIlio5QPO4aQzrwqbQggWM8hkA=='}

    #response = server_query(BASE_URL + '/public-key-101/submit/sommerard', parameters)

    #print(response, "\n")


    #-----------------------------------------------------------------------------

    #with open('rsa_key.pub', 'r') as file:
    #    public_key = file.read()

    #with open('rsa_key', 'r') as file:
    #    private_key = file.read()
    
    #parameters = {'public-key': public_key}
    #print("Parameters: \n", parameters)
    
    #response = server_query(BASE_URL + '/public-key-101/query/sommerard', parameters)

    #with open('response', 'w') as file:
    #    file.write(response)

    #print(response, "\n")

    #os.system('base64 -d response > resp_test')

    #msg_dec = dec('rsa_key', 'resp_test')

    #print(msg_dec)

    #base64 -d response > resp_b64d
    #openssl pkeyutl -decrypt -inkey rsa_key -in resp_b64d 

    #-----------------------------------------------------------------------------

    #openssl rand 128 | base64 > sym_128_key

    # MO4f73kpRLo0L7Nk74WhQnapDfO0CIS9mOiV89JeHUIvVtSj1pMQH8+BGT2Vhoj/JPloBV++suL2
    # UhFSILtpATq1btrntvVrTh5/D2FfpyUv6h+zEpR12E9lDZmcNAveIDW+qzYNkvvsQvqDRY3nt8lh
    # UlVDFUcOUpN6m6puZ4E=

    # openssl pkeyutl -encrypt -pubin -inkey get-PK -in sym_128_key | base64

    # PH0zt0K7N/6JsWBoUypbzGPcoU0Iqn1b+TN5nWorj6vAeybdYNCUBpGOgmnl6f503QRnlrIG/td6
    # zQ3cx90DW6VZzx51ikh44DxverUCyK9A1eGy6ols25zzSAfBZMfnH/bSqjwt/nGH8f7EigTTmrG8
    # u3+uMNpYZfwjTLNj7jANGnU2p72xAQ6Bj/5lYM85UJMDAXOdIuAGq9KycYOfEpYccX0oXotYICz+
    # 0oqffQuBfr2JOGCV2+5x5ekgeeuvRfJvpWgj6Q2OnGE2BvqImvdKK1ETvootd3rBp4asvtFvRD9q
    # s0KSWeaBWNeacafWZZIIo4k5heqJD2AsPNvqHQ==

    # openssl enc -aes-128-cbc -k sym_128_key -base64 -in msg2

    # U2FsdGVkX18y8Zl5EbnfY8fpaygYGb+sEc4/9FzLX/whz1a9GpOAT1/ItuBidAby


   with open('rsa_key.pub', 'r') as file:
        public_key = file.read()

   parameters = {'public-key': public_key, 'session-key': 'PH0zt0K7N/6JsWBoUypbzGPcoU0Iqn1b+TN5nWorj6vAeybdYNCUBpGOgmnl6f503QRnlrIG/td6zQ3cx90DW6VZzx51ikh44DxverUCyK9A1eGy6ols25zzSAfBZMfnH/bSqjwt/nGH8f7EigTTmrG8u3+uMNpYZfwjTLNj7jANGnU2p72xAQ6Bj/5lYM85UJMDAXOdIuAGq9KycYOfEpYccX0oXotYICz+0oqffQuBfr2JOGCV2+5x5ekgeeuvRfJvpWgj6Q2OnGE2BvqImvdKK1ETvootd3rBp4asvtFvRD9qs0KSWeaBWNeacafWZZIIo4k5heqJD2AsPNvqHQ=='}

   response = server_query(BASE_URL + '/public-key-101/hybrid/sommerard', parameters)

   print(response, "\n")

   with open('hybrid_ciphertext', 'w') as file:
       file.write(response['ciphertext'])

   with open('hybrid_session_key', 'w') as file:
       file.write(response['session-key'])
