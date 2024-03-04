import axios from "axios";

// permet d'obtenir tous les antécédents ou un antécédent si un patient est renseigé
export const fetchGetAntecedents = (patient) => {
    return axios.get(
        `/antecedents?patient=${patient}`
    ).then(response => response.data)
};