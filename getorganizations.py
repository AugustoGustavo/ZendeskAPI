from zenpy import Zenpy
import tokens
from dbconn import dbconn

# Create a Zenpy instance
zenpy_client = Zenpy(domain="zendesk.com",subdomain=tokens.__logos_subdomain__,email=tokens.__logos_mail__,token=tokens.__logos_zendesk__)

# Get a psql connection
conn = dbconn.connect( dbconn.config() )
cursor = conn.cursor()

# Get a view content
## content = zenpy_client.views.execute(view=tokens.__view_quarterlytickets__)
content = zenpy_client.organizations()

# Perform a simple for
for i in range(content.count):

    row = content.next()

    values = " "

    values = str(row.id) + ", " 
    values = values + "'" + row.name + "' "

    #execute sql command
    sql = "INSERT INTO organizations VALUES({values})".format(values = values)
    cursor.execute( sql )

conn.commit()
cursor.close()
conn.close()
    