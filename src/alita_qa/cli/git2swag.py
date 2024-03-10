from ..git2swagger import main as git2swag
import argparse
import logging

logging.basicConfig(level=logging.INFO)

# Task example:
# Use repository spring-petclinic/spring-framework-petclinic with 
# branch main It is Java Spring application, please create swagger spec. 
# Deployment URL is https://petclinic.example.com
git2swag = argparse.ArgumentParser(prog='Git to Swagger', description='Generates swagger files from a git repository')
git2swag.add_argument('-t', '--task', type=str, help='Task to be performed', required=True)

def main():
    args = git2swag.parse_args()
    for message in git2swag(args.task):
        if 'actions' in message.keys():
            print(message['actions'][0].log)
        else:
            print ("Some other message ")
    
