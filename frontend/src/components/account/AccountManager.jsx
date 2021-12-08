import React from 'react'
import axios from 'axios'
import {useAuth0} from '@auth0/auth0-react'
import { Container, Row,} from 'react-bootstrap'
import {useHistory} from 'react-router-dom'

import '../../styles/account/AccountManager.css';
import UserInfoTable from './UserInfoTable'
import UserAvatar from './UserAvatar'

export default function AccountManager() {
    const { user } = useAuth0();
    let history = useHistory();

    const putAvatar = (data, setSource, encodeImage) => {
        var url = "http://localhost:5000/account/change/avatar"
        axios.put(url, data, {
            headers: {
                'accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.8',
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
            }
        })
            .catch(error => {
                console.log(error.message)
            })
        setTimeout(() => {
            getAvatar(setSource, encodeImage)
        }, 2000);
    }

    const getAvatar = (setSource, encodeImage) => {
        const time = new Date().getTime(); //To make sure that request will execute despite cache photo memory
        var url = "http://localhost:5000/account/avatar"
        if (user !== undefined) {
            axios.get(url, {
                responseType: 'arraybuffer',
                params: {
                    email: user.email,
                    t: time
                }
            })
                .then(response => {
                    setSource(encodeImage(response.data))
                })
                .catch(error => {
                    console.log(error.message)
                })
        }
    }

    const deleteUser = () => {
        var url = "http://localhost:5000/register"
        axios.delete(url, { data: { email: user.email } })
            .then(response => {
            })
            .catch(error => {
                console.log(error.message)
            })
        history.push("/")
    }

    const getInfo = (setUserInfo) => {
        var url = "http://localhost:5000/user/single"
        if (user !== undefined) {
            axios.get(url, {
                params: {
                    email: user.email
                }
            })
                .then(resp => {
                    setUserInfo(resp.data)
                })
        }
    }

    return (
        <Container className="account_container">
            <Row>
                <UserAvatar getAvatar={getAvatar} putAvatar={putAvatar} />
            </Row>
            <Row>
                <UserInfoTable getInfo={getInfo} deleteUser={deleteUser} />
            </Row>
        </Container>

    )
}
