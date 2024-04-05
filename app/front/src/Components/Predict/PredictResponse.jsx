import Chargement from "../../Elements/Chargement";
import { sanitizedData } from "../../Elements/utils";

// affichage du CRO après analyse par le modèle agrémenté de CSS.
const PredictResponse = ({ predict, CRO, handleNewPredict, predictSuccess }) => {

    // place le CRO entre deux balises p
    let CROpredict = "<p>" + CRO + "</p>";
    // ajoute des span aux entités trouvés par le modèle pour permettre l'ajout de CSS sur le texte
    let keys = Object.keys(predict);
    for (let i = 0; i < keys.length; i++) {
        for (let j = 0; j < keys[i].length; j++) {
            CROpredict = CROpredict.replaceAll(predict[keys[i]][j], `<span class="predict ${keys[i]}">${predict[keys[i]][j]} - <strong>${keys[i]}</strong></span>`);
            CROpredict = CROpredict.replaceAll('\n', '<br/>');
            console.log(CROpredict.includes('\n'))
        };
    };

    const predict_viod = (arr) => arr != null ? arr.join(', '): 'Pas de donnée'

    return (
        <div id='container-predict'>
            {!predictSuccess ? <Chargement texte='Votre CRO ne contient aucune donnée à extraire !'/>:
            <div id='container-response'>
                <div id='predict-CRO'
                    // affichage du CRO agrémenté de CSS au niveau des entités déterminées 
                    dangerouslySetInnerHTML={sanitizedData(CROpredict)} />
                <div id='predict-list'>
                    {/* affichage des données extraites du CRO */}
                    <ul>
                        <li>Anatomopathologiste: {predict_viod(predict.DOC)}</li>
                        <li>Patient: {predict_viod(predict.PER)}</li>
                        <li>Date de naissance: {predict_viod(predict.DATE)}</li>
                        <li>Adresse: {predict_viod(predict.LOC)}</li>
                        <li>NIR: {predict_viod(predict.NIR)}</li>
                        <li>Diagnostic: <strong>{predict_viod(predict.DIAG)}</strong></li>
                    </ul>
                </div>
            </div>}
            <div id='container-btn'>
                <button
                    // bouton qui permet de réinitialiser la recherche 
                    onClick={handleNewPredict}
                    className='btn'>
                    <div>
                        <span class="material-symbols-outlined">arrow_back</span>
                        Analyser un nouveau CRO
                    </div>
                </button>
            </div>
        </div>
    );
};

export default PredictResponse;