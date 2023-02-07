from zenpy import Zenpy
import tokens

# Create a Zenpy instance
zenpy_client = Zenpy(domain="zendesk.com",subdomain="logostechnology",email="valter@logostechnology.com.br",token=tokens.__logos_zendesk__)

# Get a view content
content = zenpy_client.views.execute(view="1500022583221")

# example
##content = {"name": 56, "eye_color": "green", "id": "45355", "name": "Nora", "childrens":{"Ch1":"Joao","Ch2":"Maria"}}
##print(content["childrens"]["Ch2"])

# Perform a simple for
for i in range(content.count):
    row = content.next()
    print("Ticket: ", row.ticket_id)
    print("Assunto: ", row.subject)
    print("Tipo: ", row.type)
    print("Status: ", row.ticket.status)
    print("Solicitante: ", row.requester.name)
    print("Prioridade: ", row.priority)
    print("Data de criação: ", row.created)
    print("Data de atualização: ", row.updated) 
    print("Grupo: ", row.group)
    print("\n")