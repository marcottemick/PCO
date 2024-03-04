import { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import './Antecedent.css';
// permet de charger les antécédents ou un antécédent si un patient est sélectionné
import { fetchGetAntecedents } from '../../Hooks/getAntecedents';
// permet de récupérer le CRO et les données extraites à partir de l'id
import { fetchGetReadCRO } from '../../Hooks/getReadCRO';
// modale qui permet de lire le CRO et les détails
import ModalCRO from './CROmodal';
// page de chargement et d'erreur
import Chargement from '../../Elements/Chargement';
// élément qui permet de renseigner un patient
import Input from './Input';

// affichage des antécédents des patients. Un input permet de sélectioner un patient en particulier.
const Antecedent = () => {
    // stocke les antécédents de chaque patient
    const [antecedents, setAntecedents] = useState([]);
    // stocke temporairement l'id du CRO à visualiser
    const [idCRO, setIdCRO] = useState('');
    // stocke les données pour affichage dans la modale
    const [detailCRO, setDetailCRO] = useState({});
    // sélection du patient pour recherche
    const [valuePatient, setValuePartient] = useState('');
    // gestion de la modale
    const [isOpen, setIsOpen] = useState(false);
    // gestion du chargement des données
    const [isLoading, setIsLoading] = useState(false);
    // validation du patient après entré dans l'input
    const [validSearch, setValidSearch] = useState(false);
    // gestion des erreurs de chargement
    const [isError, setIsError] = useState(false);
    //message d'erreur ou chargement (par défaut)
    const [errorMessage, setErrorMessage] = useState('Aucune donnée pour ce patient !')

    //  charge les antécédents, par défaut, toutes si ancun patient sélectionné
    useEffect(() => {
        setIsLoading(true);
        fetchGetAntecedents(valuePatient)
            .then(response =>
                response.response ?
                    setAntecedents(response.antecedents) :
                    setIsError(true))
            .catch(e => {
                console.error(e.message);
                setIsError(true);
                setErrorMessage('Il y a eu un problème durant le chargement des antécédents patients !')
            })
            .finally(() => setIsLoading(false));
    }, [validSearch]);

    // récupère le CRO, ainsi que les données extraites lorsque l'id du CRO est cliqué
    useEffect(() => {
        if (idCRO !== "") {
            fetchGetReadCRO(idCRO)
                .then(response => {
                    setDetailCRO(response.detailCRO);
                    setIsOpen(true);
                }).catch(e => {
                    console.error(e.message);
                    toast.error('Il y a une erreur durant le traitement de votre demande !', {
                        position: 'bottom-right',
                        autoClose: 3000, // Fermer automatiquement après 3 secondes
                    });
                });
        };
    }, [idCRO]);

    const renderAntecedents = () => {
        return (
            <>
                <Input
                    valuePatient={valuePatient}
                    setValuePartient={setValuePartient}
                    setValidSearch={setValidSearch}
                    isError = {isError}
                    setIsError={setIsError} 
                    setErrorMessage={setErrorMessage}/>
                {!isError ?
                    <div id='container-antecedents'>
                        {/* si aucune erreur, affiche le(s) antécédent(s), si erreur, affiche un message */}
                        {antecedents.map((patient, index) =>
                            <div
                                key={index}
                                className='container-data-patient'>
                                <div>
                                    <p>Information patient:</p>
                                    <ul>
                                        <li>Numéro de sécurité social: {patient.nir}</li>
                                        <li>Patient: {patient.name}</li>
                                        <li>Adresse: {patient.address}</li>
                                        <li>Date de naissance: {patient.birthday}</li>
                                    </ul>
                                </div>
                                <div>
                                    <p>Antécédents:</p>
                                    <ul>
                                        {patient.dict_CRO_diag.map((diag, index) =>
                                            <li
                                                key={index}
                                                className='select-CRO'
                                                onClick={() => setIdCRO(Object.values(diag)[0])}>
                                                <div>{Object.keys(diag)} (CRO numéro {Object.values(diag)})
                                                    <span class="material-symbols-outlined">
                                                        feature_search
                                                    </span></div>
                                            </li>)}
                                    </ul>
                                </div>
                            </div>)}
                    </div> : <Chargement
                        texte={errorMessage}
                    />}
                {!isOpen || <ModalCRO
                    setIsOpen={setIsOpen}
                    antecedents={antecedents}
                    idCRO={idCRO}
                    detailCRO={detailCRO}
                    setIdCRO={setIdCRO}
                />}
            </>
        );
    };

    // affiche les données une fois que la variable de chargement passe en false
    if (isLoading) {
        return <Chargement
            texte='Chargement des antécédents en cours ...'
        />
    }
    else {
        return renderAntecedents();
    }

};

export default Antecedent;