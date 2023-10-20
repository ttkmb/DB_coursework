from database.database_functions import DBManager
from database.database_creating import CreateDB

user_password = input('Enter password: ')
db = CreateDB('coursework', 'postgres', f'{user_password}')
if db.create():
    print('Таблицы успешно созданы')
DBManager(user_password).add_data_to_db()
while True:
    user_input = input(
        'Введите 1 чтобы показать компании и количество вакансий у каждой компании\n'
        'Введите 2 чтобы показать все вакансии с указанием названия компании, названия вакансии и зарплаты и '
        'ссылки на вакансию.\n'
        'Введите 3 чтобы показать среднюю зарплату по вакансиям.\n'
        'Введите 4 чтобы показать список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
        'Введите 5 чтобы показать список всех вакансий, в названии которых содержатся переданные слова.\n'
        'Введите 6 для выхода\n')
    if user_input == '6':
        break
    elif user_input == '1':
        print(DBManager(user_password).get_companies_and_vacancies_count())
    elif user_input == '2':
        print(DBManager(user_password).get_all_vacancies())
    elif user_input == '3':
        print(DBManager(user_password).get_avg_salary())
    elif user_input == '4':
        print(DBManager(user_password).get_vacancies_with_higher_salary())
    elif user_input == '5':
        user_keyword = input('Enter keyword: ')
        print(DBManager(user_password).get_vacancies_with_keyword(f'{user_keyword}'))
