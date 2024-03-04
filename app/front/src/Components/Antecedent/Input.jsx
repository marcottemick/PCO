import { useState, useEffect } from "react";
// permet de charger l'ensemble des patients
import { fetchGetPatients } from "../../Hooks/getPatients";

// permet de sélectionner un patient en particulier
const Input = ({ valuePatient, setValuePartient, setValidSearch, isError, setIsError, setErrorMessage }) => {
    // contient l'ensemble des patients de la base de données
    const [patients, setPatients] = useState([]);

    // appel par défaut l'ensemble des patients de la base de données
    useEffect(() => {
        fetchGetPatients()
        .then(response => setPatients(response.patients))
        .catch(e => {
            console.error(e.message);
            setIsError(true);
            setErrorMessage('Il y a eu un problème durant le chargement des antécédents patients !')
        })
    }, [])

    // modifie la valeur du patient sélectionné
    const handleInputChange = (e) => {
        setValuePartient(e.target.value);
    };

    console.log(isError)

    return (
        <div id='container-input'>
            <div>
                <label>
                    Rechercer un patient:
                    <input
                        type="text"
                        list='patients'
                        value={valuePatient}
                        onChange={handleInputChange}
                        disabled={isError} />
                    <datalist id="patients">
                        {/* génère une liste d'option sélectionnable des patients présent dans la base de données */}
                        {
                            patients.map((patient, index) =>
                                <option value={patient} key={index}></option>
                            )
                        }
                    </datalist>
                </label>
                <button
                // bouton de validation de la recherche
                    className="btn"
                    onClick={() => {
                        setValidSearch(prev => !prev);
                    }}><div>
                        <span class="material-symbols-outlined">done</span>
                        Valider
                    </div>
                </button>
                <button
                // bouton de rechargement de l'ensemble des données
                    className="btn"
                    onClick={() => {
                        setValidSearch(prev => !prev);
                        setValuePartient('');
                        setIsError(false);
                    }}>
                    <div>
                        <span class="material-symbols-outlined">arrow_back</span>
                        Réinitialiser
                    </div>
                </button>
            </div>
        </div>
    );
};

export default Input;