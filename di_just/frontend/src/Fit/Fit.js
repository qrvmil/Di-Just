import axios from 'axios';
import Posts from './Posts';
import Select from 'react-select';
import { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';



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
    
    <h2 style={{color: "white"}}>List of digests</h2>
    <Button variant="outline-info" onClick={changeDigest}>Change for {digestType == "img" ? "link": "image"} digest</Button>
    
    
    <Container>
    <Row>
    <Col xs={4}>
    <p style={{color: "white"}}>Sort by:</p>

    
    <ListGroup>
        <ListGroup.Item variant="info">
            <div>
                <div className="fw-bold">Name</div>
                <input type="text" value={inputValue} onChange={handleChange} />
                <Button variant="outline-dark" onClick={handleClick2}>go</Button>
            </div>
        </ListGroup.Item>
    
        <ListGroup.Item variant="info">
        <div>
            <div className="fw-bold">Topics:</div>
            <Select
            value={selectedOptions}
            onChange={handleSelectChange}
            options={topics_names}
            isMulti
            /> 
            <Button variant="outline-dark" onClick={() => handleClick1()}>go</Button>
        </div>
        </ListGroup.Item>
    
    <ListGroup.Item variant="info">
    <div>
        <div className="fw-bold">Time:</div>
        <Button variant="outline-dark" onClick={() => handleClick3()}>Old</Button> <Button variant="outline-dark" onClick={() => handleClick4()}>New</Button>
    </div>
    </ListGroup.Item>
    </ListGroup>
    </Col>

    

    <Col md="8">
    {currentChoice !== null ? <Posts digestType = {digestType} type = {currentChoice["type"]} content = {currentChoice["content"]}/>: ' '}
    </Col>
    </Row>
    </Container>

    <Button variant="outline-info" onClick={clickType}>Create digest</Button>
    

    </>
    )
    

}