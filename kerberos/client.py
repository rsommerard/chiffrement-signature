# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import subprocess

### adresse du serveur de TP
BASE_URL = "http://pac.bouillaguet.info/TP1"
ENCODING = 'utf-8'

class DecryptionError(Exception):
    pass

def enc(msg, cipher="aes-128-cbc", passphrase=None, base64=True, decrypt=False):
    """invoke the OpenSSL library (though the openssl executable which must be
       present on your system to encrypt or decrypt content using a symmetric cipher.

       # encryption use
       >>> c = enc("toto", passphrase="foobar")

       # decryption use
       >>> enc(c, passphrase="foobar", decrypt=True)
       'toto'
       """

    args = ["openssl", "enc", "-" + cipher]
    if base64:
        args.append("-base64")
    if passphrase:
        args.append("-k")
        args.append(passphrase)
    if decrypt:
        args.append('-d')
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    if stderr == "bad decrypt\n":
        raise DecryptionError()
    return stdout.decode(ENCODING)

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
    parameters = {'login': 'sommerard'}
    response = server_query(BASE_URL + '/kerberos/AS', parameters)

    print(response, "\n")

    msg = json.dumps({'login': 'sommerard', 'timestamp': time.time()})

    print(msg, "\n")

    print(response['Client-TGS-key'], "\n")
    tgs_key = enc(response['Client-TGS-key'], passphrase='a6a14edecccbdbe6e5dabceb', decrypt=True)
    print(tgs_key, "\n")

    encmsg = enc(msg, passphrase=tgs_key)

    parameters = {'Ticket-Granting-Ticket': response['Ticket-Granting-Ticket'], 'server': '189.11.154.8', 'authenticator': encmsg}

    print(parameters, "\n")

    response = server_query(BASE_URL + '/kerberos/TGS', parameters)

    print(response, "\n")



    msg = json.dumps({'login': 'sommerard', 'timestamp': time.time()})

    server_key = enc(response['Client-Server-key'], passphrase=tgs_key, decrypt=True)

    encmsg = enc(msg, passphrase=server_key)

    parameters = {'Client-to-Server-Ticket': response['Client-to-Server-Ticket'], 'authenticator': encmsg}

    response = server_query(BASE_URL + '/kerberos/189.11.154.8', parameters)

    print(response, "\n")

    print(enc(response, passphrase=server_key, decrypt=True))

    parameters = {'proof': 'U2FsdGVkX18BpD1wiziQXRgw+mhPfQVSp/SY4f7s8fdp9YsY+BZqZrSkPMjGxhQR\nlMyQNp96xOIQTO4l4Z194A=='}

    response = server_query(BASE_URL + '/kerberos/mission-accomplished', parameters)

    print(response, "\n")
