import React, { useRef, useState, useEffect } from 'react'
import { Card, Jumbotron, Button } from 'react-bootstrap'
import axios from 'axios'

export default function Analyser() {

    const hiddenFileInput = React.useRef(null);
    const [photo, setPhoto] = useState();
    const [edibleData, setEdibleData] = useState();
    const [speciesData, setSpeciesData] = useState();
    const [color, setColor] = useState()

    const handleFileInputClick = e => {
        hiddenFileInput.current.click();
    }

    const handleFileInputChange = e => {
        const photoUploaded = e.target.files[0];
        readFileDataAsBase64(photoUploaded)
        const data = new FormData();
        data.append('mushroom_image', photoUploaded)
        checkMushroom(data)
    }

    function readFileDataAsBase64(file) {
        const fileToArrayBuffer = require('file-to-array-buffer')
        fileToArrayBuffer(file).then((data) => {
            setPhoto(encodeImage(data))
        })
    }

    function encodeImage(arrayBuffer) {
        let b64encoded = btoa([].reduce.call(new Uint8Array(arrayBuffer), function (p, c) { return p + String.fromCharCode(c) }, ''))
        let mimetype = "image/png"
        return "data:" + mimetype + ";base64," + b64encoded
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
        if (edibleData) {
            if(edibleData[0]["tag_name"] === "jadalny"){
                setColor("forestGreen")
            }else
                setColor("red")
        }
    }, [edibleData])

    var mushroomButton = (
        <Button className="d-flex mx-auto" variant="info" onClick={handleFileInputClick} >
            Wybierz grzyb do analizy
            <input
                type="file"
                ref={hiddenFileInput}
                onChange={handleFileInputChange}
                name="myImage"
                style={{ display: 'none' }} />
        </Button>
    )
    const B = (props) => <h5 style={{fontWeight: 'bold', color: `${color}`}}>{props.children}</h5>

    return (
        <div className="mt-5" style={{fontFamily: 'Helvetica'}}>
            {!photo && mushroomButton}
            {photo && edibleData && speciesData &&
                <Card className="d-flex mx-auto mt-5" style={{ width: '25rem' }}>
                    <Card.Img variant="top" src={photo} />
                    <Card.Body>
                        <Card.Title style={{backgroundColor: `${color}`}}>
                            <h3 className="px-5" >{speciesData[0]["tag_name"]}</h3>
                        </Card.Title>
                            <h5 className="px-5" >Załączony grzyb jest: <B>{edibleData[0]["tag_name"]}</B></h5>
                        <Card.Footer className="w-100" style={{ width: "100%" }}>
                            {mushroomButton}
                        </Card.Footer>
                    </Card.Body>
                </Card>
            }
        </div>
    )
}
