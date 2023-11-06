import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import { useState, useRef, useEffect } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {Routes, Route, useNavigate} from 'react-router-dom';



const API_URL = 'http://localhost:8000';

function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}


export default function EditLinkDigest() {
    const [formLink, setFormLink] = useState([]);
    const [formDesc, setFormDesc] = useState([
        ''
    ]);
    const [name, setName] = useState('');
    const [introduction, setIntroduction] = useState('');
    const [conclusion, setConclusion] = useState('');
    const params = useParams();
    const digestId = params.id;
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    const navigate = useNavigate();
    const [digest, setDigest] = useState(null);
    



    useEffect(() => {
        const url1 = `${API_URL}/link-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {
            setDigest(response.data);
            })
        
    }, [])


    const handleLinkChange = (event, index) => {
        digest["digest links"][index]["link"] = event.target.value;
    }
    const handleDescChange = (event, index) => {
        digest["digest links"][index]["description"] = event.target.value;
    }

    const handleName = (event) => {
        digest["general info"]["name"] = event.target.value;
    }


    const handleIntroduction = (event) => {
        digest["general info"]["introduction"] = event.target.value;
    }

    const handleConclusion = (event) => {
        digest["general info"]["conclusion"] = event.target.value;
    }

    const submit = (e) => {
        e.preventDefault();

        let updates = {
            updates: []
            
        };
        digest["digest links"].map(function(elem) {
            let update = {
                pk: elem["id"],
                description: elem["description"],
                link: elem["link"]
            }
            updates = {
                updates: [
                    ...updates.updates,
                    update
                ]
            }
        });


        
        let formData= new FormData();
        formData.append('updates', JSON.stringify(updates));
        formData.append('name', digest["general info"]["name"]);
        formData.append('introduction', digest["general info"]["introduction"]);
        formData.append('conclusion', digest["general info"]["conclusion"]);

        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;

        axios.put(`http://127.0.0.1:8000/link-digest/update/${digestId}/`, formData, {headers: {"Authorization" : "Token " + token}})
            .then(res => {
                console.log(res);
                console.log(res.data);});

        navigate(`/link-digest/${digestId}/`)
       
    }

 
    


    return (
        <>
            <Form onSubmit={submit} style={{maxWidth: '600px', margin: 'auto'}}>

            
            <input name='name' type='text' placeholder={digest !== null ? digest["general info"]["name"]: ' '} onChange={event => handleName(event)}></input>
            <input name='introduction' type='text' placeholder={digest !== null ? digest["general info"]["introduction"]: ' '} onChange={event => handleIntroduction(event)}></input>
            <div>
                {(digest !== null) ? digest["digest links"].map((form, index) => {
                    return (<div key={index}>
                        <input name='picture' type='text' placeholder={form["link"]} onChange={event => handleLinkChange(event, index)}/>
                        <input name='description' placeholder={form["description"]} onChange={event => handleDescChange(event, index)}/>
                        
                        </div>) 
                }): ' '}

            </div>
            

            <input name='conclusion' type='text' placeholder='conclusion' onChange={event => handleConclusion(event)}></input>


                <Form.Group className="mb-3" controlId="public">
                    <Form.Check type="checkbox" label="Private digest" />
                </Form.Group>

                <Button variant="primary" type="submit">
                Submit
                </Button>
            </Form>
            
            

        </>
    )
}