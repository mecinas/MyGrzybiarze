import React, { useState, useEffect } from 'react'
import { Typeahead, Menu, MenuItem } from 'react-bootstrap-typeahead';
import { Card, Image, Button } from 'react-bootstrap'
import axios from 'axios';

export default function ProfileTypeahead(props) {

    const [userPhoto, setUserPhoto] = useState(null);
    const [isFriend, setIsFriend] = useState(false);
    const [options, setOptions] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [isProfileHidden, setIsProfileHidden] = useState(false);

    useEffect(() => {
        getUsers()
    }, [])

    useEffect(() => {
        if (selectedUser !== null) {
            checkIfFriends()
            getAvatar()
        }
    }, [selectedUser])

    const getUsers = () => {
        axios.get("http://localhost:5000/user/list")
            .then(resp => {
                setOptions(resp.data)
            }).catch(error => {
                console.log(error.message)
            })
    }

    const checkIfFriends = () => {
        axios.get("http://localhost:5000/friendship/check", {
            params: {
                first_email: props.loggedUser.email,
                sec_email: selectedUser.email
            }
        })
            .then(resp => {
                setIsFriend(resp.data.areFriends)
            }).catch(error => {
                console.log(error.message)
            })
    }

    const deleteFriend = () => {
        var url = "http://localhost:5000/account/avatar"
        axios.delete(url, {
            data: {
                first_email: props.loggedUser.email,
                sec_email: selectedUser.email
            }
        }).catch(error => {
            console.log(error.message)
        })
    }

    const sendFriendRequest = (request_user) => {
        let url = "http://localhost:5000/notification"
        let data = {
            notification_type: "action",
            message: props.loggedUser.firstname + " " + props.loggedUser.surname + " wysłałał/a Ci zaproszenie do znajomych",
            user_email: selectedUser.email,
            request_user: props.loggedUser.email
        }
        axios.post(url, data)
        .catch(error => console.log(error.message))
    }

    const getAvatar = () => {
        const time = new Date().getTime(); //Prevents cache photo memory
        var url = "http://localhost:5000/account/avatar"
        axios.get(url, {
            responseType: 'arraybuffer',
            params: {
                email: selectedUser.email,
                t: time
            }
        })
            .then(response => {
                setUserPhoto(encodeImage(response.data))
            })
            .catch(error => {
                console.log(error.message)
            })

    }

    function encodeImage(arrayBuffer) {
        let b64encoded = btoa([].reduce.call(new Uint8Array(arrayBuffer), function (p, c) { return p + String.fromCharCode(c) }, ''))
        let mimetype = "image/png"
        return "data:" + mimetype + ";base64," + b64encoded
    }

    const renderMenu = (results) => {
        return (
            <Menu id="menu-id">
                {results.map((option, index) => {
                    let jsonOption = JSON.parse(option)
                    return (
                        <MenuItem
                            key={index}
                            onMouseEnter={() => {
                                setSelectedUser(jsonOption)
                                setIsProfileHidden(true)
                            }}
                            onMouseLeave={() => {
                                setIsProfileHidden(false)
                            }}
                            option={jsonOption.firstname + " " + jsonOption.surname}
                            position={index}
                        >
                            {jsonOption.firstname + " " + jsonOption.surname}
                        </MenuItem>
                    )
                }
                )}
            </Menu>
        );
    };

    return (
        <div className="mr-4 d-flex position-relative">
            {isProfileHidden &&
                <Card
                    className="position-absolute"
                    style={{ width: '18rem', right: "235px" }}
                    onMouseEnter={() => { setIsProfileHidden(true) }}
                    onMouseLeave={() => { setIsProfileHidden(false) }}>
                    <Card.Header className="d-flex" style={{ width: '100%' }}>
                        {userPhoto &&
                            <Image
                                className="avatar_img mx-auto"
                                src={userPhoto}
                                roundedCircle={true}
                                style={{ width: '10vw' }} />
                        }
                    </Card.Header>
                    <Card.Body>
                        <Card.Title>{selectedUser.firstname + " " + selectedUser.surname}</Card.Title>
                        <Card.Footer>
                            {!isFriend &&
                                <Button variant="outline-success" onClick={() => sendFriendRequest()}>
                                    Dodaj do znajomych
                                </Button>
                            }{isFriend &&
                                <div>
                                    <Card.Text>Jesteście znajomymi</Card.Text>
                                    <Button variant="outline-danger" onClick={() => deleteFriend()}>
                                        Usuń z znajomych
                                </Button>
                                </div>
                            }
                        </Card.Footer>
                    </Card.Body>
                </Card>
            }
            <Typeahead
                id="typeahead-id"
                options={options}
                placeholder="Wyszukaj znajomych..."
                renderMenu={renderMenu}
            />

        </div>
    )
}
