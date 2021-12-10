import { Button, ListGroup, ListGroupItem } from 'react-bootstrap';
import React, { useState, useEffect, useRef } from 'react'
import { Bell, PersonPlusFill, PersonXFill, Trash } from 'react-bootstrap-icons';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react'

export default function Notification() {
    const [isListHidden, setIsListHidden] = useState(false);
    const [notificationList, setNotificationList] = useState(<ListGroup.Item>Brak nowych powiadomień</ListGroup.Item>);
    const wrapperRef = useRef(null);
    const { user } = useAuth0();

    const createNotification = (user_email) => {
        var url = "http://localhost:5000/user/single"
        if (user !== undefined) {
            axios.get(url, {
                params: {
                    email: user.email
                }
            })
                .then(resp => {
                    postNotification(user_email, resp.data.firstname + " " + resp.data.surname)
                })
        }
    }

    const postNotification = (user_email, user_name) => {
        var url = "http://localhost:5000/notification"
        var notification_type = "info"
        var message = user_name + " przyjął/eła twoje zaproszenie do znajomych"
        axios.post(url,
            {
                notification_type: notification_type,
                message: message,
                user_email: user_email
            }
        )
            .catch(error => {
                console.log(error.message)
            })
    }

    const postFriendship = (sec_user_email) => {
        var url = "http://localhost:5000/friendship"
        if (user !== undefined) {
            axios.post(url, {
                "first_email": user.email,
                "sec_email": sec_user_email
            })
                .catch(error => {
                    console.log(error.message)
                })
        }
    }

    const deleteNotification = (notification_id) => {
        var url = "http://localhost:5000/notification"
        axios.delete(url, {
            data: { notification_id: notification_id }
        })
            .catch(error => {
                console.log(error.message)
            })
    }

    useEffect(() => {
        function handleClick(event) {
            if (wrapperRef.current) {

                if (!wrapperRef.current.contains(event.target))
                    setIsListHidden(false)
                else
                    setIsListHidden(true)
            }
        }
        document.addEventListener("mousedown", handleClick);
        return () => {
            document.removeEventListener("mousedown", handleClick);
        };
    }, [wrapperRef]);

    useEffect(() => {
        getNotifications();
    }, [user])

    const getNotifications = () => {
        if (user !== undefined) {
            axios.get("http://localhost:5000/notification", {
                params: {
                    user_email: user.email
                }
            })
                .then(resp => {
                    if (resp.data.length > 0)
                        setNotificationList(resp.data.map(singleNotification => {
                            if (singleNotification.notification_type === "info")
                                return (
                                    <ListGroup.Item key={singleNotification.id}>
                                        {singleNotification.message}
                                        <Button
                                            className="position-absolute"
                                            variant="dark"
                                            style={{ right: "0", top: "0" }}
                                            onClick={() => {
                                                deleteNotification(singleNotification.id)
                                                setTimeout(() => {
                                                    getNotifications()
                                                }, 100);
                                            }}>
                                            <Trash className="d-flex" size="20" />
                                        </Button>
                                    </ListGroup.Item>
                                )
                            else
                                return (
                                    <ListGroup.Item key={singleNotification.id}>
                                        {singleNotification.message}
                                        <Button
                                            className="position-absolute"
                                            variant="success"
                                            style={{ right: "0", top: "0" }}
                                            onClick={() => {
                                                postFriendship(singleNotification.request_email)
                                                deleteNotification(singleNotification.id)
                                                createNotification(singleNotification.request_email)
                                                setTimeout(() => {
                                                    getNotifications()
                                                }, 3000);

                                            }}>
                                            <PersonPlusFill className="d-flex" size="20" />
                                        </Button>
                                        <Button
                                            className="position-absolute"
                                            variant="danger"
                                            style={{ right: "0", bottom: "0" }}
                                            onClick={() => {
                                                deleteNotification(singleNotification.id)
                                                setTimeout(() => {
                                                    getNotifications()
                                                }, 3000);
                                            }}>
                                            <PersonXFill className="d-flex" size="20" />
                                        </Button>
                                    </ListGroup.Item>
                                )
                        }))
                    else
                        setNotificationList(<ListGroup.Item>Brak nowych powiadomień</ListGroup.Item>)
                }).catch(error => {
                    console.log(error.message)
                })
        }
    }


    return (
        <div className="position-relative" style={{ "width": "7%" }}>
            <Button
                className="p-1 mr-5 float-right"
                style={{ "width": "30%" }}
                variant="outline-light"
                onClick={() => { setIsListHidden(true) }}>
                <Bell size="100%" />
            </Button>
            {isListHidden &&
                <ListGroup ref={wrapperRef} className="position-absolute" style={{ width: "20.7vw", right: "0", top: "45px" }}>
                    {notificationList}
                </ListGroup>
            }
        </div>
    )
}
