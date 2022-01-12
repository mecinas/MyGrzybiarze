import axios from "axios";
import React, { useState } from "react";
import { Form, Button, Jumbotron, Container } from 'react-bootstrap'
import { useAuth0 } from '@auth0/auth0-react'
import { Redirect } from 'react-router-dom';
import { useHistory } from 'react-router-dom'

import '../../styles/Register.css'

export default function CreateUser(props) {
    const history = useHistory();
    const { user } = useAuth0();

    const onFormSubmit = e => {
        e.preventDefault()
        const formData = new FormData(e.target)
        const data = Object.fromEntries(formData.entries())
        const { email } = user;
        data["email"] = email
        createUser(data)
        sessionStorage.setItem('isLogged', true)
        props.setIsLogged(true)
        setTimeout(() => {
            history.push("/account/dashboard")
        }, 500)
        
    }

    const createUser = (data) => {
        var url = "http://localhost:5000/register"
        axios.post(url, data)
            .then(resp => {
            })
            .catch(error => {
                console.log(error.message)
            })
    }

    return (
        <Container onSubmit={onFormSubmit}>
            <Jumbotron className="greeting-jumbo">
                <h1 className="greeting-title">Witaj na naszej platformie!</h1>
                <h5>
                    Twoje konto nie zostało jeszcze utworzone, aby skorzystać z pełni możliwości MyGrzybiarze wypełnij poniższy formularz
                </h5>

                <Button variant="primary">Dowiedz się więcej o korzyściach korzystania z MyGrzybiarze</Button>
            </Jumbotron>

            <Form>
                <Form.Group controlId="formBasicNickname">
                    <Form.Control type="text" name='nickname' placeholder="Wprowadź pseudonim" />
                </Form.Group>

                <Form.Group controlId="formBasicFirstname">
                    <Form.Control type="text" name='firstname' placeholder="Wprowadź imię" />
                </Form.Group>

                <Form.Group controlId="formBasicSurname">
                    <Form.Control type="text" name='surname' placeholder="Wprowadź nazwisko" />
                </Form.Group>

                <Form.Group controlId="formBasicDate">
                    <Form.Label>Data urodzin</Form.Label>
                    <Form.Control type="date" name='dateOfBirth' />
                </Form.Group>

                <Form.Group className="checkbox-group" controlId="formBasicCheckbox">
                    <Form.Check type="checkbox" />
                    <Form.Label>Potwierdzam zapoznanie z <a href="/createUser">Regulaminem</a></Form.Label>
                </Form.Group>

                <Form.Group className="btn-group">
                    <Button className="submit-btn" variant="warning" type="submit">
                        Prześlij
                    </Button>
                </Form.Group>

            </Form>

        </Container>
    )
}
