import axios from "axios";

// récupère le rôle après vérification de l'identification
export const fetchPutLogin = (obj) => {
    return axios.put(
        '/login', obj
    ).then(response => response.data)
};