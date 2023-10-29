import axios from 'axios';
import getToken from './App';
import { useState } from "react";
import { useEffect } from 'react';

const API_URL = 'http://localhost:8000';

// axios.defaults.withCredentials = true;


// get user id
function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}

// get user info 

//get profile info

function Profile() {

    const [userInfo, setUserInfo] = useState(null);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        
        const userId = getUserId();
        const url = `${API_URL}/users/user/${userId}/`;
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
        axios.get(url, {
            headers: {
                  "Authorization" : "Token " + token}}).then(response => {setUserInfo(response.data)});
        
        //console.log(userInfo);
    }, [])
    console.log(userInfo);
   
    return (
    <>
        <p>Profile! {userInfo != null ? userInfo.username: "Anonym"}</p>
        <p>User info: </p>
    </>
    )

}


export default Profile;