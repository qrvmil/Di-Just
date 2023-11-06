import { useState, useEffect } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import { useRef } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {Routes, Route, useNavigate} from 'react-router-dom';


const API_URL = 'http://localhost:8000';

function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}






export default function EditImgDigest() {
    // call your hook here
    const navigate = useNavigate();
    const [formImage, setFormImage] = useState([
        null
    ]);
    const [digest, setDigest] = useState(null);
    const [change, setChange] = useState(true);
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

   
    useEffect(() => {

        const url1 = `${API_URL}/img-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {
            setDigest(response.data);
            
        });

        

    }, [])


    // update digest with current image
    const handleImageChange = (event, index, id) => {
        let updates = {
            updates: [
                {
                    pk: id,
                    type: "picture",
                    picture: 0
                }
            ]
            
        };
        digest["digest images"].map(function(elem) {
            let update = {
                pk: elem["id"],
                type: "description",
                description: elem["description"]
            }
            updates = {
                updates: [
                    ...updates.updates,
                    update
                ]
            }
        });
        let img = event.target.files[0];
        let formData = new FormData();
        formData.append('updates', JSON.stringify(updates));
        formData.append('pictures', img);
        formData.append('pictures', img);
        formData.append('name', digest["general info"]["name"]);
        formData.append('introduction', digest["general info"]["introduction"]);
        formData.append('conclusion', digest["general info"]["conclusion"]);


        


        axios.put(`http://127.0.0.1:8000/img-digest/update/${digestId}/`, formData, {headers: {"Authorization" : "Token " + token}})
            .then(res => {
                console.log(res);
                console.log(res.data);});

        const url1 = `${API_URL}/img-digest/get/${digestId}/`;
        axios.get(url1, {headers: {"Authorization" : "Token " + token}}).then(response => {
            setDigest(response.data);
            
        });
        
        setChange(!change);
        window.location.reload();
        
    }
    const handleDescChange = (event, index) => {
        digest["digest images"][index]["description"] = event.target.value;
        
    }

    const handleName = (event) => {
        digest["general info"]["name"] = event.target.value;
    }


    const handleIntroduction = (event) => {
        digest["general info"]["introduction"] = event.target.value;
    }

    const handleConclusion = (event) => {
        digest["digest images"]["conclusion"] = event.target.value;
    }

    const submit = (e) => {
        e.preventDefault();
        let updates = {
            updates: []
        }
        digest["digest images"].map(function(elem) {
            let update = {
                pk: elem["id"],
                type: "description",
                description: elem["description"]
            }
            updates = {
                updates: [
                    ...updates.updates,
                    update
                ]
            }
        });
        let formData = new FormData();
        formData.append('updates', JSON.stringify(updates));
        
        formData.append('name', digest["general info"]["name"]);
        formData.append('introduction', digest["general info"]["introduction"]);
        formData.append('conclusion', digest["general info"]["conclusion"]);



        


        axios.put(`http://127.0.0.1:8000/img-digest/update/${digestId}/`, formData, {headers: {"Authorization" : "Token " + token}})
            .then(res => {
                console.log(res);
                console.log(res.data);});

        navigate(`/img-digest/${digestId}/`)

       
    }
    
   


    return (
        <>
            <Form onSubmit={submit} style={{maxWidth: '600px', margin: 'auto'}}>

            
            <input name='name' type='text' placeholder={digest !== null ? digest["general info"]["name"]: ' '} onChange={event => handleName(event)}></input>
            <input name='introduction' type='text' placeholder={digest !== null ? digest["general info"]["introduction"]: ' '} onChange={event => handleIntroduction(event)}></input>
            <div>
                {digest !== null ? digest["digest images"].map((form, index) => {
                    return (<div key={index}>
                        <Image src={'http://127.0.0.1:8000/' + form["picture"]} rounded />
                        
                        <input name='picture' type='file' placeholder='picture' onChange={event => handleImageChange(event, index, form["id"])}/>
                        <input name='description' placeholder={form["description"]} onChange={event => handleDescChange(event, index)}/>
                        </div>) 
                }): ' '}

            </div>
            

            <input name='conclusion' type='text' placeholder={digest !== null ? digest["general info"]["conclusion"]: ' '} onChange={event => handleConclusion(event)}></input>


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