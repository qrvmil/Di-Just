import axios from 'axios';
import Posts from './Posts';
import Select from 'react-select';
import { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

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

function listOfImgDigests (info) {
    const keys = Object.keys(info);
   
    return axios.get(`${API_URL}/img-all/`, {params: info}).then(res => res.data)
    
}

function listOfLinkDigests (info) {
    return axios.get(`${API_URL}/link-all/`, {params: info}).then(res => res.data)

}



export default function Fit() {

    const [inputValue, setInputValue] = useState('');
    const [currentChoice, setCurrentChoice] = useState(null);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [digestType, setDigestType] = useState("img");
    const navigate = useNavigate();

    const changeDigest = () => {
        if (digestType == "img") {
            setDigestType("link")
        }
        else {
            setDigestType("img");
        }
    }

    const clickType = () => {
        navigate('/type');
    }
    

    const handleChange = (event) => {
        setInputValue(event.target.value);
      };

    const handleSelectChange = (selectedValues) => {
        setSelectedOptions(selectedValues);
    };

    const handleClick1 = () => {
        console.log(1);
        const topics = [];
        for (let i = 0; i < selectedOptions.length; i++) {
            topics.push(topics_dict[selectedOptions[i].label]);
        }
        console.log(topics);
        
        setCurrentChoice({type: "topics", content: topics});
    }
    const handleClick2 = () => {
        console.log(digestType);
        setCurrentChoice({type: "owner", content: inputValue});
        setInputValue('');
    }
    const handleClick3 = () => {
        setCurrentChoice({type: "time", content: "old"});
    }
    const handleClick4 = () => {
        setCurrentChoice({type: "time", content: "new"});
    }


    return (
    <>
    
    <Button variant="info" onClick={clickType}>Create digest</Button>
    <h2 style={{color: "white"}}>List of digests</h2>
    <button onClick={changeDigest}>Change for {digestType == "img" ? "link": "image"} digest</button>
    
    <p style={{color: "white"}}>Sort by:</p>
    <div >
    <div>
        <input type="text" value={inputValue} onChange={handleChange} /> <button onClick={handleClick2}>go</button>
        <p style={{color: "white"}}>Owner name: {inputValue}</p>
    </div>
    
    <div>
        <p style={{color: "white"}}>Topics:</p> <button onClick={() => handleClick1()}>go</button> 
        <Select
        value={selectedOptions}
        onChange={handleSelectChange}
        options={topics_names}
        isMulti
        /> 
        
        
    </div>
    
    <div>
        <p style={{color: "white"}}>Time</p> <button onClick={() => handleClick3()}>Old</button> <button onClick={() => handleClick4()}>New</button>
    </div>
    {currentChoice !== null ? <Posts digestType = {digestType} type = {currentChoice["type"]} content = {currentChoice["content"]}/>: ' '}
    </div>
    </>
    )
    

}