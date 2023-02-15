from zenpy import Zenpy
import tokens
from dbconn import dbconn

# Create a Zenpy instance
zenpy_client = Zenpy(domain="zendesk.com",subdomain=tokens.__logos_subdomain__,email=tokens.__logos_mail__,token=tokens.__logos_zendesk__)

# Get a psql connection
conn = dbconn.connect( dbconn.config() )
cursor = conn.cursor()

# Get a view content
content = zenpy_client.views.execute(view=tokens.__view_quarterlytickets__)

# Perform a simple for
for i in range(content.count):

    row = content.next()

    agent = ""
    module = ""
    values = " "

    #validate and ajust 
    if len(row.created) == 0:
        data_create = "1999-01-01"

    if row.organization_id == None:
        organizationid = 0
    else:
        organizationid = row.organization_id

    if len(row.custom_fields) > 1:
        agent = row.custom_fields[0]["name"]
        module = row.custom_fields[1]["name"]
    elif len(row.custom_fields) > 0:
        agent = row.custom_fields[0]["name"]

    #prepare array for the insert parameters
    params = [row.ticket_id, 
              row.subject, 
              row.type, 
              row.ticket.status, 
              row.requester.name, 
              row.priority, 
              "TIMESTAMP '" + row.created[0:10] + "'", 
              "TIMESTAMP '" + row.updated[0:10] + "'", 
              row.group, 
              agent, 
              module, 
              organizationid]

    #make sql insert string
    for position in range(len(params)):
        if (params[position] == 0 and position < 7) or params[position] == "" or params[position] == None:
            params[position] = ""
        
        if position < 11:
            if type(params[position]) == int:
                values = values + str(params[position]) + ", "
            elif position == 6 or position == 7: #6 or 7 to the TIMESTAMP string convert
                values = values +params[position] + ", "
            else:
                values = values + "'" + params[position] + "', "
        else:
            if type(params[position]) == int:
                values = values + str(params[position])
            else:
                values = values + "'"+params[position] + "'"

    #execute sql command
    sql = "INSERT INTO quarterlytickets VALUES({values})".format(values = values)
    cursor.execute( sql )

conn.commit()
cursor.close()
conn.close()
    