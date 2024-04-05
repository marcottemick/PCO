from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
import re
import random
import pandas as pd
import time
import concurrent.futures
import openai
import os

class Generate_people:
    def __init__(self, sexe: int, number: int, titre: str, name_df: str) -> pd.DataFrame:
        self.sexe = sexe
        self.number = number
        self.titre = titre
        self.name_df = name_df
        self.fake = Faker('fr_FR')
        self.person = {}
        self.persons = []

    def generate_identitate(self) -> list:
        self.person = {}

        if self.sexe == 1:
            self.person['name'] = (self.titre + ' ' + self.fake.first_name_male() + ' ' +  self.fake.last_name_male()).strip()
        elif self.sexe == 2:
           self.person['name'] = (self.titre + ' ' +  self.fake.first_name_female() + ' ' +  self.fake.last_name_female()).strip()
        
        if self.titre == '':
            self.person['address'] = self.fake.address().replace('\n', ', ')
            self.person['birthday'] = self.fake.date_of_birth(minimum_age=16, maximum_age=90).strftime("%d/%m/%Y")
    
    def generate_nir(self) -> str:
        nir = []
        nir.append(str(self.sexe))
        annee_mois = self.person['birthday'].split('/')[1: 3]
        annee_mois.reverse()
        nir.extend(annee_mois)

        regex_code_postal = re.compile(r'\b\d{5}\b')
        code_postal = regex_code_postal.search(self.person['address'])
        nir.append(code_postal.group())

        nombre_aleatoire_1 = str(random.randint(1, 999)).zfill(3)
        nombre_aleatoire_2 = str(random.randint(1, 99)).zfill(2)

        nir.extend([nombre_aleatoire_1, nombre_aleatoire_2])

        self.person['nir'] = ' '.join(nir)

    def factory_people(self) -> list:
        for n in range(1, self.number + 1):
            self.generate_identitate()
            if self.titre == '':
                self.generate_nir()
            self.persons.append(self.person)

    def append_df(self) -> pd.DataFrame:
        df = pd.read_csv(f'{self.name_df}.csv', sep=';')
        new_df = pd.DataFrame(self.persons)
  
        df = pd.concat([df, new_df], ignore_index=True)
        if self.name_df == 'patients':
            df = df.drop_duplicates(subset= ['nir'])
        elif self.name_df == 'anatomopathologists':
            df = df.drop_duplicates(subset= ['name'])
            df['id_med'] = df.reset_index().index
        df.to_csv(f'{self.name_df}.csv', sep=';', index=False)

        return True

    def main(self) -> pd.DataFrame:
        self.factory_people()
        self.append_df()
        
        return True
    
class Generate_CRO:
    def __init__(self, datas_CRO, model, id_prompt) -> list:
        self.datas_CRO = datas_CRO
        self.texts = []
        self.model = model
        self.id_prompt = id_prompt

    def prompt(self, data_CRO):
        if self.id_prompt == 0:
            prompt = f"""Génère en français un compte opératoire d'anatomopathologie qui a pour titre : Compte rendu d'anatomopathologie. pour un cas de {data_CRO['diagnostic']['diagnostic']} en trois partie : description macroscopique, description microscopique, immunohistochimie et conclusion avec rappel des faits. Le diagnostic ne doit apparaitre que dans la conclusion. Spécifie en bas de page 'Note : ceci est un compte rendu fictif.' Compte en rendu en français."""
        elif self.id_prompt == 1:
            prompt = f"""Génère en français un compte opératoire d'anatomopathologie qui a pour titre : Compte rendu d'anatomopathologie. pour un diagnostic de {data_CRO['diagnostic']['diagnostic']} en trois partie : description macroscopique, description microscopique, immunohistochimie et conclusion avec rappel des observations. Le diagnostic ne doit apparaitre que dans la conclusion. Spécifie en bas de page 'Note : ceci est un compte rendu fictif.' Compte en rendu en français."""
        elif self.id_prompt == 2:
            prompt = f"""Génère en français un compte opératoire d'anatomopathologie qui a pour titre : Compte rendu d'anatomopathologie. pour un cas de {data_CRO['diagnostic']['diagnostic']} sur une {data_CRO['diagnostic']['opération']} en trois partie : description macroscopique, description microscopique, immunohistochimie et conclusion avec rappel des preuves. Le diagnostic ne doit apparaitre que dans la conclusion. Spécifie en bas de page 'Note : ceci est un compte rendu fictif.' Compte en rendu en français."""
        elif self.id_prompt == 3:
            prompt = f"""Génère en français un compte opératoire d'anatomopathologie qui a pour titre : Compte rendu d'anatomopathologie. pour un diagnostic de {data_CRO['diagnostic']['diagnostic']} sur une {data_CRO['diagnostic']['opération']} en trois partie : description macroscopique, description microscopique, immunohistochimie et conclusion avec rappel des observations. Le diagnostic ne doit apparaitre que dans la conclusion. Spécifie en bas de page 'Note : ceci est un compte rendu fictif.' Compte en rendu en français."""

        return prompt

    def huggingChat_CRO(self, data_CRO) -> str:
        driver = webdriver.Chrome()
        driver.get(f'https://huggingface.co/chat?model={self.model}')

        try: 
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/button').click()
        except:
            pass

        time.sleep(1)
        prompt = self.prompt(data_CRO)
        print(prompt)
        driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div/form/div/div/textarea').send_keys(prompt)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div/form/div/button').click()
        time.sleep(10)  
        
        verif_text = True  
        while verif_text:
            
            div_text_pred = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div/div[2]/div[1]')
            CRO_pred = div_text_pred.text
  
            time.sleep(2)

            div_text_next = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div/div[2]/div[1]')
            CRO_next = div_text_next.text
    
            if len(CRO_pred) == len(CRO_next):                
                CRO = CRO_next
                print(CRO, '\n')
                verif_text = False
                
        time.sleep(2)
        self.text_append(CRO, data_CRO, self.model)
        driver.quit()   

    def API_chatGPT(self):
        for data_CRO in self.datas_CRO:
            prompt = self.prompt(data_CRO)
            openai.api_key = os.environ.get('KEY_API_CHATGPT')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", 
                     "content": prompt}      
                ]
            )

            CRO = response['choices'][0]['message']['content']
            self.text_append(CRO, data_CRO, self.model)
   
    def multithreading(self, nb_worker: int = 1):
        with concurrent.futures.ThreadPoolExecutor(max_workers=nb_worker) as executor:
            executor.map(self.huggingChat_CRO, self.datas_CRO)
    
    def input(self):
        for data_CRO in self.datas_CRO:
            print(self.prompt(data_CRO))
            CRO = input()
            CRO = CRO.replace('  ', '\n')
            self.text_append(CRO, data_CRO, self.model)
    
    def text_append(self, CRO, data_CRO, source):
        self.texts.append({
            'CRO': CRO,            
            'id_diag': data_CRO['diagnostic']['id_diag'],
            'id_med': data_CRO['med']['id_med'],
            'nir': data_CRO['patient']['nir'],
            'source': source,
            'operation': data_CRO['diagnostic']['opération']
            })
        
    def append_CRO(self, file):
        df_cro = pd.read_csv(file, sep=';')
        new_cro = pd.DataFrame(self.texts)
        print(new_cro)
        df_cro = pd.concat([df_cro, new_cro], ignore_index=True)
        df_cro.to_csv(file, sep=';', index=False) 
        
    
class Select_line:
    """
    niv_1: nombre de liste dans la première boucle
    niv_2: nombre de valeur dans la deuxième boucle
    type_op: all (valeur par défaut), biopsie, exérèse
    """
    def __init__(self, niv_1: int, niv_2: int, type_op:str = 'all') -> list:
        self.datas_CRO_niv_1 = []
        self.datas_CRO_niv_2 = []
        self.data_CRO = {}
        self.niv_1 = niv_1
        self.niv_2 = niv_2
        self.type_op = type_op

    def open_datas(self) -> pd.DataFrame:
        self.patients = pd.read_csv(r"G:\Mon Drive\PCO\data\patients.csv", sep=';', dtype= str)
        self.meds = pd.read_csv(r"G:\Mon Drive\PCO\data\anatomopathologists.csv", sep=";", dtype= str)
        self.diagnostics = pd.read_csv(r"G:\Mon Drive\PCO\data\diagnostics_v2.csv", sep=';', dtype= str)

        self.diagnostics = self.diagnostics.query('generation == "1"')

        self.index_patients = self.patients.index.tolist()        
        self.index_meds = self.meds.index.tolist()        
        self.index_diags = self.diagnostics.index.tolist()

    def select_patients(self, id_patient) -> list:
        self.data_patient = self.patients.loc[id_patient]
        self.data_patient = self.data_patient.to_dict()
        self.data_patient['num_secu_social'] = self.data_patient['nir']

        self.data_CRO['patient'] = self.data_patient
      
    def select_med(self, id_med) -> list:
        self.data_med = self.meds.loc[id_med]
        self.data_med = self.data_med.to_dict()

        self.data_CRO['med'] = self.data_med

    def type_operation(self) -> list:
        valeur_debut = 0
        valeur_fin = 1
        if self.type_op == 'biopsie':
            valeur_fin = 0
        elif self.type_op == 'exérèse':
            valeur_debut = 1

        random_operation = random.randint(valeur_debut, valeur_fin)        
        if random_operation == 0:
            self.data_diagnostic['opération'] = 'biopsie'
        else:          
            self.data_diagnostic['opération'] = 'exérèse'

    def select_diagnostic(self, id_diagnostic) -> list:
        self.data_diagnostic = self.diagnostics.loc[id_diagnostic]
        self.data_diagnostic = self.data_diagnostic.to_dict()
        self.type_operation()

        self.data_CRO['diagnostic'] = self.data_diagnostic

    def generate_liste_niv_1_niv_2(self, index):
        total_select = self.niv_1 * self.niv_2

        nb_dupli = total_select // len(index)
        liste_dupli = index * nb_dupli
        manque = total_select - len(liste_dupli)
        liste_manque = random.sample(index, manque)
        liste_dupli += liste_manque
        random.shuffle(liste_dupli)
        niv_1 = [liste_dupli[i:i+self.niv_2] for i in range(0, len(liste_dupli), self.niv_2)]

        return niv_1

    def main(self) -> list:
        self.open_datas()

        niv_1_patients = self.generate_liste_niv_1_niv_2(self.index_patients)
        niv_1_meds = self.generate_liste_niv_1_niv_2(self.index_meds)
        niv_1_diags = self.generate_liste_niv_1_niv_2(self.index_diags)

        for niv_1 in range(0, self.niv_1):  
            for niv_2 in range(0, self.niv_2):                          
                self.select_patients(niv_1_patients[niv_1][niv_2])
                self.select_med(niv_1_meds[niv_1][niv_2])
                self.select_diagnostic(niv_1_diags[niv_1][niv_2])
                self.datas_CRO_niv_2.append(self.data_CRO)
                self.data_CRO = {}

            self.datas_CRO_niv_1.append(self.datas_CRO_niv_2)
            self.datas_CRO_niv_2 = []

        return self.datas_CRO_niv_1


    