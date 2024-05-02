from flask import Flask, jsonify, request
import pandas as pd
import spacy
import utils
import flask_monitoringdashboard as dashboard
import re

app = Flask(__name__)
# https://medium.com/flask-monitoringdashboard-turtorial/monitor-your-flask-web-application-automatically-with-flask-monitoring-dashboard-d8990676ce83

dashboard.config.init_from(file='\config.cfg')

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

        cursor.execute(f'''SELECT id_role, id FROM logins 
                       WHERE login = "{login}" and password = "{password}";''')
        response_role = cursor.fetchone()

        if response_role is None:
            role = 0
            id = 0
        else:
            role = response_role[0]
            id = response_role[1]


        response = {'role': role, 'id': id}
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

        cursor.execute(f'''SELECT * FROM logins JOIN role USING (id_role);''')
        df_logins = cursor.fetchall()

        columns=[i[0] for i in cursor.description]
        cursor.close()

        df_logins = pd.DataFrame(df_logins, columns= columns, dtype=str)
        df_logins = df_logins.drop(['description'], axis=1)
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

        print(id)

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''DELETE FROM logins WHERE id={int(id)};''')
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
    # try:
    req = request.json
    CRO = req.get('CRO')
    id_user = req.get('id_user')

    bdd = utils.get_db_connection()
    cursor = bdd.cursor()

    nlp = spacy.load(r"G:\Mon Drive\PCO\generate_model\training\model-best")
    doc = nlp(CRO)

    predict = {}

    for ent in doc.ents:
        ner = ent.text.strip()          
        if ent.label_ in predict.keys():
            if ent.text not in predict[ent.label_]:
                predict[ent.label_].append(ner)
        else:
            predict[ent.label_] = [ner]  

    patient = re.search(r"Patient : (.+?)\n", CRO)
    birthday = re.search(r"Date de naissance : (.+?)\n", CRO)
    address = re.search(r"Adresse : (.+?)\n", CRO)
    nir_find = re.search(r"Numéro de sécurité social : (.+?)\n", CRO)
    doc = re.search(r"Signature : (.+?), anatomopathologiste", CRO)

    id_doc = -1
    nir = -1

    if patient is not None:
        patient_extract = patient.group(1).strip()
        predict['PER'] = [patient_extract]
    if birthday is not None:
        birthday_extract = birthday.group(1).strip()
        predict['DATE'] = [birthday_extract]
    if address is not None:
        address_extract = address.group(1).strip()
        predict['LOC'] = [address_extract]
    if doc is not None:
        doc_extract = doc.group(1).strip()
        predict['DOC'] = [doc_extract]

        cursor.execute(f'SELECT * FROM anatomopathologists;')
        docs_in_bdd = cursor.fetchall()
        columns=[i[0] for i in cursor.description]
        docs_df = pd.DataFrame(docs_in_bdd, columns= columns, dtype=str)
        doc_in_bdd = docs_df.query(f'name == "{doc_extract}"')

        if len(doc_in_bdd) == 0:
            cursor.execute(
            f'''INSERT INTO anatomopathologists (name, id_med)
            VALUES("{doc_extract}", "{len(docs_df)}");''')    
            bdd.commit()
            id_doc = len(docs_in_bdd)
        else:
            id_doc = doc_in_bdd.id_med.tolist()[0]    

    if nir_find is not None:
        predict['NIR'] = [nir_find.group(1).strip()]

        cursor.execute(f'SELECT nir FROM patients WHERE nir = "{nir}";')
        patient_in_bdd = cursor.fetchall()
        if len(patient_in_bdd) == 0:
            nir = nir_find.group(1).strip()
            cursor.execute(
            f'''INSERT INTO patients (name, address, birthday, nir)
            VALUES("{patient_extract}", "{address_extract}", "{birthday_extract}", "{nir}");''')
            bdd.commit()           


    cursor.execute('SELECT id_CRO FROM CRO ORDER BY id_CRO DESC LIMIT 1;')
    CRO_in_bdd = cursor.fetchall()
    ids_CRO = pd.DataFrame(CRO_in_bdd, columns=['id_CRO'], dtype=str)
    id_last_CRO = int(ids_CRO.id_CRO[0])

    id_diag = -1
    if 'DIAG' in predict:
        predict_in_CRO = predict['DIAG'][0]
    
        cursor.execute(f'SELECT * FROM diagnostics_v2;')
        diags_in_bdd = cursor.fetchall()
        columns=[i[0] for i in cursor.description]
        diags_df = pd.DataFrame(diags_in_bdd, columns= columns, dtype=str)
        
        diag_in_bdd = diags_df.query(f'diagnostic == "{predict_in_CRO}"')

        if len(diag_in_bdd) == 0:
            cursor.execute(
            f'''INSERT INTO diagnostics_v2 (diagnostic, id_diag)
            VALUES("{predict_in_CRO}", "{len(diags_df)}");''')    
            bdd.commit()
            id_diag = len(diags_in_bdd)
        else:
            id_diag = diag_in_bdd.id_diag.tolist()[0]

    query =  f'''INSERT INTO CRO (CRO, nir, id_diag, id_med, load_by, id_CRO)
        VALUES("{CRO}", "{nir}", "{int(id_diag)}", "{int(id_doc)}", "{id_user}", "{id_last_CRO + 1}");'''
    cursor.execute(query)    
    bdd.commit()

    if id_diag == -1:
        utils.send_mail('CRO sans diagnostic trouvé', CRO)
    

    if len(predict.keys()) > 0:
        response = {'response': True,           
                    'predict': predict}
        return jsonify(response)
    else:
        response = {'response': False}
    
    # except Exception as e:
    #     print(e)
    #     utils.send_mail('endpoint predict', e)

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
                    diagnostics_v2.id_diag, diagnostic,
                    address, birthday, name, nir
                    FROM CRO 
                    JOIN patients USING (nir) 
                    JOIN diagnostics_v2 USING (id_diag) 
                    {"WHERE name = '" + patient + "'" if patient != "" else ""};''')
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
        print(id_CRO)

        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT * FROM CRO
                    JOIN patients USING (nir)
                    JOIN diagnostics_v2 USING (id_diag)
                    JOIN anatomopathologists USING (id_med)
                    JOIN logins ON CRO.load_by = logins.id
                    WHERE id_CRO = "{int(id_CRO)}";''')
        datas_CRO = cursor.fetchall()    

        columns=[i[0] for i in cursor.description]

        print(columns)

        columns[8] = 'name_patient'
        columns[15] = 'name_med'

        cursor.close()

        datas_CRO = pd.DataFrame(datas_CRO, columns = columns, dtype=str)
        datas_CRO = datas_CRO.drop(['id_med', 'id_diag', 'operation', 'load_by', 'id', 'password', 'id_role', 'source', 'generation', 'statut', 'nb_mots'], axis = 1)
        datas_CRO_response = datas_CRO.to_dict(orient='records')

        print(datas_CRO_response)

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
        bdd = utils.get_db_connection()
        cursor = bdd.cursor()

        cursor.execute(f'''SELECT * FROM metrics;''')
        metrics = cursor.fetchall()   

        columns=[i[0] for i in cursor.description]
        cursor.close()

        df_metrics = pd.DataFrame(metrics, columns= columns, dtype=str)
        metrics_list = df_metrics.to_dict(orient='list')

        response = {'response': metrics_list}
        return jsonify(response)
    
    except Exception as e:
        print(e)
        utils.send_mail('endpoint metriques', e)


dashboard.config.enable_logging=True    
dashboard.bind(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)