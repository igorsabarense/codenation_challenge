import requests
import hashlib
import json
from pprint import pprint

GET_URL = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=921518d49d6bc5b1920838a5623f9dadeb975d14"
POST_URL = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=921518d49d6bc5b1920838a5623f9dadeb975d14"

data = requests.get(GET_URL).json()

with open('answer.json', 'w') as outfile:
    json.dump(data, outfile)

cifra = data['cifrado'];
CEASER_KEY = data['numero_casas']
print(cifra)


# updateJson("decifrado", decifrado)


def decrypt(cifra, key):
    decifrado = ""

    for i in range(0, len(cifra)):

        if cifra[i] == '.' or cifra[i] == ' ':
            decifrado += cifra[i]
        elif (ord(cifra[i]) - key) < 97:
            pos = 97 - (ord(cifra[i]) - key)
            decifrado += chr(122 + 1 - pos)
        else:
            decifrado += chr(ord(cifra[i]) - key)

    return decifrado


dec = decrypt(cifra, CEASER_KEY)


def updatejsonfile(field, new_data):
    jsonFile = open("answer.json", "r")  # Open the JSON file for reading
    data = json.load(jsonFile)  # Read the JSON into the buffer
    jsonFile.close()  # Close the JSON file

    ## Working with buffered content
    tmp = data['' + field + '']
    data['' + field + ''] = new_data

    ## Save our changes to JSON file
    jsonFile = open("answer.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


updatejsonfile('decifrado', dec)
sha1 = hashlib.sha1(dec.encode('utf-8')).hexdigest()
updatejsonfile('resumo_criptografico', sha1)

answer = {'answer': open('answer.json', 'rb')}
r = requests.post("https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=921518d49d6bc5b1920838a5623f9dadeb975d14", files=answer)
print(r.status_code, r.reason)
