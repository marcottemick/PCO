import { useState } from 'react';

//permet de gérer le token en le stockant et en l'utilisant sur le site
const useToken = () => {
    const getToken = () => {
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString); 
        return userToken
    };

    const [token, setToken] = useState(getToken());

    console.log(token)

    const saveToken = userToken => {
        localStorage.setItem('token', JSON.stringify(userToken));
        setToken(userToken);
    };

    return {
        setToken: saveToken,
        token
    }
}

export default useToken;