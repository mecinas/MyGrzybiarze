import React, { useState, useEffect } from 'react'
import { Typeahead, Menu, MenuItem } from 'react-bootstrap-typeahead';
import {Card, Image, Button } from 'react-bootstrap'
import axios from 'axios';

export default function ProfileTypeahead() {

    const [userPhoto, setUserPhoto] = useState(null);
    const [options, setOptions] = useState([]);
    const [userName, setUserName] = useState("");
    const [isProfileHidden, setIsProfileHidden] = useState(false);

    useEffect(() => {
        getUsers()
    }, [])

    const getUsers = () => {
        axios.get("http://localhost:5000/user/list")
            .then(resp => {
                setOptions(resp.data)
            }).catch(error => {
                console.log(error.message)
            })
    }

    const getAvatar = (userEmail) => {
        const time = new Date().getTime(); //Prevents cache photo memory
        var url = "http://localhost:5000/account/avatar"
        axios.get(url, {
            responseType: 'arraybuffer',
            params: {
                email: userEmail,
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
                                getAvatar(jsonOption.email)
                                setIsProfileHidden(true)
                                setUserName(jsonOption.firstname + " " + jsonOption.surname)
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
                        <Card.Title>{userName}</Card.Title>
                        <Card.Footer>
                            <Button variant="outline-success">
                                Dodaj do znajomych
                                </Button>
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
