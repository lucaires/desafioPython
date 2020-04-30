import requests
import json
import hashlib


# Faz a requisição get retornando um arquivo json
req = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=657db0cd9f7f554963f5af9e99893a43a83555b7')
resp = json.loads(req.text)

# Função que grava os dados JSON recuperados em um arquivo answer
def escrever_json(lista):
    with open('answer.json', 'w') as f:
        json.dump(lista, f)

# Função para decifrar
def decripta(mensagem, chave):
    cripto = ''
    for i in mensagem:
        if 'A' <= i <= 'Z':
            if ord(i) - chave < ord('A'):
                cripto += chr(ord('Z') - (chave - (ord(i) + 1 - ord('A'))))
            else:
                cripto += chr(ord(i) - chave)
        elif 'a' <= i <= 'z':
            if ord(i) - chave < ord('a'):
                cripto += chr(ord('z') - (chave - (ord(i) + 1 - ord('a'))))
            else:
                cripto += chr(ord(i) - chave)
        else:
            cripto += i
    return cripto


# separando o campo cifrado
msg = resp['cifrado']
print(msg)

#pegando o numero de casas para decifrar
key = resp['numero_casas']
print(key)

# Pegar a mensagem decifrada
cripto = decripta(msg, key)


# adicionar no campo decifrado
resp['decifrado'] = cripto


result = hashlib.sha1(cripto.encode())
msg_cifra = result.hexdigest()

print(msg_cifra)

resp['resumo_criptografico'] = msg_cifra
print(resp)


#função para escrever o arquivo json com a mensagem cifrada
escrever_json(resp)

#função para enviar o arquivo answer.json em formato multiform
url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=657db0cd9f7f554963f5af9e99893a43a83555b7'
files = {'answer': open('answer.json', 'rb')}

r = requests.post(url, files=files)
r.text

#Resultado do desafio.
print(r.json())