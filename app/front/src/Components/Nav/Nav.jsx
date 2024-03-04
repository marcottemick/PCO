import { NavLink } from 'react-router-dom';
import './Nav.css';

// affichage du menu de navigation
const Nav = ({ token, setToken }) => {

    const resetLogin = () => {
        // supprime le token => déconnexion
        localStorage.removeItem('token');
        setToken(null);
    };

    return (
        <>
            <nav>
                <ul>
                    {/* prend en compte le rôle pour l'affichage du menu */}
                    {token.role > 1 ? <NavLink
                        to='/analyse'
                        className='link'
                        activeClassName='active-link'>
                        <li><span className="material-symbols-outlined">
                            manage_search
                        </span>Analyse de CRO
                        </li>
                    </NavLink> : null}
                    <NavLink
                        to='/patients'
                        className='link'
                        activeClassName='active-link'>
                        <li><span className="material-symbols-outlined">
                            patient_list
                        </span>Antécédents Patients
                        </li>
                    </NavLink>
                    {token.role > 2 ? <NavLink
                        to='/statistiques'
                        className='link'
                        activeClassName='active-link'>
                        <li><span className="material-symbols-outlined">
                            monitoring
                        </span>Statistiques
                        </li>
                    </NavLink> : null}
                    {token.role > 3 ? <NavLink
                        to='/admin'
                        className='link'
                        activeClassName='active-link'>
                        <li><span className="material-symbols-outlined">
                            admin_panel_settings
                        </span>Administration
                        </li>
                    </NavLink> : null}
                </ul>
            </nav>
            <p onClick={resetLogin}>
                {/* bouton de déconnexion */}
                <span className="material-symbols-outlined">
                    logout
                </span>
                Déconnexion</p>
        </>
    );
};

export default Nav;