import { useState } from 'react'
import { BrowserRouter as Router, Route, Switch, useLocation } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'

import Start from './components/core/Start'
import Redirecting from './components/core/Redirecting'
import Register from './components/core/Register'
import Dashboard from './components/dashboard/Dashboard'
import DefaultNavbar from './components/navbar/DefaultNavbar'
import AccountManager from './components/account/AccountManager'
import NotAuthorized from './components/core/NotAuthorized'
import Analyser from './components/analyser/Analyser'

function App() {

  const { isAuthenticated, isLoading } = useAuth0();
  const [isLogged, setIsLogged] = useState(sessionStorage.getItem('isLogged'))
  const location = useLocation();

  return (
    <div className="App">
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

                    <Route path="/account/analyser">
                      <Analyser />
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
