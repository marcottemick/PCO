import axios from "axios";

// envoie du CRO à l'API est récupèration de la prédiction
export const fetchPutCRO = (CRO) => {
    return axios.put(
        '/predict', CRO
    ).then(response => response.data)
};