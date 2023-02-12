from datetime import datetime
from zenpy import Zenpy
import tokens
from dbconn import dbconn

# Create a Zenpy instance
zenpy_client = Zenpy(domain="zendesk.com",subdomain=tokens.__logos_subdomain__,email=tokens.__logos_mail__,token=tokens.__logos_zendesk__)

# Get a psql connection
conn = dbconn.connect( dbconn.config() )
cursor = conn.cursor()

# Get a view content
content = zenpy_client.views.execute(view=tokens.__view_opentickets__)

# Perform a simple for
for i in range(content.count):

    row = content.next()

    agent = ""
    values = " "
    
    if len(row.created) == 0:
        data_create = "1999-01-01"

    if row.organization_id == None:
        organizationid = 0
    else:
        organizationid = row.organization_id

    if len(row.custom_fields) > 0:
        agent = row.custom_fields[0]["name"]

    params = [row.ticket_id , row.subject, row.requester.name, row.priority, "TIMESTAMP '" + row.created[0:10] + "'", row.group, agent, organizationid]

    for position in range(len(params)):
        if (params[position] == 0 and position < 7) or params[position] == "" or params[position] == None:
            params[position] = ""
        
        if position < 7:
            if type(params[position]) == int:
                values = values + str(params[position]) + ", "
            elif position == 4:
                values = values +params[position] + ", "
            else:
                values = values + "'" + params[position] + "', "
        else:
            if type(params[position]) == int:
                values = values + str(params[position])
            else:
                values = values + "'"+params[position] + "'"

    sql = "INSERT INTO opentickets VALUES({values})".format(values = values)
    cursor.execute( sql )
    #cursor.execute("INSERT INTO opentickets VALUES(10500,'assunto teste','Gustavo Jesus','normal',TimeStamp '2023-02-10','','Gustavo Jesus',123456)")

conn.commit()
cursor.close()
conn.close()
    