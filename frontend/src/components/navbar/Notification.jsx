import { Button, ListGroup, ListGroupItem } from 'react-bootstrap';
import React, { useState, useEffect, useRef } from 'react'
import { Bell,  PersonPlusFill, PersonXFill, Trash} from 'react-bootstrap-icons';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react'

export default function Notification() {
    const [isListHidden, setIsListHidden] = useState(false);
    const [notificationList, setNotificationList] = useState(<ListGroup.Item>Brak nowych powiadomień</ListGroup.Item>);
    const wrapperRef = useRef(null);
    const { user } = useAuth0();

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
                                            onClick={() => console.log("smiec")}>
                                            <Trash className="d-flex" size="20"/>
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
                                            onClick={() => console.log("Dodaj")}>
                                            <PersonPlusFill className="d-flex" size="20"/>
                                        </Button>
                                        <Button 
                                            className="position-absolute" 
                                            variant="danger" 
                                            style={{ right: "0", bottom: "0" }}
                                            onClick={() => console.log("usun")}>
                                            <PersonXFill className="d-flex" size="20"/>
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
