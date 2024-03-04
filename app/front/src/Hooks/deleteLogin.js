import axios from "axios";

// permet de supprimer un utilisateur
export const fetchDeleteLogin = (obj) => {
    return axios.put(
        `/deleteLogin`, obj
    ).then(response => response.data)
};