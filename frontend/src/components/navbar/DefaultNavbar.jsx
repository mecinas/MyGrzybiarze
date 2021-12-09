import React from 'react'
import { Navbar, Nav, Button} from 'react-bootstrap'
import ProfileTypeahead from './ProfileTypeahead'
import Notification from './Notification'

import companyLogo from '../../resources/company_logo.png'

export default function DefaultNavbar() {

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
                <Nav.Link href="#features">TODO</Nav.Link>
            </Nav>
            <ProfileTypeahead />
            <Notification />
        </Navbar>
    )
}



