from zenpy import Zenpy
import tokens

# Create a Zenpy instance
zenpy_client = Zenpy(domain="zendesk.com",subdomain=tokens.__logos_subdomain__,email=tokens.__logos_mail__,token=tokens.__logos_zendesk__)

# Get a view content
content = zenpy_client.views.execute(view=tokens.__view_opentickets__)

# Perform a simple for
for i in range(content.count):
    row = content.next()
    print("Ticket: ", row.ticket_id)
    print("Assunto: ", row.subject)
    print("Solicitante: ", row.requester)
    print("Prioridade: ", row.priority)
    print("Data de criação: ", row.created)
    print("Grupo: ", row.group)
    print("\n")
    