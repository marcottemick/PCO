import axios from "axios";

// récupère le rôle après vérification de l'identification
export const fetchPostLogin = (obj) => {
    return axios.post(
        '/ajoutLogin', obj
    ).then(response => response.data)
};