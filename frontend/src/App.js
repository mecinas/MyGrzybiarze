import { useState } from 'react'
import { BrowserRouter as Router, Route, Switch, useLocation } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'

import Start from './components/Start'
import Redirecting from './components/Redirecting'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import DefaultNavbar from './components/DefaultNavbar'
import AccountManager from './components/account/AccountManager'
import NotAuthorized from './components/NotAuthorized'

function App() {

  const { isAuthenticated, isLoading } = useAuth0();
  const [isLogged, setIsLogged] = useState(sessionStorage.getItem('isLogged'))
  const location = useLocation();

  return (
    <div className="App">
      {console.log("isLoading: " + isLoading)}
      {console.log("isAuthenticated: " + isAuthenticated)}
      {console.log("isLogged: " + isLogged)}
      <Router>
        <Switch>
          <Route exact path="/">
            <Start />
          </Route>

          {!isLoading && <Router>
            <Switch>
              {isAuthenticated && <Router>
                <Switch>

                  <Route path="/redirect">
                    <Redirecting setIsLogged={setIsLogged} />
                  </Route>

                  <Route path="/register">
                    <Register setIsLogged={setIsLogged} />
                  </Route>

                  {isLogged && <Router>
                    <Route path="/account">
                      <DefaultNavbar />
                    </Route>

                    <Route path="/account/dashboard">
                      <Dashboard />
                    </Route>

                    <Route path="/account/manager">
                      <AccountManager />
                    </Route>

                  </Router>}

                  <Route path="*">
                    <NotAuthorized />
                  </Route>

                </Switch>
              </Router>}

              <Route path="*">
                <NotAuthorized />
              </Route>

            </Switch>
          </Router>}
        </Switch>
      </Router>
    </div>
  );
}

export default App;
