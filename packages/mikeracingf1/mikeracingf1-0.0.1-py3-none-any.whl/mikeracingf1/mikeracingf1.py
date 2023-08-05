import requests


class MikeRacingF1:
    def __init__(self):
        self.url = "https://api.f1stats.io/v1.0/api/"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

    def get_circuits(self, year):
        url = f"{self.base_url}circuits"
        params = {"token": self.token, "year": year}
        response = requests.get(url, params=params)
        return response.json()

    def get_constructor_results(self, year):
        url = f"{self.base_url}constructorresults"
        params = {"token": self.token, "year": year}
        response = requests.get(url, params=params)
        return response.json()

    def get_constructor_list(self):
        url = f"{self.base_url}constructors"
        params = {"token": self.token}
        response = requests.get(url, params=params)
        return response.json()

    def get_constructorstandings(self):
        url = f"{self.base_url}constructorstandings"
        params = {"token": self.token}
        response = requests.get(url, params=params)
        return response.json()

    def get_driversinfo(self,year):
        url = f"{self.base_url}driversinfo"
        params = {"token": self.token, "year": year}
        response = requests.get(url, params=params)
        return response.json()

    def get_driverstandings(self,year):
        url = f"{self.base_url}driverstandings"
        params = {"token": self.token, "year": year}
        response = requests.get(url, params=params)
        return response.json()

    def get_races(self,year):
        url = f"{self.base_url}races"
        params = {"token": self.token, "year": year}
        response = requests.get(url, params=params)
        return response.json()


    def get_results(self, year,round):
        url = f"{self.base_url}results"
        params = {"token": self.token, "year": year, "round": round}
        response = requests.get(url, params=params)
        return response.json()



