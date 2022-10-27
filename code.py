import re
import requests
import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pymongo import MongoClient

#Utilizando método get para coletar o código fonte html da página web
url = 'https://grupoutah.com.br'
request = requests.get(url)
html = request.text

#Utilizando uma regex para filtrar o código html em busca de URLs
#r'\bhref="https://\w+\.\w+\.\w+\.\w+/\w+-\w+' regex principal menos específica
#r'https://\w+\.\w+\.\w+\.\w+/\w+-\w+-\w+-\w+-\w+' regex mais específica
sites = (re.findall(r'https://\w+\.\w+\.\w+\.\w+/\w+-\w+-\w+-\w+-\w+', html))
#diretorios = json.dumps(sites)
#print(f"\nDiretórios encontrados: \n", sites)

#Transformando a lista retornada pela regex em um dicionário
dict = {"URLs":[]}
length = len(sites)
i = 0
while i < length:
    dict["URLs"].append(sites[i])
    i += 1   
#print(dict)

#Usando método json.dump() para escrever o conteúdo do dicionário "dict" em um arquivo .json
os.chdir("C:/Users/gusta/OneDrive/Área de Trabalho/python projects")
with open("diretorios.json", "w") as file:
    json.dump(dict, file)

#Usando método write() para escrever o conteúdo da lista "sites" em um arquivo de texto, 
# colocando cada elemento em uma linha
with open("diretorios.txt", "w") as file2:
    for i in sites:
        file2.write("%s=\n" % i)

#Usando módulo smtplib e MIME para enviar o arquivo contendo todas as URLs encontradas 
# para o endereço email indicado
def send_email(email,password):
    content_email = 'Checkpoint 4 - all_in - RM92917'
    subject = 'URLs encontradas no site escaneado.'
    msg = MIMEMultipart('alternative')
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject
    body = MIMEText(content_email, 'plain')
    msg.attach(body)

    filename = 'diretorios.txt'
    with open(filename, 'r') as f:
        part = MIMEApplication(f.read(), Name=(filename))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format((filename))
    msg.attach(part)
    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(email,password)
    server.send_message(msg, from_addr=email, to_addrs=[email])
    server.quit()

send_email('email', 'password')

#Usando módulo pymongo para fazer a conexão com banco MongoDB cloud 
# e inputar o dicionário "dict" contendo as URLs encontradas pela regex
connection = 'connection string'
client = MongoClient(connection)
db = client.database
collection = db.collection_name
collection.insert_one(dict)
