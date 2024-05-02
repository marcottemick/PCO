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
        data = {'CRO': """Titre : Compte rendu d'anatomopathologie
                Patient : Marguerite Derose
                Date de naissance : 15/01/1963
                Adresse : 349, boulevard de Jacques, 21813 Legendre
                Numéro de sécurité social : 2 1963 01 21813 466 39
                Présentation :
                Cet examen anatomopathologique porte sur une masse gastrointestinale externe, retirée chirurgicalement chez un patient de 45 ans.
                Description macroscopique :
                Lors de l'examen initial, nous avons constaté une masse sphérique bien délimitée, mesurant environ 3 cm de diamètre. Sa surface était polypoïde et couverte d'une muqueuse intestinale normale. La capsule du tumorama présentait adhérences minimes à la paroi abdominale. L'aspect cutáné était homogène et non inflammatoire. Aucune ulcération ou hémorrhagie n'était observée.
                Description microscopique :
                L'étude histologique révélait une formation composée majoritairement de tissus conjonctifs matures, intercalées entre des structures glandulaires tubulo-aciniques. Ces dernières présentaient des cellules cubiques à pyramidales, disposées autour de canaux centraux dilatés. Des zones myxoïdes étaient également identifiables. Les mitoses étaient rares et les atypies nucléaires minimales. Les limites du carcinome squirrheux étaient nettes et il n'y avait pas d'infiltration peridermique ni intramurales.
                Immunohistochimie :
                Les cellules épithéliales ont été positives pour le CK7 et CK20, confirmant leur origine entéro-épitheliale. Les cellules myoide ont été positivement marquées par SMA (Smooth Muscle Actin) et des fibroblasts ont montré une expression faible de viment et des fibrilles de collagène type I sont visibles.
                Conclusion :
                Dans cette observation, nous retrouvons tous les critères morphologiques caractéristiques d'un carcinome squirrheux. Ce dernier est constitué d'un assemblage disproportionné de tissus conjonctifs et d'éléments glandulaires entéro-épithéliaux. Son aspect histologique et immunohistochimique conforte ce diagnose.
                Signature : Dr Agile Strong, anatomopathologiste"""}
        response = self.app.put('/predict', data=json.dumps(data), content_type='application/json')

        # Vérifiez le code de statut
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text= True))
        response_true = {'predict': {
                             'DOC':  ['Dr Agile Strong'], 
                             'PER':  ['Marguerite Derose'], 
                             'DATE': ['15/01/1963'], 
                             'LOC':  ['349, boulevard de Jacques, 21813 Legendre'],
                             'NIR':  ['2 1963 01 21813 466 39'],
                             'DIAG': ['carcinome squirrheux']},
                         'response': True}
        
        self.assertEqual(response_data['response'], response_true['response'])
        self.assertEqual(response_data['predict'], response_true['predict'])

    def test_patients(self):
        response = self.app.get('patients')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(data['patients']) != 0, True)
    
    def test_antecedent_true(self):
        param = {'patient': 'Adrien Pages'}
        response = self.app.get('antecedents', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        response_true = [{'address': '637, avenue Théophile Pelletier, 24660 Sainte Alfred', 
                        'birthday': '09/02/1968', 
                        'dict_CRO_diag': [{'mélanome': '1730'}, {'rosacée': '1744'}, {'rosacée': '1761'}, 
                        {'maladie de Duhring-Brocq': '1871'}, {'sarcome à cellules fusiformes de Kaposi': '1880'}], 
                        'name': 'Adrien Pages', 
                        'nir': '1 1968 02 24660 427 60'}]
        expected_response = {'antecedents': response_true, 'response': True}
        self.assertEqual(response_data, expected_response)

    def test_antecedent_false(self):
        param = {'patient': 'Bertrand Pinto'}
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

        response_true = {'nir': '2 1994 11 19795 060 32'}

        expected_response = {'detailCRO': response_true}
        self.assertEqual(response_data['detailCRO']['nir'], expected_response['detailCRO']['nir'])

if __name__ == '__main__':
    unittest.main(verbosity= 2)