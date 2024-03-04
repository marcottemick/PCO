from flask import Flask, jsonify, request, render_template
import pandas as pd
import spacy
import utils
import flask_monitoringdashboard as dashboard

app = Flask(__name__)
# https://medium.com/flask-monitoringdashboard-turtorial/monitor-your-flask-web-application-automatically-with-flask-monitoring-dashboard-d8990676ce83
dashboard.config.init_from(file='\config.cfg')
dashboard.bind(app)

@app.route('/test', methods=['GET'])
def get_test():
    response = {'response': 'connection au serveur'}
    return jsonify(response)

@app.route('/login', methods= ['PUT'])
def put_login() -> dict:
    '''
    envoie le rôle de celui qui tente de se logger
    -entrée : login(str) et password(str)
    -sortie : le numéro du rôle (int), envoie 0 si la personne n'est pas identifiée
    '''
    try:
        req = request.json
        login = req.get('id')
        password = req.get('password')

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT id_role FROM logins WHERE login = "{login}" and password = "{password}";''')
        response_role = cursor.fetchone()

        if response_role is None:
            role = 0
        else:
            role = response_role[0]

        response = {'role': role}
        return jsonify(response)

    except Exception as e:
        print(e)
        utils.send_mail('endpoint predict', e)

@app.route('/logins', methods= ['GET'])
def get_logins():
    '''
    envoie toutes les utilisateurs avec leurs logins,password et rôle
    entrée: null
    sortie: liste d'utilisateurs avec login, password, rôle et id de l'utilisateur(int)
    '''
    try:
        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT * FROM logins 
                       JOIN role USING (id_role);''')
        df_logins = cursor.fetchall()

        columns=[i[0] for i in cursor.description]
        cursor.close()

        df_logins = pd.DataFrame(df_logins, columns= columns, dtype=str)
        df_logins = df_logins.drop(['id_role','description'], axis=1)
        logins = df_logins.values.tolist()

        response = {
            'logins': logins
            }
        return jsonify(response)
    except Exception as e:
        print(e)
        utils.send_mail('endpoint predict', e)

@app.route('/deleteLogin', methods=['PUT'])
def delete_login():
    '''
    suppresion d'un utilisateur
    entrée: id(int)
    sortie : boolean
    '''
    try:
        req = request.json
        id = req.get('id')

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''DELETE FROM logins WHERE id={id};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        response = {'response': True}
        return jsonify(response)

    except Exception as e:
        print(e)
        utils.send_mail('endpoint predict', e)

@app.route('/ajoutLogin', methods=['POST'])
def post_login() -> dict:
    '''
    ajoute un nouvel identifiant
    entrée: login(str)/password(str)/role(int)
    sortie: boolean
    '''
    try:
        req = request.json
        login = req.get('login')
        password = req.get('password')
        role = req.get('role')

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''INSERT INTO logins (login, password, id_role)
                       VALUES("{login}", "{password}", {int(role)});''')
        bdd.commit()
        cursor.close()
        bdd.close()

        response = {'response': True}
        return jsonify(response)

    except Exception as e:
        print(e)
        utils.send_mail('endpoint predict', e)

@app.route('/predict', methods=['PUT'])
def put_predict() -> dict:
    '''
    envoie de la prédiction
    -entrée: CRO (str)
    -sortie: dictionnaire de prédiction
    '''
    try:
        req = request.json
        CRO = req.get('CRO')
        CRO= CRO.lower()

        nlp = spacy.load(r"C:\PCO\generate_model\training\model-best")
        doc = nlp(CRO)

        predict = {}

        for ent in doc.ents:
            ner = ent.text.strip()
            if ent.label_ == 'PER' and 'dr ' in ner:
                if 'DOC' in predict.keys():
                    if ent.text not in predict['DOC']:                    
                        predict['DOC'].append(ner)
                else:
                    predict['DOC'] = [ner]       
            elif ent.label_ in predict.keys():
                if ent.text not in predict[ent.label_]:
                    predict[ent.label_].append(ner)
            else:
                predict[ent.label_] = [ner]           

        if len(predict.keys()) > 0:
            response = {'response': True,           
                        'predict': predict}
            return jsonify(response)
        else:
            response = {'response': False}
    
    except Exception as e:
        print(e)
        utils.send_mail('endpoint predict', e)

@app.route('/patients', methods=['GET'])
def get_patients() -> dict:
    '''
    envoie de l'ensemble des patients présent dans la base de donnée
    -entrée: null
    -sortie: list de patients
    '''
    try:
        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT name FROM patients;''')
        df_patients = cursor.fetchall()

        columns=[i[0] for i in cursor.description]
        cursor.close()

        df_patients = pd.DataFrame(df_patients, columns= columns, dtype=str)
        df_patients = df_patients.sort_values(by=['name'])
        patients_list = df_patients.name.values.tolist()

        response = {'patients': patients_list}
        return jsonify(response)
    
    except Exception as e:
        print(e)
        utils.send_mail('endpoint patients', e)

@app.route('/antecedents', methods=['GET'])
def get_antecedents() -> dict:
    """
    envoie les antécédents de chaque patient ou un antécédent d'un patient
    -entrée: patient (str) -> optionnel
    -sortie: dictionnaire des données personnels de chaque patient, antécédent sous forme de list
    """
    try:
        patient = request.args.get('patient')

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT CRO.id_CRO, CRO.nir, CRO.id_diag, 
                    diagnostics.id_diag, diagnostic,
                    address, birthday, name, nir
                    FROM CRO 
                    JOIN patients USING (nir) 
                    JOIN diagnostics USING (id_diag) {"WHERE name = '" + patient + "'" if patient != "" else ""};''')
        df_antecedents = cursor.fetchall()    

        columns=[i[0] for i in cursor.description]
        cursor.close()

        df_antecedents = pd.DataFrame(df_antecedents, columns= columns, dtype=str)
        
        if len(df_antecedents) != 0:
            # supprime les colonnes en double
            df_antecedents = df_antecedents.loc[:,~df_antecedents.columns.duplicated()]
            # ne conserve que les cinq premier diagnostics de chaque patient
            df_antecedents = df_antecedents.groupby('name', group_keys=False).apply(utils.garder_cinq_premieres_occurrences)

            colonnes = df_antecedents.columns.tolist()
            colonnes.remove('id_CRO')
            colonnes.remove('diagnostic')
            colonnes.remove('id_diag')

            df_antecedents['dict_CRO_diag'] = df_antecedents.apply(lambda row: {row['diagnostic']: row['id_CRO']}, axis=1)

            df_antecedents_groupby = df_antecedents.groupby(colonnes, as_index=True).agg(
                {'dict_CRO_diag': list}
                ).reset_index()
            df_antecedents_groupby = df_antecedents_groupby.sort_values(by=['name'])
            df_antecedents_dict = df_antecedents_groupby.to_dict(orient='records')
            
            response = {
                'response': True,
                'antecedents': df_antecedents_dict}
            return jsonify(response)

        else:
            response = {
                'response': False
                }
            return jsonify(response)
        
    except Exception as e:
        print(e)
        utils.send_mail('endpoint antecedents', e)

@app.route('/CRO', methods=['GET'])
def get_read_CRO() -> dict:
    '''
    envoie le CRO et les détails associé à un id (diagnostic)
    -entrée: id du CRO (str -> int)
    -sortie: dictionnaire rassemblant le CRO & les données extraites
    '''
    
    try:
        id_CRO = request.args.get('id_CRO')

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT * FROM CRO
                    JOIN patients USING (nir)
                    JOIN diagnostics USING (id_diag)
                    JOIN anatomopathologists USING (id_med)
                    WHERE id_CRO = {int(id_CRO)};''')
        datas_CRO = cursor.fetchall()    

        columns=[i[0] for i in cursor.description]
        columns[7] = 'name_patient'
        columns[13] = 'name_med'

        cursor.close()

        datas_CRO = pd.DataFrame(datas_CRO, columns= columns, dtype=str)
        datas_CRO = datas_CRO.drop(['id_med', 'id_diag', 'cancer', 'organe', 'operation'], axis = 1)
        datas_CRO_response = datas_CRO.to_dict(orient='records')

        response = {'detailCRO': datas_CRO_response[0]}
        return jsonify(response)
    
    except Exception as e:
        print(e)
        utils.send_mail('endpoint CRO', e)

@app.route('/metriques', methods=['GET'])
def get_metriques():
    '''
    envoie des métriques d'entaînement
    entrée: null
    sortie: dictionnaire des différentes métriques
    '''
    try:
        metrics = pd.read_csv(r'C:\PCO\generate_model\metrics_df.csv', sep=';')
        metrics = metrics.drop(['NER', 'dataset', 'hyperparamètres'], axis=1)
        metrics_list = metrics.to_dict(orient='list')

        response = {'response': metrics_list}
        return jsonify(response)
    
    except Exception as e:
        print(e)
        utils.send_mail('endpoint metriques', e)

if __name__ == '__main__':
    app.run(debug=True, port=5000)