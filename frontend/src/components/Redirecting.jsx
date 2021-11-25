import React, { useState, useEffect } from 'react'
import { Container, Spinner } from 'react-bootstrap'
import { Redirect } from 'react-router-dom'
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios'

import '../styles/Redirecting.css'

export default function Redirecting(props) {
    const [isRegistered, setIsRegistered] = useState(null);
    const [redirection, setRedirection] = useState();
    const { user } = useAuth0();

    const checkIfRegistred = () => {
        var url = "http://localhost:5000/register/check"
        axios.get(url, {
            params: {email: user.email}
        })
            .then(res => {
                setIsRegistered(res.data.isRegistered)
            })
            .catch(error => {
                console.log(error.message)
            })
    }

    useEffect(() => {
        if (user !== undefined) {
            checkIfRegistred()
        }
    }, [user])

    useEffect(() => {
        if(isRegistered !== null)
            if(isRegistered ===  false)
                setRedirection(<Redirect to="/register" />)
            else{
                setRedirection(<Redirect to="/account/dashboard" />)
                sessionStorage.setItem('isLogged', true)
                props.setIsLogged(true)
            }
    }, [isRegistered])

    return (
        <Container>
            <h3 className="text">Przekierunkowanie do odpowiedniej strony</h3>
            <Spinner className="spinner" animation="border" variant="warning" />
            {redirection}
        </Container>
    )
}
