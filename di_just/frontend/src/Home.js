import axios from 'axios';
import { useState } from 'react';
const API_URL = 'http://localhost:8000';

function getUsersProfiles() {
    const url = `${API_URL}/users/profiles/`;
    
    return axios.get(url).then(response => response.data[0].user);
} 

function Home() {

    const [Username, setUsername] = useState();

    getUsersProfiles().then(function(res){ 
        console.log(res);
        setUsername(res);
    });
    console.log(Username);

    return (
    <>
        <p>Hi! {Username}</p>
    </>
    )

}

export default Home;