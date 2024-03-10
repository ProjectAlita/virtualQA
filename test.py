from src.alita_qa.git2swagger import main as git2swag
import logging
logging.basicConfig(level=logging.ERROR)

g2s_task = """Use repository spring-petclinic/spring-framework-petclinic with branch main 
It is Java Spring application, please create swagger spec. Store them in folder `swaggers`. 
Deployment URL is https://petclinic.example.com"""


for message in git2swag(g2s_task):
    # This is basically the place where we can form chat history
    if 'actions' in message.keys():
        print(message['actions'][0].log)
    else:
        print ("Some other message ")
    