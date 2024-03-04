import axios from "axios";

// permet d'obtenir l'ensemble des patients contenus dans la base de données
export const fetchGetPatients = () => {
    return axios.get(
        '/patients'
    ).then(response => response.data)
};