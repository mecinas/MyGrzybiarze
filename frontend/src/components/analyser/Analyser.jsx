import React, { useRef, useState, useEffect } from 'react'
import { Col, Image, Button } from 'react-bootstrap'
import axios from 'axios'

export default function Analyser() {

    const hiddenFileInput = React.useRef(null);
    const [photo, setPhoto] = useState();
    const [edibleData, setEdibleData] = useState();
    const [speciesData, setSpeciesData] = useState();

    const handleFileInputClick = e => {
        hiddenFileInput.current.click();
    }

    const handleFileInputChange = e => {
        const photoUploaded = e.target.files[0];
        setPhoto(photoUploaded)
        const data = new FormData();
        data.append('mushroom_image', photoUploaded)
        checkMushroom(data)
    }

    const checkMushroom = (data) => {
        var edible_url = "http://localhost:5000/analyser/edible"
        var species_url = "http://localhost:5000/analyser/species"
        postMushroom(data, edible_url, setEdibleData)
        postMushroom(data, species_url, setSpeciesData)
    }

    const postMushroom = (data, url, setData) => {
        axios.post(url, data, {
            headers: {
                'accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.8',
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
            }
        }).then(response => {
            setData(response.data)
        })
            .catch(error => {
                console.log(error.message)
            })
    }

    useEffect(() => {
        if (edibleData && speciesData) {
            console.log(photo)
            console.log(edibleData)
            console.log(speciesData)
        }
    }, [edibleData, speciesData])
    return (
        <div>
            <Button variant="light" onClick={handleFileInputClick} >
                Wybierz grzyb do analizy
                <input
                    type="file"
                    ref={hiddenFileInput}
                    onChange={handleFileInputChange}
                    name="myImage"
                    style={{ display: 'none' }} />
            </Button>
        </div>
    )
}
