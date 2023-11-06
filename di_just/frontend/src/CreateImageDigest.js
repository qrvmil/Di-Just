import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import Select from 'react-select';
import { useState, useRef } from "react";
import { BrowserRouter, Routes, Route, Link, redirect, useNavigate} from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}

// TODO: отображание картинокч

const topics_dict = {
    "Cinema": 13,
	"Music": 12,
	"Technologies": 11,
	"Memes": 10,
	"Animals": 9,
	"Travelling": 8,
	"Food": 7,
	"Education": 6,
	"News": 5,
	"Math": 4,
	"Computer Science" : 3,
	"Sport": 2,
	"Art": 1
}

const topics_names = [
    { value: 'Cinmea', label: 'Cinema' },
    { value: 'Music', label: 'Music' },
    { value: 'Animals', label: 'Animals' },
    { value: 'Technologies', label: 'Technologies' },
    { value: 'Memes', label: 'Memes' },
    { value: 'Travelling', label: 'Travelling' },
    { value: 'Food', label: 'Food' },
    { value: 'Education', label: 'Education' },
    { value: 'News', label: 'News' },
    { value: 'Math', label: 'Math' },
    { value: 'Computer Science', label: 'Computer Science' },
    { value: 'Sport', label: 'Sport' },
    { value: 'Art', label: 'Art' },
]

 
export default function CreateImageDigest () {

    const [formImage, setFormImage] = useState([
        null
    ]);
    const [formDesc, setFormDesc] = useState([
        ''
    ]);
    const [name, setName] = useState('');
    const [introduction, setIntroduction] = useState('');
    const [conclusion, setConclusion] = useState('');
    const [selectedOptions, setSelectedOptions] = useState([]);
    const navigate = useNavigate();


    const handleImageChange = (event, index) => {
        let data = [...formImage];
        data[index] = event.target.files[0];
        setFormImage(data);
    }

    const handleSelectChange = (selectedValues) => {
        setSelectedOptions(selectedValues);
    };

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
        for (let i = 0; i < selectedOptions.length; i++) {
            formDataReq.append('topic', topics_dict[selectedOptions[i].label]);
        }
             
        let pictures = [];
        let descriptions = [];
        //formFields.map((elem) => {
            //pictures.push(elem.picture);
            //descriptions.push(elem.description);
        //})
        
        
        formImage.forEach((item) => {
            formDataReq.append(`pictures`, item);
          });

        formDesc.forEach((item) => {
            formDataReq.append(`descriptions`, item);
        });

        selectedOptions.forEach((item) => {
            formDataReq.append(`topics`, item);
        });


        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;

        axios.post(`http://127.0.0.1:8000/img-digest/create/`, formDataReq, {headers: {"Authorization" : "Token " + token, 'Content-Type': 'multipart/form-data'}})
            .then(res => {
                console.log(res);
                console.log(res.data);},
            )
        navigate('/profile')
       
        }

    const addFields = () => {
        
        let picture = null;
        let description = '';

        setFormImage([...formImage, picture]);
        setFormDesc([...formDesc, description])



    }

    const removeFields = (index) => {

        let data1 = [...formImage];
        data1.splice(index, 1);
        setFormImage(data1);
        
        let data2 = [...formDesc];
        data2.splice(index, 1);
        setFormDesc(data2);

    }
    
   


    return (
        <>
            <Form onSubmit={submit} style={{ maxWidth: '600px', margin: 'auto'}}>

            
            <input name='name' type='text' placeholder='name' onChange={event => handleName(event)}></input>
            <input name='introduction' type='text' placeholder='introduction' onChange={event => handleIntroduction(event)}></input>
            <p>Topics:</p>
            <Select
                value={selectedOptions}
                onChange={handleSelectChange}
                options={topics_names}
                isMulti
            />
            <div>
                {formImage.map((form, index) => {
                    return (<div key={index}>
                        <Image src={formImage[index] !== null ? 'http://127.0.0.1:8000/' + formImage[index].name: ''} rounded />
                        
                        <input name='picture' type='file' placeholder='picture' onChange={event => handleImageChange(event, index)}/>
                        <input name='description' placeholder='description' onChange={event => handleDescChange(event, index)}/>
                        <Button variant="primary" onClick={() => removeFields(index)}>
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