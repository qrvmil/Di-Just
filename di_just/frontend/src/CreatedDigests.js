import axios from 'axios';
import { useState, useEffect } from 'react';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import './Fit/Posts.css';
const API_URL = 'http://localhost:8000';


// 👇️ get ID from url
function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}


function CreatedDigests() {

    const [createdImgDigests, setCreatedImgDigests] = useState([]);
    const [createdLinkDigests, setCreatedLinkDigests] = useState([]);
    const [digestType, setDigestType] = useState(true); // true === image dagest, false === link digest :)
    const navigate = useNavigate();

    const handleClick = () => {
        setDigestType(!digestType);
    }

   

    const goToImageDigest = (id) => {
        navigate(`/img-digest/${id}/`);

    }

    const goToLinkDigest = (id) => {
        navigate(`/link-digest/${id}/`);
    }

    // add function get topic by id

   

    let current_info;
    if (digestType) {
        current_info = [...createdImgDigests];
    }
    else {
        current_info = [...createdLinkDigests]
    }


    useEffect(() => {
        
        
        const userId = getUserId();
        const url1 = `${API_URL}/img-digest/user/${userId}/`;
        const url2 = `${API_URL}/link-digest/user/${userId}/`;
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
        axios.get(url1, {
            headers: {
                "Authorization" : "Token " + token}}).then(response => {setCreatedImgDigests(response.data)});
        axios.get(url2, {
            headers: {
                "Authorization" : "Token " + token}}).then(response => {setCreatedLinkDigests(response.data)});
        console.log(createdImgDigests);
        console.log(createdLinkDigests);
        //console.log(userInfo);
    }, [])
    
    // TODO: add creator username to every digest
    // TODO: add digest pages to every digest

    return (
    <>
        <Alert variant={"info"} className="d-none d-lg-block">Created digests:</Alert>
        <Button variant="outline-info" onClick={handleClick}>Change for {digestType ? "link": "image"} digests</Button>
        <div className='wrapper'>
        {current_info.map((element) => 
                <div>
                    <Card>
                        <Card.Header>{element.owner}  |   {element.created_timestamp.slice(0, 10)}</Card.Header>
                        <Card.Body>
                            <Card.Title>{element.name}</Card.Title>
                            <Card.Text>
                            {element.introduction}
                            </Card.Text>
                            <Button variant="primary" onClick={() => digestType ? goToImageDigest(element.id): goToLinkDigest(element.id)}>Dive to digest</Button>
                        </Card.Body>
                    </Card>

                </div>
        )}
        
       </div>
    </>
    )

}

export default CreatedDigests;