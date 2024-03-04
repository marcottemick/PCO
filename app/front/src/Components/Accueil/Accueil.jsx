import './Accueil.css';

import { useEffect } from 'react';

import { fetchGetTest } from "../../Hooks/getTest";

//  page d'accueil
const Accueil = () => {
    useEffect(() => {
        fetchGetTest().then(response => console.log(response.response))
    }, []);

    return (
        <div id='container-accueil'>
            <ul>
                <li>
                    <div id='logo-accueil'>
                        C.R.Otomy
                    </div>
                </li>
                <li>
                    C.R.Otomy est une application qui permet d'extraire les données (diagnostic, nom, date, adresse & médecin) à partir de compte rendu opératoire d'anatomopathologie.
                    L'application permet aussi de voir les antécédents des patients et le CRO associé à un diagnostic donné.
                </li>
                <li>
                    La page 'Analyse de CRO' vous propose d'extraire les données d'un CRO via un textarea.
                    La réponse apparaît avec le CRO agrémenté des entités trouvées et un détail des données extraites.
                </li>
                <li>
                    La page 'Base de données Patients' permet de voir les antécédents des patients. Une modale permet de voir le CRO en détail.
                </li>
            </ul>
        </div>
    );
};

export default Accueil;