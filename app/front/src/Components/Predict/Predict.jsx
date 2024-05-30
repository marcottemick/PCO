import "./Predict.css"

import { useState } from "react";
import { toast } from 'react-toastify';

// envoie du CRO et récupèration de la prédiction
import { fetchPutCRO } from "../../Hooks/putCRO";

import PredictResponse from "./PredictResponse";

import Textarea from "./TextArea";
import Chargement from "../../Elements/Chargement";

const Predict = ({id}) => {
    // gère le chargement des données
    const [isLoading, setIsLoading] = useState(false);
    // gère le succès du chargement des données
    const [predictSuccess, setPredictSuccess] = useState(false);
    // stocke le CRO à envoyer
    const [CRO, setCRO] = useState('');
    // récupère la prédiction
    const [predict, setPredict] = useState({});

    // envoie du CRO et récupération de la prédiction
    const handleClickCRO = async () => {
        if (CRO !== "") {
            setIsLoading(true);
            fetchPutCRO({ 'CRO': CRO, 'id_user': id }).then(response => {
                if (response.response) {
                    if (response.response) {
                        setPredictSuccess(response.response);
                        setPredict(response.predict);
                    }
                    else {
                        setPredictSuccess(response.response);
                    };                    
                };
            })
                .then(() => setIsLoading(false))
                .catch(e => {
                    setIsLoading(false);
                    toast.error("Une erreur est survenue durant l'analyse du CRO !", {
                        position: 'bottom-right',
                        autoClose: 3000, // Fermer automatiquement après 3 secondes
                    });
                    console.error(e.message)
                })

        }
        else {
            toast.error('Aucun CRO à analyser !', {
                position: 'bottom-right',
                autoClose: 5000,
            });
        };
    };

    // réinitialise les variables pour une nouvelle recherche
    const handleNewPredict = () => {
        setPredictSuccess(false);
        setCRO('');
        setPredict({});
    };

    const PredictRender = () => {
        return (
            <div id="container-predict">
                {!predictSuccess ?
                    <Textarea
                        CRO={CRO}
                        setCRO={setCRO}
                        handleClickCRO={handleClickCRO}
                    /> :
                    <PredictResponse
                        CRO={CRO}
                        predict={predict}
                        handleNewPredict={handleNewPredict}
                        predictSuccess = {predictSuccess}
                    />
                }
            </div>
        );
    };

    // gestion du chargement de la donnée
    if (isLoading) {
        return <Chargement
            texte='Analyse du CRO en cours ...'
        />
    }
    else {
        return PredictRender();
    };
};

export default Predict