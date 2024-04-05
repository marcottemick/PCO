import './App.css';

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import 'react-toastify/dist/ReactToastify.css';

import Antecedent from './Components/Antecedent/Antecedent';
import Predict from './Components/Predict/Predict';
import Nav from './Components/Nav/Nav';
import Accueil from './Components/Accueil/Accueil';
import Surveillance from './Components/Surveillance/Surveillance';
import useToken from './useToken';
import Login from './Components/Login/Login';
import Administation from './Components/Administration/Administration';

function App() {
  const { token, setToken } = useToken();

  console.log(token)

  const renderApp = () => {
    return (
      <>
        <Router>
          <header>
            <a id='logo' href='/'>C.R.Otomy</a>
            <Nav
              token={token}
              setToken={setToken}
            />
          </header>
          <body>
            <Switch>
              <Route exact path='/'>
                <Accueil token={token} />
              </Route>
              <Route path='/analyse'>
                <Predict id={token.id}/>
              </Route>
              <Route path='/patients'>
                <Antecedent />
              </Route>
              <Route path='/statistiques'>
                <Surveillance />
              </Route>
              <Route path='/admin'>
                <Administation />
              </Route>
            </Switch>
          </body>
        </Router>
        <footer>
          <p>Powered by</p>
          <img
            src={'https://upload.wikimedia.org/wikipedia/commons/8/88/SpaCy_logo.svg'}
            alt='logo de Spacy'
          />
          <p>. Created by Marcotte Mickaël.</p>
        </footer>
      </>
    );
  };

  if (!token) {
    return (
      <div>
        <Login
          setToken={setToken}
        />
        <footer>
          <p>Powered by</p>
          <img
            src={'https://upload.wikimedia.org/wikipedia/commons/8/88/SpaCy_logo.svg'}
            alt='logo de Spacy'
          />
          <p>. Created by Marcotte Mickaël.</p>
        </footer>
      </div>
    )
  } else if (token) {
    return renderApp();
  };
};

export default App;
