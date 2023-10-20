import json


import psycopg2
from utils.API import HeadHunterApi


class DBManager:
    def __init__(self, password):
        self.password = password
        self.conn = psycopg2.connect(
            database='coursework',
            user='postgres',
            password=f'{self.password}',
            host='localhost',
            port=5432
        )
        self.cur = self.conn.cursor()

    def add_data_to_db(self):
        """
        Добавляет данные в базу данных
        """

        with open('../DB_coursework/employers.json', 'r') as f:
            data = json.load(f)

        for key, value in data.items():
            self.cur.execute("INSERT INTO employees VALUES (%s, %s)", (key, value))
            self.conn.commit()

            api = HeadHunterApi(key)
            vacancies = []

            query = ('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)'
                     'ON CONFLICT (id_vacancy) DO NOTHING')

            for vacancy in api.get_vacancies():
                vacancies.append(
                    (vacancy['id'], vacancy['name'], vacancy['salary']['from'] if vacancy['salary'] else None,
                     vacancy['employer']['id'], vacancy['snippet']['responsibility'],
                     vacancy['alternate_url']))
                self.cur.executemany(query, vacancies)
                self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        self.cur.execute('SELECT employer_name, COUNT(id_vacancy) '
                         'FROM employees '
                         ''
                         'JOIN vacancies using(employer_id) '
                         'GROUP BY employer_name')
        rows = self.cur.fetchall()
        for row in rows:
            company = row[0]
            count = row[1]
            print(f"{company} - {count}")

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cur.execute("""
                        select employer_name, vacancies.vacancy, vacancies.salary, vacancies.link 
                        from employees
                        join vacancies using(employer_id)
        """)
        for vacancy in self.cur.fetchall():
            print(vacancy)

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        self.cur.execute("SELECT AVG(salary) FROM vacancies")
        return round(self.cur.fetchone()[0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        self.cur.execute("""
                        select * 
                        from vacancies
                        where salary > (select AVG(salary) from vacancies)
        """)
        for vacancy in self.cur.fetchall():
            print(vacancy)

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        self.cur.execute(f"""
                        select * 
                        from vacancies
                        where vacancy like '%{keyword}%'
                        """)
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
