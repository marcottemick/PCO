import axios from "axios";

export const fetchGetTest = () => {
    return axios.get(
        '/test'
    ).then(response => response.data)
};