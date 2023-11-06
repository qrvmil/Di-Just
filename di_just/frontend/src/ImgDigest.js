import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Image from 'react-bootstrap/Image';
import Col from 'react-bootstrap/Col';
import { Button } from 'react-bootstrap';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Comments from './Comments';




const API_URL = 'http://localhost:8000';


export default function ImgDigest() {

    const [digest, setDigest] = useState(null);
    const [comments, setCommets] = useState(null);
    const params = useParams();
    const digestId = params.id;
    const navigate = useNavigate();

    const handleEditClick = (id) => {
        navigate(`/img-edit/${id}`);
    }

    

    
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    const user = userToken?.user;

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/digest/comments/?pk=${digestId}&type=img`).then(res => setCommets(res.data));
    }, [])

    

    useEffect(() => {
        const url1 = `${API_URL}/img-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {setDigest(response.data)});

    }, [])

    let topics = digest !== null ? digest["general info"]["topic"]: '';
    let images = digest !== null ? digest["digest images"]: [];
    

   
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
        <p>Images:</p>
        <ul>
            {images !== [] && images.map(function(elem) {
                return( 
                <li>
                    <p>{elem.picture}</p>
                    <img src={'http://localhost:8000/' + elem.picture} alter="help"/>
                    <p>{elem.description}</p>
                </li>)
            })}
        </ul>

        <Comments placement={"end"} name={"comments"} comments={comments !== null ? comments: []} type={"image"} digest={digestId}/>

        {digest !== null && digest["general info"]["owner"] === user ? <Button variant="outline-info" onClick={() => handleEditClick(digestId)}>Edit digest</Button>: ''}





    </>)

}