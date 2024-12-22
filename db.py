import sqlalchemy


def mysql_connect():
    user = 'root'
    password = 'root'
    host = '127.0.0.1'
    #host = 'host.docker.internal'
    port = 3306
    database = 'glpi'

    return sqlalchemy.create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def postgresql_connect():
    user = "postgres"
    password = "12340987"
    host = "localhost"
    port = 5432
    database = "postgres"

    return sqlalchemy.create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )