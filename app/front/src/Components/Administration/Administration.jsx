import './Administration.css'

import { useEffect, useState } from 'react';
import { toast } from 'react-toastify';

import { fetchGetLogins } from '../../Hooks/getLogins';
import { fetchDeleteLogin } from '../../Hooks/deleteLogin';

import Chargement from '../../Elements/Chargement';
import { fetchPostLogin } from '../../Hooks/postLogin.js';

// permet de visualiser tous les utilisateurs du site avec login, password et rôle
// les utilisateurs peuvent être supprimé et rajouté
const Administation = () => {
    // contient la liste de tous les utilsateurs
    const [logins, setLogins] = useState([]);
    // surveille le chargement des données
    const [isLoading, setIsLoading] = useState(false);
    // gère le succès du chargement des données
    const [isError, setIsError] = useState(false);
    // surveille l'ajout et la suppression d'utilisateurs
    const [isChange, setIsChange] = useState(false);
    // variables de stockages pour un nouvel utilisateur
    const [loginAjout, setLoginAjout] = useState("");
    const [passwordAjout, setPasswordAjout] = useState("");
    const [roleSelect, setRoleSelect] = useState("");

    // chargement des utilisateurs
    useEffect(() => {
        setIsLoading(true);
        fetchGetLogins()
            .then(response => setLogins(response.logins))            
            .catch(e => {
                console.error(e.message);
                setIsError(true);
            })
            .finally(() => setIsLoading(false));
    }, [isChange]);

    // suppression d'un utilisateur
    const handleClikDeleteLogin = (id, indexCell) => {        
        fetchDeleteLogin({ 'id': id })
        .then(response => {
            if (response.response) {
                const loginsDelete = [...logins]
                loginsDelete.splice(indexCell, 1)
                setLogins(loginsDelete);
            };
        })
        .catch(e => {
            console.error(e.message);
            toast.error('Une erreur est survenue lors de la tentative de suppression !', {
                position: 'bottom-right',
                autoClose: 3000,
            });
        });
    };

    // ajout d'un utilisateur
    const handleClikAjoutLogin = () => {
        fetchPostLogin({
            'login': loginAjout,
            'password': passwordAjout,
            'role': roleSelect
        })
            .then(response => {
                if (response.response) {
                    setIsChange(prev => !prev)
                };
            })
            .catch(e => {
                console.error(e.message);
                toast.error("Une erreur est survenue lors de la tentative d'ajout !", {
                    position: 'bottom-right',
                    autoClose: 3000, // Fermer automatiquement après 3 secondes
                });
            });
    };

    // Exemple de tableau
let monTableau = [1, 2, 3, 4, 5];
console.log(monTableau)

// Index de la valeur à supprimer
let indexASupprimer = 2;

// Utilisation de la méthode splice pour supprimer la valeur à l'index spécifié
monTableau.splice(indexASupprimer, 1);

console.log(monTableau); // Le tableau maintenant : [1, 2, 4, 5]

    const renderLogins = () => {
        return (
            <div id='page-admin'>
                <div id='container-ajout'>
                    <label>
                        <input
                            type="text"
                            placeholder='login'
                            value={loginAjout}
                            onChange={e => setLoginAjout(e.target.value)}
                        />
                    </label>
                    <label>
                        <input
                            type="text"
                            placeholder='password'
                            value={passwordAjout}
                            onChange={e => setPasswordAjout(e.target.value)}
                        />
                    </label>
                    <label for="role">
                        <select
                            id="role"
                            value={roleSelect}
                            onChange={e => setRoleSelect(e.target.value)}
                        >
                            <option value="">--Attribuer un rôle--</option>
                            <option value={1}>Lecteur</option>
                            <option value={2}>Analyse</option>
                            <option value={3}>Dev</option>
                            <option value={4}>Admin</option>
                        </select>
                    </label>
                    <button
                        // bouton de d'ajout d'un utilisateur
                        className='btn'
                        onClick={() => handleClikAjoutLogin()}>
                        Valider
                    </button>
                </div>
                <div id='container-table'>
                    <table>
                        {/* table d'affichage des utilisateurs */}
                        <thead>
                            <tr>
                                <td>Login</td>
                                <td>Password</td>
                                <td>Rôle</td>
                            </tr>
                        </thead>
                        <tbody>
                            {logins.map((cell, indexRow) =>
                                <tr key={indexRow}>{cell.slice(1, 4).map((cell, indexCell) =>
                                    <td key={indexCell}>{cell}</td>)}
                                    <td>
                                        <button
                                            // bouton de suppression d'un utilisateur grâve à son id
                                            className='btn'
                                            onClick={() => handleClikDeleteLogin(cell[0], indexRow)}>
                                            Supprimer
                                        </button>
                                    </td>
                                </tr>)}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    };

    if (isLoading) {
        return <Chargement texte="Données en cours de chargement..." />;
    }
    else if (isError) {
        return <Chargement texte="Une erreur est une survenue durant le chargement des données !" />;
    }
    else {
        return renderLogins();
    };
};

export default Administation;