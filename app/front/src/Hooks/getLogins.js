import axios from "axios";

// permet d'obtenir toutes les personnes pouvant se logger sur le site
export const fetchGetLogins = () => {
    return axios.get(
        `/logins`
    ).then(response => response.data)
};