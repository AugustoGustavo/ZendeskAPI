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

#empty table
#sql = "DELETE FROM quarterlytickets "
#cursor.execute( sql )
#conn.commit()

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
        if len(row.custom_fields[0]) > 2:
            agent = row.custom_fields[0]["name"]
        if len(row.custom_fields[1]) > 2:
            module = row.custom_fields[1]["name"]
    elif len(row.custom_fields) > 0:
        if len(row.custom_fields[0]) > 2:
            agent = row.custom_fields[0]["name"]

    #prepare array for the insert parameters
    params = [row.ticket_id,                                #a
              row.subject,                                  #b
              row.type,                                     #c
              row.ticket.status,                            #d
              row.requester.name,                           #e
              row.priority,                                 #f
              "TIMESTAMP '" + row.created[0:10] + "'",      #g
              "TIMESTAMP '" + row.updated[0:10] + "'",      #H
              row.group,                                    #i
              agent,                                        #j
              module,                                       #k
              organizationid]                               #l

    #make sql insert string
    for position in range(len(params)):
        if (params[position] == 0 and position < 7) or params[position] == "" or params[position] == None:
            params[position] = ""

    #execute sql command
    sql = "INSERT INTO quarterlytickets VALUES({a},'{b}','{c}','{d}','{e}','{f}',{g},{h},'{i}','{j}','{k}',{l})"
    sql = sql.format(a = params[0], b = params[1],c = params[2],d = params[3],e = params[4],f = params[5],g = params[6],h = params[7],i = params[8],j = params[9],k = params[10],l = params[11])
    sql += " ON CONFLICT (ticket_id) DO UPDATE SET"
    sql += " subject = '{b}', status = '{d}', requester_name = '{e}' ,priority = '{f}', data_update = {h} , agent='{j}',module='{k}',organization_id={l} "
    sql = sql.format(b = params[1],d = params[3],e = params[4],f = params[5],h = params[7],j = params[9],k = params[10],l = params[11])
    cursor.execute( sql )

sql = "UPDATE quarterlytickets SET organization_name = org.organization_name FROM organizations org WHERE org.organization_id = quarterlytickets.organization_id"
cursor.execute( sql )

conn.commit()
cursor.close()
conn.close()
    