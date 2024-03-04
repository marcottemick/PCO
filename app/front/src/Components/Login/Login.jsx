import { useState } from 'react';
import './Login.css';
import { fetchPutLogin } from '../../Hooks/putLogin';

const Login = ({ setToken }) => {
    const [id, setId] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('')

    const handleClickLogin = (e) => {
        e.preventDefault()
        if (id !== "" && password !== "") {
            fetchPutLogin({ id, password })
            .then(response => {
                if (response.role === 0) {
                    setErrorMessage('Erreur: identifiant ou mot de passse erroné !');
                }
                else {
                    setToken({
                        'id': id,
                        'role': response.role
                    });
                };
            }).catch(e => {
                console.error(e.message);
                setErrorMessage('Erreur: connexion perdue !')
            });
        }
    };

    return (
        <div id='page-login'>
            <div >
                <div id='container-bienvenu'>
                    <p>Bienvenu sur</p> 
                    <p id='logo-login'>C.R.Otomy</p>
                </div>
                <div id='container-form'>
                    <form>
                        <input
                            type="text"
                            placeholder="Login"
                            value={id}
                            onChange={e => setId(e.target.value)} />
                    </form>
                    <form>
                        <input
                            type="password"
                            placeholder="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)} />
                    </form>
                    <button
                        className='btn'
                        onClick={handleClickLogin}>Valider</button>
                </div>
            </div>
            <p id='message-error'>
                {errorMessage}
            </p>
        </div>

    );
};

export default Login;