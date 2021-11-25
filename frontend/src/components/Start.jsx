import React from 'react'
import { Container, Button, Image } from 'react-bootstrap'
import {useAuth0} from '@auth0/auth0-react'

import mushroom from '../resources/mushroom_2.jpg'
import companyLogo from '../resources/company_logo.png'
import auth0Logo from '../resources/auth0_logo.svg'
import '../styles/Start.css'

export default function Start() {
    const {loginWithRedirect} = useAuth0();

    return (
        <div>
            <Image className="mushroom_img" src={mushroom} />
            <Container className="start_container">
                <Image className="logo" src={companyLogo} />
                <h3 className="text">
                    Podziel się swoim grzybowym entuzjazmem z innymi już dziś!
                </h3>
                <Button className="login_btn" variant="outline-secondary" onClick={loginWithRedirect}>
                    <Image src={auth0Logo} className="auth0_logo" />
                                    Zaloguj się za pomocą Auth0
                </Button>
                <h6>Sprawdź nasz <a href="/">Regulamin</a></h6>
            </Container>
        </div>
    )
}
