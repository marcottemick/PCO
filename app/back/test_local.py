import unittest
import json
from server import app

text = """Titre : Compte rendu d'anatomopathologie
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
                Signature : Dr Agile Strong, anatomopathologiste"""

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
        data = {'CRO': text,
                "id_user": 3}
        response = self.app.put('/predict', data=json.dumps(data), content_type='application/json')

        # Vérifiez le code de statut
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.get_data(as_text= True))
       
        response_keys = ['predict', 'response']
        response_predict_keys = ['DOC', 'PER', 'DATE', 'LOC', 'NIR', 'DIAG']

        for key in response_keys:
            self.assertIn(key, response_data)
        for key in response_predict_keys:
            self.assertIn(key, response_data['predict'])

    def test_patients(self):
        response = self.app.get('patients')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(len(data['patients']) != 0, True)
    
    def test_antecedent(self):
        param = {'patient': 'Adrien Pages'}
        response = self.app.get('antecedents', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response_data['response'], True)
   
    def test_get_CRO(self):
        param = {'id_CRO': "0"}
        response = self.app.get('CRO', query_string=param)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response_data['response'], True)

if __name__ == '__main__':
    unittest.main(verbosity= 2)