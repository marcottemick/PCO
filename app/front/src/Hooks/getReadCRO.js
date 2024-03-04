import axios from "axios";

// récupère un CRO dans la base de données en fonction de son id, ainsi que les détails extraits
export const fetchGetReadCRO = (id_CRO) => {
    return axios.get(
        `/CRO?id_CRO=${id_CRO}`
    ).then(response => response.data)
};