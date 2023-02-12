import configparser
import pg8000

class dbconn:

    def __init__():
        
        dbconn.__conn = None


    def config(filename='database.ini' , section = 'postgresql'):

        # create a parser
        parser = configparser.ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db


    def connect(dbparams):

        # Connect to your postgres DB        
        dbconn.__conn = pg8000.connect(dbparams['user'],dbparams['host'],dbparams['database'],dbparams['port'],dbparams['password'])

        return dbconn.__conn 
    

    def close():

        # close connection
        dbconn.__conn.close()

    
