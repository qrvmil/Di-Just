import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Image from 'react-bootstrap/Image';
import Col from 'react-bootstrap/Col';
import { Button } from 'react-bootstrap';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Comments from './Comments';



const API_URL = 'http://localhost:8000';


export default function LinkDigest() {

    const [digest, setDigest] = useState(null);
    const params = useParams();
    const digestId = params.id;

    
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const [comments, setCommets] = useState(null);
    const token = userToken?.token;
    const navigate = useNavigate();

    const handleEditClick = (id) => {
        navigate(`/link-edit/${id}`);
    }

    function getComments() {
        axios.get(`digest/comments/${digestId}/`, {params: {type: "link"}}).then(res => setCommets(res.data))

    }

    useEffect(() => {
        const url1 = `${API_URL}/link-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {setDigest(response.data)});
        
    }, [])

    let topics = digest !== null ? digest["general info"]["topic"]: '';
    let links = digest !== null ? digest["digest links"]: [];
    const user = userToken?.user;
   
    return(
    <>
        <p>Image digest {digestId}</p>
        <p>{digest !== null ? digest["general info"]["name"] : ''}   |   {digest != null ? digest["general info"]["created_timestamp"].slice(0, 10): ''}</p>
        <p>{digest !== null ? digest["general info"]["introduction"] : ''}</p>
        
        <p>Topics:</p>
        <ul>
            {topics !== '' && topics.map(function(elem) {
                return <li>{elem}</li>
            })}
        </ul>
        <p>Links:</p>
        <ul>
            {links !== [] && links.map(function(elem) {
                return( 
                <li>
                    <a href={elem.link}>{elem.link}</a>
                    <p>{elem.description}</p>
                </li>)
            })}
        </ul>

        <p>{digest !== null ? digest["general info"]["conclusion"] : ''}</p>

        <Comments placement={"end"} name={"comments"} comments={comments} type={"link"}/>


        {digest !== null && digest["general info"]["owner"] === user ? <Button variant="outline-info" onClick={() => handleEditClick(digestId)}>Edit digest</Button>: ''}






    </>)

}