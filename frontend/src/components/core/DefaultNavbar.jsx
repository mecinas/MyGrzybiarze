import React, { useState, useEffect } from 'react'
import { Component } from 'react';
import { Navbar, Nav, Form, Button, FormControl } from 'react-bootstrap'
import { Typeahead, Menu, MenuItem } from 'react-bootstrap-typeahead';
import axios from 'axios';

import companyLogo from '../../resources/company_logo.png'

export default function DefaultNavbar() {

    const [options, setOptions] = useState([]);

    useEffect(() => {
        setOptions([
            "Apples",
            "Avocados",
            "Bananas",
            "Broccoli",
            "Oranges",
            "Kale",
            "Lemons",
            "Limes"
        ]);

        getUsers()
        
    }, [])

    const getUsers = () => {
        axios.get("http://localhost:5000/user/list")
        .then(resp => {
            setOptions(resp.data.map(value => {
                return value.firstname + " " + value.surname
            }))
        }).catch(error => {
          console.log(error.message)
        })
    }

    const renderMenu = (results) => {
        return (
            <Menu id="menu-id">
                {results.map((option, index) => (
                    <MenuItem 
                        key={index}
                        onMouseEnter={(e) => {console.log(e.target)}}
                        onMouseLeave={(e) => {console.log(e)}}
                        option={option}
                        position={index}
                    >
                        {option}
                    </MenuItem>
                ))}
            </Menu>
        );
    };


    return (
        <Navbar bg="warning" variant="light">
            <Navbar.Brand href="/dashboard">
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
            <div className="mr-4">
                <Typeahead
                    id="typeahead-id"
                    options={options}
                    placeholder="Wyszukaj znajomych..."
                    renderMenu={renderMenu}
                 />
            </div>

        </Navbar>
    )
}



