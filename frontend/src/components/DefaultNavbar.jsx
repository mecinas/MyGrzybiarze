import React from 'react'
import { Navbar, Nav, Form, Button, FormControl } from 'react-bootstrap'

import companyLogo from '../resources/company_logo.png'

export default function DefaultNavbar() {
    return (
        <Navbar bg="warning" variant="light">
            <Navbar.Brand>
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
            <Form inline>
                <FormControl type="text" placeholder="Znajdź opis dla grzyba" className="mr-sm-2" />
                <Button variant="outline-light">Znajdź</Button>
            </Form>
        </Navbar>
    )
}
