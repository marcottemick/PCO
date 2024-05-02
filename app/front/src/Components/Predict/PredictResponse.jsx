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

    const predict_viod = (arr) => arr != null ? arr.join(', ') : 'Pas de donnée'

    return (
        <div id='container-predict'>
            {!predictSuccess ? <Chargement texte='Votre CRO ne contient aucune donnée à extraire !' /> :
                <div id='container-response'>
                    <div id='predict-CRO'>
                        <div id="container-text"
                            // affichage du CRO agrémenté de CSS au niveau des entités déterminées 
                            dangerouslySetInnerHTML={sanitizedData(CROpredict)} />
                    </div>
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
                </div>}
        </div>
    );
};

export default PredictResponse;

/*
Patient : Gilbert Étienne,
Adresse : 49, boulevard de Jacques, 21813 Legendre
Date de naissance : 15/01/1963
Numéro de sécurité social : 1 1963 01 21813 466 38
Description macroscopique :
Dans ce cas clinique, nous avons reçu une pièce cutanée mesurant environ 3 cm x 2 cm, provenant d'une biopsie pratiquée sur une plaque cutanée érythémateuse, papuleuse et à lésions argentées caractéristiques du psoriasis. La section transversale révélait une zone centrale hyperkératoseuse, associée à des infiltrats inflammatoires sous-jacents, tandis qu'une bordure périphérique apparaissait normale.
Description microscopique :
Au niveau histologique, on note une hyperprolifération acanthocytaire associée à une augmentation quantitative et qualitative des kératinocytes matures (parakératose). L'épithélium épineux présente une orthokératose au centre, avec formation de micropapilles et parfois des acanthomes. Les espaces intercellulaires sont étroits et remplis de leucocytes polymorphes, principalement des neutrophiles. On retrouve également des granules de Munro et des mousseaux de Touton. Au niveau du tissu annexe, il existe une infiltration inflammoire composée majoritairement de lymphocytes T helper 1 et de neutrophiles.
Immunohistochimie :
Pour confirmer notre hypothèse diagnostique, nous avons réalisés plusieurs marquages immunhistochimiques. Nous avons détecté une expression importante de l'anticorps anti-HLA DR4 dans les cellules inflammatoires, ce qui est consistant avec un psoriasis. De plus, on observe une forte expression de CD86, marqueur des macrophages activés, ainsi qu'une faible expression de FOXP3, indice d'une activation Th1 dominante.
Conclusion :
Ce compte rendu anatomopathologique décrit les aspects macroscopiques et microscopiques observés dans cette biopsie cutanée provenant d'une plaque psoriatique. Les résultats histologiques ont montré une hyperprolifération acanthocytaire, une parakératose et une orthokératose, ainsi qu'une importante infiltration inflammatoire. Des marquages immunhistochimiques ont été effectuées pour confirmer notre hypothèse diagnostique, et les résultats obtenus sont compatibles avec un psoriasis.
Signature : Dr Zacharie Mercier, anatomopathologiste
Note :ceci est un compte rendu fictif
*/