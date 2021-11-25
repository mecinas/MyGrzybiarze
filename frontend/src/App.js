import './App.css';
import {useState} from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'

import Start from './components/Start'
import Redirecting from './components/Redirecting'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import DefaultNavbar from './components/DefaultNavbar'
import AccountManager from './components/account/AccountManager'
import NotAuthorized from './components/NotAuthorized'

//Zabezpieczenie stron

function App() {

  const { isAuthenticated, isLoading } = useAuth0();
  const [isLogged, setIsLogged] = useState(sessionStorage.getItem('isLogged'))
  return (
    <div className="App">
      <Router>
        <Route exact path="/">
          <Start />
        </Route>

        <Route path="/redirect">
          {!isLoading && isAuthenticated &&
            <Redirecting setIsLogged={setIsLogged}/>
          }
          {!isLoading && !isAuthenticated &&
            <NotAuthorized />
          }
        </Route>

        <Route path="/account">
        {!isLoading && isAuthenticated && isLogged &&
            <DefaultNavbar />
          }
          {!isLoading && (!isAuthenticated || !isLogged)&&
            <NotAuthorized />
          }
        </Route>

        <Route path="/account/dashboard">
        {!isLoading && isAuthenticated && isLogged &&
            <Dashboard />
          }
        </Route>

        <Route path="/account/manager">
        {!isLoading && isAuthenticated && isLogged &&
            <AccountManager />
          }
        </Route>

        <Route path="/register">
        {!isLoading && isAuthenticated &&
            <Register setIsLogged={setIsLogged}/>
          }
          {!isLoading && !isAuthenticated &&
            <NotAuthorized />
          }
        </Route>

      </Router>
    </div>
  );
}

export default App;
