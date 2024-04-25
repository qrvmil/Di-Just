import axios from 'axios';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import { Routes, Route, useNavigate } from 'react-router-dom';
import useToken from './useToken';

const API_URL = 'http://localhost:8000';


function getUsersProfiles() {
    const url = `${API_URL}/users/profiles/`;
    
    return axios.get(url).then(response => response.data[0].user);
} 

function Home() {
    

    const navigate = useNavigate();

    const clickType = () => {
        navigate('/type');
    }

    const [Username, setUsername] = useState();

    getUsersProfiles().then(function(res){ 
        console.log(res);
        setUsername(res);
    });
    console.log(Username);

    return (
    <>
        <Button variant="info" onClick={clickType}>Create digest</Button>
        <p>Hi! {Username}</p>
    </>
    )

}

export default Home;