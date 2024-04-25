import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Image from 'react-bootstrap/Image';
import Col from 'react-bootstrap/Col';
import { Button } from 'react-bootstrap';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Comments from './Comments';
import './styles/LinkDigest.css';
import './Fit/Posts.css';
import './styles/buttonStyle.css';
import Badge from 'react-bootstrap/Badge';


const API_URL = 'http://localhost:8000';

const linkStyle = {
    color: '#2c70f5',
    textDecoration: 'none',
    background: '#101b3b',
    padding: '5px 10px',
    borderRadius: '5px',
  };

export default function LinkDigest() {

    const [digest, setDigest] = useState(null);
    const [comments, setCommets] = useState(null);
    const [saved, setSaved] = useState(false);
    const [wasDeleted, setWasDeleted] = useState(false);
    const params = useParams();
    const digestId = params.id;
    const navigate = useNavigate();

    
    
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    const user = userToken?.user;
    const bot_link = `https://t.me/dijust_bot?start=link_${digestId}`;

    const handleEditClick = (id) => {
        navigate(`/link-edit/${id}`);
    }

    const deleteDigest = (id) => {
        setWasDeleted(true)
        axios.delete(`http://127.0.0.1:8000/link-digest/delete/${id}/`, {headers: {"Authorization": "Token " + token}})
    }

    const handleSave = () => {
        if (!saved) {
            axios.post("http://127.0.0.1:8000/digest/save/", {
                "pk": digestId,
                "digest-type": "link-digest"

            }, {
                headers: {
                    "Authorization": "Token " + token
                }
            })
            setSaved(true)
        }
        else {
            axios.post("http://127.0.0.1:8000/digest/unsave/", {
                "pk": digestId,
                "digest-type": "link-digest"

            }, {
                headers: {
                    "Authorization": "Token " + token
                }
            })
            setSaved(false)
        }
    }

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/digest/comments/?pk=${digestId}&type=link`).then(res => setCommets(res.data));
    }, [])

    useEffect(() => {
        const url1 = `${API_URL}/link-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {setDigest(response.data)});
        
    }, [])

    let topics = digest !== null ? digest["general info"]["topic"]: '';
    let links = digest !== null ? digest["digest links"]: [];

    useEffect(() => {
        if (digest !== null) {
            console.log(digest["general info"]["saves"]);
            console.log(user);
            if (digest["general info"]["saves"].includes(user)) {
                console.log(user);
                setSaved(true);
            }
        }
    }, [digest])


    if (wasDeleted) {
        return (<div>Digest was successfully deleted</div>)
    }
   
   
    return(
    <>
        <div className='digest-info-id'>
        <p>{digest !== null ? digest["general info"]["name"] : ''}   |   {digest != null ? digest["general info"]["created_timestamp"].slice(0, 10): ''}</p>
        <p>Introduction:</p>
        <p>{digest !== null ? digest["general info"]["introduction"] : ''}</p>
        </div>
        <p style={{color: "white"}}>Topics:</p>
        <ul style={{color: "white"}}>
            {topics !== '' && topics.map(function(elem) {
                return <Badge bg="light" text="dark"><li>{elem}</li></Badge>
            })}
        </ul>
        <p style={{color: "white"}}>Links:</p>
        <ul>
            {links !== [] && links.map(function(elem) {
                return( 
                <div className='link-description-container'>
                    <a href={elem.link}>tap</a>
                    <p style={{color: "white"}}>{elem.description}</p>
                </div>)
            })}
        </ul>
        <p style={{color: "white"}}>Conclusion:</p>
        <p style={{color: "white"}}>{digest !== null ? digest["general info"]["conclusion"] : ''}</p>

        

        <Comments placement={"end"} name={"comments"} comments={comments !== null ? comments: []} type={"link"} digest={digestId}/>
        <button onClick={() => handleSave()} className='logout-button'>{saved ? "Unsave": "Save"}</button>

        
        {digest !== null && digest["general info"]["owner"] === user ? <>
        <button variant="outline-info" onClick={() => handleEditClick(digestId)} className='logout-button'>Edit digest</button>
        <button onClick={() => deleteDigest(digestId)} className='logout-button'>Delete</button>
        </>: ''} 
        <button className='logout-button'><a href={bot_link} style={linkStyle} >Remind me in telegram-bot</a></button>



    </>)

}