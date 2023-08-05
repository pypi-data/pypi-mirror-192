import requests
import re
import pandas as pd
from pymongo import MongoClient
from sodapy import Socrata
from bs4 import BeautifulSoup
import time
import urllib3


class Yuku:
    def __init__(self, mongo_db: str = "yuku", mongodb_uri: str = "mongodb://localhost:27017/", socrata_endpoint: str = "www.datos.gov.co"):
        """
        Contructor for Yuku, we only support open datasets, credentials are not supported.

        Parameters:
        ------------
        socrata_endpoint:str
            endpoint for socrata, default "www.datos.gov.co"
        """
        self.client = Socrata("www.datos.gov.co", None, timeout=120)
        self.mlient = MongoClient(mongodb_uri)
        self.db = self.mlient[mongo_db]
        self.socrata_endpoint = socrata_endpoint
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def download_cvlac(self, dataset_id: str):
        """
        Method to download cvlav information.
        This can take long time, but if something goes wrong we support checkpoint.

        Parameters:
        ------------
        dataset_id:str
            id for dataset in socrata ex: bqtm-4y2h
        """
        scienti_url = 'https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh='
        if "cvlac_dataset_info" in self.db.list_collection_names():
            print("WARNING: cvlac_dataset_info already in the database, it will be not downloaded again, drop the database if you want start over.")
        else:
            print(f"INFO: downloading dataset metadata from id {dataset_id}")
            dataset_info = self.client.get_metadata(dataset_id)
            self.db["cvlac_dataset_info"].insert_one(dataset_info)
        if "cvlac_data" in self.db.list_collection_names():
            print("WARNING: cvlac_data already in the database, it will be not downloaded again, drop the database if you want start over.")
        else:
            data = self.client.get_all(dataset_id)
            data = list(data)
            self.db["cvlac_data"].insert_many(data)
        cod_rh_data = self.db["cvlac_data"].distinct("id_persona_pr")
        cod_rh_stage = self.db["cvlac_stage"].distinct("id_persona_pr")
        # computing the remaining ids for scrapping
        cod_rh = set(cod_rh_data) - set(cod_rh_stage)
        cod_rh = list(cod_rh)
        print(f"INFO: found {len(cod_rh_data)} records in data\n      found {len(cod_rh_stage)} in stage\n      found {len(cod_rh)} remain records to download.")

        counter = 0
        count = len(cod_rh)
        for cvlac in cod_rh:
            if counter % 10 == 0:
                print(f"INFO: Downloaded {counter} of {count}")
            url = f'{scienti_url}{cvlac}'

            dd = {'id_persona_pr': cvlac}

            try:
                r = requests.get(url, verify=False)
            except Exception:
                continue

            if not r.text:
                continue

            soup = BeautifulSoup(r.text, 'lxml')  # Parse the HTML as a string
            tables = soup.find_all('table')

            # 1: Full names
            if len(tables) > 2:
                t = tables[1]
            else:
                dd['nombre'] = ''
                continue

            tr = pd.read_html(t.decode())[0].to_dict(orient='records')

            for d in tr:
                if d and isinstance(d.get(0), str) and isinstance(d.get(1), str):
                    dd[d.get(0)] = d.get(1).replace('\xa0', ' ')
                else:
                    continue

            # 2. Academic Social Networks  and authors Ids
            t = tables[2]

            # 2.a) Academic Social Networks (Google Scholar)
            next = 2
            try:
                ids = t.find_all('h3')[0].text
            except Exception:
                ids = ''
            if ids == 'Redes sociales académicas':
                next = 3
                ll = t.find_all('a')
                for x in ll:
                    try:
                        dd[x.text.split(' (')[0]] = x['href']
                    except Exception:
                        continue
            # 2.b) authors Ids (ORCID, Scopus, ...)
            try:
                t = tables[next]
            except Exception:
                continue

            try:
                ids = t.find_all('h3')[0].text
            except Exception:
                ids = ''
            if ids == 'Identificadores de autor':
                ll = t.find_all('a')
                for x in ll:
                    try:
                        dd[re.search('\(([\w]+)\)', x.text).groups()[0]] = x['href']  # noqa
                    except Exception:
                        continue
            self.db["cvlac_stage"].insert_one(dd)
            time.sleep(0.3)
            counter += 1
        print(f"INFO: Downloaded {counter} of {count}")

    def download_gruplac(self, dataset_id: str):
        """
        Method to download gruplac information.
        Unfortunately we dont have support for checkpoint in this method.

        Parameters:
        ------------
        dataset_id:str
            id for dataset in socrata ex: 33dq-ab5a
        """
        if "gruplac_dataset_info" in self.db.list_collection_names():
            print("WARNING: gruplac_dataset_info already in the database, it will be not downloaded again, drop the database if you want start over.")
        else:
            print(f"INFO: downloading dataset metadata from id {dataset_id}")
            dataset_info = self.client.get_metadata(dataset_id)
            self.db["gruplac_dataset_info"].insert_one(dataset_info)
        if "gruplac_data" in self.db.list_collection_names():
            print("WARNING: gruplac_data already in the database, it will be not downloaded again, drop the database if you want start over.")
        else:
            dataset = self.db["gruplac_dataset_info"].find_one()
            self.db["gruplac_data_cache"].drop()
            cursor = self.client.get_all(dataset_id)
            data = []
            count = int(dataset['columns'][0]['cachedContents']['count'])
            print(f"INFO: Total groups found = {count}.")
            counter = 1
            for i in cursor:
                if counter % 20000 == 0:
                    print(f"INFO: downloaded {counter} of {count}")
                    self.db["gruplac_data_cache"].insert_many(data)
                    data = []
                data.append(i)

                counter += 1

            self.db["gruplac_data_cache"].insert_many(data)
            print(f"INFO: downloaded {counter} of {count}")
            self.db["gruplac_data_cache"].rename("gruplac_data")

    def search(self, q: str, limit: int = 5):
        """
        Method to search datasets in socrata for the endpoint www.datos.gov.co

        examples:
        * q="Investigadores Reconocidos por convocatoria"
        * q="Producción Grupos Investigación"

        Parameters:
        -----------
        q:str
            Elastic search query, results of datasets are besed on similarity
        limit:int
            number of results to display, default firts 5 elements.
        """
        datasets = self.client.datasets(
            q=q, public=True)  # busca en elastic search con query "q"
        for dataset in datasets[0:limit]:
            print("name: ", dataset["resource"]["name"])
            print("id: ", dataset["resource"]["id"])
            print("description: ", dataset["resource"]["description"])
            print("attribution: ", dataset["resource"]["attribution"])
            print("attribution_link: ",
                  dataset["resource"]["attribution_link"])
            print("type: ", dataset["resource"]["type"])
            print("updatedAt: ", dataset["resource"]["updatedAt"])
            print("createdAt: ", dataset["resource"]["createdAt"])
            print('\n\n')
        return datasets[0:limit]
