import React, { useState, useEffect } from 'react'
import { Navbar, Nav, Button } from 'react-bootstrap'
import ProfileTypeahead from './ProfileTypeahead'
import Notification from './Notification'
import axios from 'axios'
import { useAuth0 } from '@auth0/auth0-react'

import companyLogo from '../../resources/company_logo.png'
import LoggedUser from './LoggedUser'

export default function DefaultNavbar() {
    const [loggedUser, setLoggedUser] = useState(null);
    const { user } = useAuth0();

    useEffect(() => {
        getLoggedUser()
    }, [])

    const getLoggedUser = () => {
        if (user !== undefined) {
            let url = "http://localhost:5000/user/single"
            axios.get(url, {
                params: {
                    email: user.email
                }
            })
                .then(resp => {
                    setLoggedUser(resp.data)
                })
                .catch(error => console.log(error.message))
        }
    }

    return (
        <Navbar bg="warning" variant="light" >
            <Navbar.Brand href="/account/dashboard">
                <img
                    src={companyLogo}
                    width="80"
                    height="60"
                    className="d-inline-block align-top"
                    alt="React Bootstrap logo"
                />
            </Navbar.Brand>
            <Nav className="mr-auto">
                <Nav.Link href="/account/manager">Zarządzaj kontem</Nav.Link>
                <Nav.Link href="/account/analyser">Analizator grzybów</Nav.Link>
            </Nav>
            <LoggedUser />
            <ProfileTypeahead loggedUser={loggedUser} />
            <Notification />
        </Navbar>
    )
}



