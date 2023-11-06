import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Image from 'react-bootstrap/Image';
import Col from 'react-bootstrap/Col';
import { Button } from 'react-bootstrap';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Comments from './Comments';
import './styles/ImgDigest.css';
import './Fit/Posts.css';
import './styles/buttonStyle.css';




const API_URL = 'http://localhost:8000';

const linkStyle = {
    color: '#2c70f5',
    textDecoration: 'none',
    background: '#101b3b',
    padding: '5px 10px',
    borderRadius: '5px',
  };


export default function ImgDigest() {

    const [digest, setDigest] = useState(null);
    const [comments, setCommets] = useState(null);
    const [saved, setSaved] = useState(false);
    const [wasDeleted, setWasDeleted] = useState(false);
    const params = useParams();
    const digestId = params.id;
    const navigate = useNavigate();
    const bot_link = `https://t.me/dijust_bot?start=img_${digestId}`;



    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    const user = userToken?.user;


    const handleEditClick = (id) => {
        navigate(`/img-edit/${id}`);
    }

    const deleteDigest = (id) => {
        setWasDeleted(true);
        axios.delete(`http://127.0.0.1:8000/img-digest/delete/${id}/`, {headers: {"Authorization": "Token " + token}})
    }
    
    const handleSave = () => {
        if (!saved) {
            axios.post("http://127.0.0.1:8000/digest/save/", {
                "pk": digestId,
                "digest-type": "img-digest"

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
                "digest-type": "img-digest"

            }, {
                headers: {
                    "Authorization": "Token " + token
                }
            })
            setSaved(false)
        }
    }

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/digest/comments/?pk=${digestId}&type=img`).then(res => setCommets(res.data));
    }, [])

    

    useEffect(() => {
        const url1 = `${API_URL}/img-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {setDigest(response.data)});

    }, [])

    let topics = digest !== null ? digest["general info"]["topic"]: '';
    let images = digest !== null ? digest["digest images"]: [];
    
    
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
        <p>{digest !== null ? digest["general info"]["introduction"] : ''}</p>
        
        <p>Topics:</p>
        <ul>
            {topics !== '' && topics.map(function(elem) {
                return <li>{elem}</li>
            })}
        </ul>
        </div>
        <p style={{color: "white"}}>Images:</p>
        <div className='wrapper'>
        <ul>
            {images !== [] && images.map(function(elem) {
                return( 
                    <div className="image-container-id">
                        <img src={'http://localhost:8000/' + elem.picture} alt={"description"} className="image-id" />
                        <p className="description-id">{elem.description}</p>
                    </div>
                )
            })}
        </ul>
        </div>

        <Comments placement={"end"} name={"comments"} comments={comments !== null ? comments: []} type={"image"} digest={digestId}/> <button onClick={() => handleSave()} className='logout-button'>{saved ? "Unsave": "Save"}</button>

        {digest !== null && digest["general info"]["owner"] === user ? <>
        <Button variant="outline-info" onClick={() => handleEditClick(digestId)} className='logout-button'>Edit digest</Button>
        <button onClick={() => deleteDigest(digestId)} className='logout-button'>Delete</button>
        </>: ''} 
        <a href={bot_link} style={linkStyle} >Remind me in telegram-bot</a>



        

    </>)

}