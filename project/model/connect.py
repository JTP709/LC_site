from sqlalchemy import create_engine

# Update the user and password for your database
user = 'owner'
password ='owner'
database = 'l_blog'

def connect(user=user,
            password=password,
            db=database,
            host='localhost',
            port=5432):
    """Returns a connection and a metadata object"""
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = create_engine(url, client_encoding='utf8')
    return con
