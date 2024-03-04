import unittest
import json
from server import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.maxDiff = None

    def test(self):
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['response'], 'connection au serveur')
    
    def test_predict_CRO(self):
        data = {'CRO': """Compte rendu d'histopathologie
                        Dr Valentine Bousquet, anatomopathologiste
                        Patient : Bertrand Pinto
                        Naissance : 23/05/1940
                        Adresse : 974, chemin Lacombe, 08761 Sainte-Luc
                        Numéro de sécurité sociale : 1 1940 05 08761 487 82
                        Objet : Examen histopathologique de la taille du côlon récupérée lors d'une colectomie
                        Résumé :
                        Nous avons procédé à l'examen histopathologique de la taille du côlon récupérée lors d'une colectomie effectuée chez le patient Bertrand Pinto, âgé de 82 ans, ayant une adresse à Sainte-Luc. L'examen a été réaliser suite à des symptômes digestifs importants et à une masse palpable au niveau abdominal.
                        Description macroscopique :
                        La pièce opératoire est une taille de côlon mesurant environ 10 cm de long sur 5 cm de largeur et 3 cm d'épaisseur. Elle présente une surface externe régulière, sans ulcération ni déformation apparente. La couleur est blanche jaunâtre avec des zones plus ou moins rosâtres.
                        Description microscopique :
                        Après préparation et coloration, les coupes histologiques ont montré une structure tubulaire épithéliale rectale avec des cellules caliciformes et des cellules columnaires. Les cellules sont bien différenciées, mais on observe une légère augmentation de la taille nucléaire et une hyperplasie modeste des cryptes. Il n'y a pas de signes de dysplasie ou de cancer.
                        Diagnostic :
                        En raison de la présence d'une masse palpable au niveau abdominal et de la taille de la taille du côlon, nous avons diagnostiqué un lipome bénin du côlon. Ce type de tumefaction est couramment rencontré dans cette région et est généralement bénin.
                        Conclusion :
                        Le patient Bertrand Pinto souffre d'un lipome bénin du côlon. Nous recommandons une surveillance régulière pour évaluer l'évolution de cette affection et prendre en charge rapidement tout signe de complication ou de transformation maligne.
                        Signature :
                        Dr Valentine Bousquet, anatomopathologiste
                        Date : 23/02/2023"""}
        response = self.app.put('/predict', data=json.dumps(data), content_type='application/json')

        # Vérifiez le code de statut
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text= True))
        response_true = {'predict': {
                             'DOC': ['dr valentine bousquet'], 
                             'PER': ['bertrand pinto'], 
                             'DATE': ['23/05/1940', '23/02/2023'], 
                             'LOC': ['974, chemin lacombe, 08761 sainte-luc'], 
                             'DIAG': ['lipome']},
                         'response': True}
        
        self.assertEqual(response_data['response'], response_true['response'])
        self.assertEqual(response_data['predict'], response_true['predict'])

    def test_patients(self):
        response = self.app.get('patients')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(data['patients']), 400)
    
    def test_antecedent_true(self):
        param = {'patient': 'Adrien Pages'}
        response = self.app.get('antecedents', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        response_true = [{'nir': '1 1968 02 24660 427 60', 
                          'address': '637, avenue Théophile Pelletier, 24660 Sainte Alfred', 
                          'birthday': '09/02/1968', 
                          'name': 'Adrien Pages', 
                          'dict_CRO_diag': [{'granulome annulaire': '36'}, 
                                            {'granulome annulaire': '42'}, 
                                            {'dermatite herpétiforme': '86'}, 
                                            {'syndrome de polypose juvénile': '128'}, 
                                            {'syndrome de Lynch': '195'}]}]
        expected_response = {'antecedents': response_true, 'response': True}
        self.assertEqual(response_data, expected_response)

    def test_antecedent_false(self):
        param = {'patient': 'Adrien Guyon'}
        response = self.app.get('antecedents', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        expected_response = {'response': False}
        self.assertEqual(response_data, expected_response)
    
    def test_get_CRO(self):
        param = {'id_CRO': '1843'}
        response = self.app.get('CRO', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        response_true = {'nir': '1 1968 02 24660 427 60'}

        expected_response = {'detailCRO': response_true}
        self.assertEqual(response_data['detailCRO']['nir'], expected_response['detailCRO']['nir'])

if __name__ == '__main__':
    unittest.main()