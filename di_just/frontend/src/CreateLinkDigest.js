import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Image from 'react-bootstrap/Image';
import { useState, useRef } from "react";
import axios from 'axios';
import Select from 'react-select';
import './styles/EditImg.css';
import './styles/buttonStyle.css';
import { BrowserRouter, Routes, Route, Link, redirect, useNavigate} from 'react-router-dom';

const API_URL = 'http://localhost:8000';

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
    const [isChecked, setIsChecked] = useState(false);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const navigate = useNavigate();


    const handleLinkChange = (event, index) => {
        let data = [...formLink];
        data[index] = event.target.value;
        setFormLink(data);
    }

    const handleCheckboxChange = (event) => {
        setIsChecked(event.target.checked);
    };

    const handleDescChange = (event, index) => {
        let data = [...formDesc];
        data[index] = event.target.value;
        setFormDesc(data);
    }

    const handleSelectChange = (selectedValues) => {
        setSelectedOptions(selectedValues);
    };

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
        formDataReq.append('public', isChecked);
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

        for (let i = 0; i < selectedOptions.length; i++) {
            formDataReq.append('topic', topics_dict[selectedOptions[i].label]);
        }

        selectedOptions.forEach((item) => {
            formDataReq.append(`topics`, item);
        });


        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;

        axios.post(`http://127.0.0.1:8000/link-digest/create/`, formDataReq, {headers: {"Authorization" : "Token " + token, 'Content-Type': 'multipart/form-data'}})
            .then(res => {
                console.log(res);
                console.log(res.data);},
        )

       navigate('/profile')
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
            <Form onSubmit={submit} style={{ maxWidth: '600px', margin: 'auto'}} className="edit-img-form">

            
            <input name='name' type='text' placeholder='name' onChange={event => handleName(event)}></input>
            <input name='introduction' type='text' placeholder='introduction' onChange={event => handleIntroduction(event)}></input>
            <p style={{color: "white"}}>Topics:</p>
            <Select
                value={selectedOptions}
                onChange={handleSelectChange}
                options={topics_names}
                isMulti
            />
            <div>
                {formLink.map((form, index) => {
                    return (<div key={index}>
                        <Image src={formLink[index] !== null ? formLink[index]: ''} rounded />
                        <input name='link' type='text' placeholder='link' onChange={event => handleLinkChange(event, index)}/>
                        <input name='description' placeholder='description' onChange={event => handleDescChange(event, index)}/>
                        <Button variant="primary" onClick={() => removeFields(index)}>
                        delete
                        </Button>
                        </div>) 
                })}

            </div>
            

            <input name='conclusion' type='text' placeholder='conclusion' onChange={event => handleConclusion(event)}></input>


            <input
                type="checkbox"
                checked={isChecked}
                onChange={handleCheckboxChange}
            />
            <label style={{color: "white"}}>Public</label>

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