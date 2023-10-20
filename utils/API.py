from abc import abstractmethod, ABC

import requests
import concurrent.futures


class ApiWorker(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterApi(ApiWorker):
    def __init__(self, employer_id):
        self.employer_id = employer_id

    def get_vacancies(self):
        vacancies = []
        params = {
            'per_page': 10,
            'page': 0,
            'area': 113
        }

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for page in range(params['per_page']):
                url = f'https://api.hh.ru/vacancies?employer_id={self.employer_id}'
                future = executor.submit(self.fetch_vacancies, url, params)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                vacancies += response['items']

        return vacancies

    @staticmethod
    def fetch_vacancies(url, params):
        response = requests.get(url, params=params)
        return response.json()
