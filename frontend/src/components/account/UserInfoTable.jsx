import React, { useState, useEffect } from 'react';
import { Card, Button, Table, Form, Col } from 'react-bootstrap';
import {useHistory} from 'react-router-dom'
import { Pencil } from 'react-bootstrap-icons';
import { useAuth0 } from '@auth0/auth0-react';

import EditProfileModal from '../EditProfileModal'
import '../../styles/account/UserInfoTable.css'

export default function UserInfoTable(props) {
    const history = useHistory();
    const { user, logout } = useAuth0();
    const [userInfo, setUserInfo] = useState()
    const [modalTitle, setModalTitle] = useState();
    const [modalForm, setModalForm] = useState();
    const [modalURL, setModalURL] = useState();

    const [showEditModal, setShowEditModal] = useState(false);
    const handleShowEditModal = () => setShowEditModal(true);
    const handleCloseEditModal = () => setShowEditModal(false);

    const setModalForName = () => {
        setModalTitle("Edytuj swoje imię i nazwisko")
        setModalURL("http://localhost:5000/account/change/name")
        setModalForm(
            <div>
                <Form.Group controlId="formBasicFirstname">
                    <Form.Control type="text" name='firstname' placeholder="Podaj nowe imię" />
                </Form.Group>

                <Form.Group controlId="formBasicSurname">
                    <Form.Control type="text" name='surname' placeholder="Podaj nowe nazwisko" />
                </Form.Group>
            </div>
        )
    }
    const setModalForNickname = () => {
        setModalTitle("Edytuj swój nick")
        setModalURL("http://localhost:5000/account/change/nickname")
        setModalForm(
            <div>
                <Form.Group controlId="formBasicFirstname">
                    <Form.Control type="text" name='nickname' placeholder="Podaj nowy nick" />
                </Form.Group>
            </div>
        )
    }

    const setModalForDateOfBirth = () => {
        setModalTitle("Edytuj swoją datę urodzenia")
        setModalURL("http://localhost:5000/account/change/dateOfBirth")
        setModalForm(
            <div>
                <Form.Group controlId="formBasicDateOfBirth">
                    <Form.Control type="date" name='dateOfBirth' placeholder="Podaj datę urodzenia" />
                </Form.Group>
            </div>
        )
    }

    const logUserOut = () => {
        sessionStorage.removeItem('isLogged')
        logout({ returnTo: window.location.origin })
    }

    useEffect(() => {
        props.getInfo(setUserInfo)
        setTimeout(() => {
            props.getInfo(setUserInfo)
        }, 2000);
    }, [user, showEditModal])

    return (
        <Col>
            {user &&
                <EditProfileModal
                    showEditModal={showEditModal}
                    handleCloseEditModal={handleCloseEditModal}
                    title={modalTitle}
                    form={modalForm}
                    modalURL={modalURL}
                    email={user.email} />
            }
            <Card className="text-center">
                <Card.Header>Profil</Card.Header>
                <Card.Body >
                    <Card.Title className="text-left">Twoje informacje</Card.Title>
                    {userInfo &&
                        <Table striped className="text-left">
                            <tbody>
                                <tr>
                                    <td>Nazwa użytkownika</td>
                                    <td>{userInfo.nickname}</td>
                                    <td>
                                        <Button className="pencil_table_ico" variant="light" onClick={() => {
                                            setModalForNickname();
                                            handleShowEditModal();
                                        }}>
                                            <Pencil color="brown" size={20} />
                                        </Button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Imię i nazwisko</td>
                                    <td>{userInfo.firstname} {userInfo.surname}</td>
                                    <td>
                                        <Button className="pencil_table_ico" variant="light" onClick={() => {
                                            setModalForName();
                                            handleShowEditModal();
                                        }}>
                                            <Pencil color="brown" size={20} />
                                        </Button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Data urodzenia</td>
                                    <td>{userInfo.dateOfBirth}</td>
                                    <td>
                                        <Button className="pencil_table_ico" variant="light" onClick={() => {
                                            setModalForDateOfBirth();
                                            handleShowEditModal();
                                        }}>
                                            <Pencil color="brown" size={20} />
                                        </Button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Adres e-mail</td>
                                    <td colSpan="2">{userInfo.email}</td>
                                </tr>
                            </tbody>
                        </Table>
                    }
                </Card.Body>
                <Card.Footer>                    
                    <Button variant="outline-warning" onClick={logUserOut}>Wyloguj się</Button>
                    <Button variant="outline-danger" onClick={props.deleteUser}>Usuń konto</Button>
                </Card.Footer>
            </Card>
        </Col>
    )
}
