import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import { useState, useRef } from "react";
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}

 
export default function CreateLinkDigest () {

    const [formLink, setFormLink] = useState([
        null
    ]);
    const [formDesc, setFormDesc] = useState([
        ''
    ]);
    const [name, setName] = useState('');
    const [introduction, setIntroduction] = useState('');
    const [conclusion, setConclusion] = useState('');


    const handleLinkChange = (event, index) => {
        let data = [...formLink];
        data[index] = event.target.value;
        setFormLink(data);
    }
    const handleDescChange = (event, index) => {
        let data = [...formDesc];
        data[index] = event.target.value;
        setFormDesc(data);
    }

    const handleName = (event) => {
        setName(event.target.value);
    }


    const handleIntroduction = (event) => {
        setIntroduction(event.target.value);
    }

    const handleConclusion = (event) => {
        setConclusion(event.target.value);
    }

    const submit = (e) => {
        e.preventDefault();
        console.log(e.target);
        let formDataReq = new FormData();
        formDataReq.append('name', name);
        formDataReq.append('introduction', introduction);
        formDataReq.append('conclusion', conclusion);
        console.log(name, introduction, conclusion);
        for (var key of formDataReq.entries()) {
            console.log(key);
        }
             
        
        console.log(formLink);
        console.log(formDesc);
        formLink.forEach((item) => {
            formDataReq.append(`links`, item);
          });

        formDesc.forEach((item) => {
            formDataReq.append(`descriptions`, item);
        });


        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;

        axios.post(`http://127.0.0.1:8000/link-digest/create/`, formDataReq, {headers: {"Authorization" : "Token " + token, 'Content-Type': 'multipart/form-data'}})
            .then(res => {
                console.log(res);
                console.log(res.data);},
    )

       
    }

    const addFields = () => {
        
        let link = null;
        let description = '';

        setFormLink([...formLink, link]);
        setFormDesc([...formDesc, description])



    }

    const removeFields = (index) => {

        let data1 = [...formLink];
        data1.splice(index, 1);
        setFormLink(data1);

        let data2 = [...formDesc];
        data2.splice(index, 1);
        setFormDesc(data2);

    }
    


    return (
        <>
            <Form onSubmit={submit}>

            
            <input name='name' type='text' placeholder='name' onChange={event => handleName(event)}></input>
            <input name='introduction' type='text' placeholder='introduction' onChange={event => handleIntroduction(event)}></input>
            <div>
                {formLink.map((form, index) => {
                    return (<div key={index}>
                        <Image src={formLink[index] !== null ? formLink[index]: ''} rounded />
                        <input name='picture' type='text' placeholder='link' onChange={event => handleLinkChange(event, index)}/>
                        <input name='description' placeholder='description' onChange={event => handleDescChange(event, index)}/>
                        <Button variant="primary" type="submit" onClick={() => removeFields(index)}>
                        delete
                        </Button>
                        </div>) 
                })}

            </div>
            

            <input name='conclusion' type='text' placeholder='conclusion' onChange={event => handleConclusion(event)}></input>


                <Form.Group className="mb-3" controlId="public">
                    <Form.Check type="checkbox" label="Private digest" />
                </Form.Group>

                <Button variant="primary" type="submit">
                Submit
                </Button>
            </Form>
            <Button variant="primary" type="submit" onClick={addFields}>
            Add more...
            </Button>
            

        </>
    )
}