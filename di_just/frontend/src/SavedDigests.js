import axios from 'axios';
import { useState } from 'react';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
const API_URL = 'http://localhost:8000';


function SavedDigests() {

    return (
    <>
        <Alert variant={"info"} className="d-none d-lg-block">Saved digests:</Alert>
       
    </>
    )

}

export default SavedDigests;