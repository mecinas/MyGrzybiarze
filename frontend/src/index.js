import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react'
import { BrowserRouter as Router} from 'react-router-dom'


const domain = process.env.REACT_APP_AUTH0_DOMAIN;
const clientId = process.env.REACT_APP_AUTH0_CLIENT_ID;
const redirectEndpoint = `/redirect`

ReactDOM.render(
    <Auth0Provider
    domain={domain}
    clientId={clientId}
    redirectUri={window.location.origin + redirectEndpoint}>
      <Router> {/* Router jest potrzebny żeby w App działało wykrywanie lokalizacji URL */}
        <App />
      </Router>
    </Auth0Provider>,
  document.getElementById('root')
);
