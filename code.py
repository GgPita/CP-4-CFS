import re
import requests
from jsonify import convert
import smtplib
import json
import pymongo

url = 'https://grupoutah.com.br'

request = requests.get(url)
html = request.text

sites = (re.findall(r'\bhref="https://\w+\.\w+\.\w+\.\w+/\w+', html))
diretorios = json.dumps(sites)
print(f"\nDiretórios encontrados: \n", diretorios)

#os.chdir("C:/Users/gusta/OneDrive/Área de Trabalho/python projects")
#with open("diretorios.txt", "w") as file:
    #json.dump(diretorios, file)

#teste = convert.jsonify("teste.txt")
#print(teste)

testando = "teste jadson."

def send_email(email,password,message):
    server = smtplib.SMTP("smtp.office365.com", 587,)
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, message)
    server.quit()

send_email('gugupitabersanete2607@hotmail.com', 'senha', diretorios)
