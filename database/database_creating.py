import psycopg2


def connect(db_name, db_user, db_password, db_host, db_port):
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    return connection


class CreateDB:
    def __init__(self, db_name, db_user, db_password, db_host='localhost', db_port=5432):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def create(self):
        with connect(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE employees 
                               (
                               employer_id serial PRIMARY KEY,
                               employer_name varchar(150)
                               );

                               CREATE TABLE vacancies (
                               id_vacancy serial PRIMARY KEY,
                               vacancy varchar(150),
                               salary integer,
                               employer_id integer REFERENCES employees(employer_id),
                               description text,
                               link varchar(150)
                               );""")
            print('Таблицы созданы')
        connection.close()
