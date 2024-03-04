import axios from "axios";

// permet d'obtenir les métriques de test
export const fetchGetMetriques = () => {
    return axios.get(
        `/metriques`
    ).then(response => response.data)
};