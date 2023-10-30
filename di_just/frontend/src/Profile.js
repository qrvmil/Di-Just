import axios from 'axios';
import getToken from './App';
import { useState } from "react";
import { useEffect } from 'react';
import Alert from 'react-bootstrap/Alert';
import { ListGroup } from 'react-bootstrap';
import Offcanvas from 'react-bootstrap/Offcanvas'
import Followers from './Followers.js';


const API_URL = 'http://localhost:8000';

// TODO: user+profile update
// TODO: followers/follows lists
// TODO: images

// axios.defaults.withCredentials = true;


// get user id
function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}

// get user profile id
function getUserProfileId() {
    const userId = getUserId();
    const url1 = `${API_URL}/users/user/${userId}/`;
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    return axios.get(url1, {
        headers: {
        "Authorization" : "Token " + token}}).then(response => {return response.data});
    

}


function Profile() {

    const [userInfo, setUserInfo] = useState(null);
    const [userId, setUserId] = useState(null);
    const [profileInfo, setProfileInfo] = useState(null);

    useEffect(() => {
        
        const userId = getUserId();
        const url1 = `${API_URL}/users/user/${userId}/`;
        const url2 = `${API_URL}/users/profile/${userId}/`;
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
        axios.get(url1, {
            headers: {
                "Authorization" : "Token " + token}}).then(response => {setUserInfo(response.data)});
        const profileId = getUserProfileId();
        axios.get(url2, {
            headers: {
                "Authorization" : "Token " + token}}).then(response => {setProfileInfo(response.data)});
        
        //console.log(userInfo);
    }, [])
    console.log(userInfo);
    console.log(profileInfo);
   
    return (
    <>
        <Followers key={0} placement={"end"} name={"followers"} />
        <Alert variant={"info"} className="d-none d-lg-block"> Personal information</Alert>
        <ListGroup>
            <ListGroup.Item variant="dark">username: {userInfo != null ? userInfo.username: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">email: {userInfo != null ? userInfo.email: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">first name: {userInfo != null ? userInfo.first_name: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">last name: {userInfo != null ? userInfo.last_name: ""}</ListGroup.Item>
        </ListGroup>
        <Alert variant={"info"} className="d-none d-lg-block">Profile information</Alert>
        <text>
            <p>age: {profileInfo != null ? profileInfo.age: ""}</p>
            <p>bio: {profileInfo != null ? profileInfo.bio: ""}</p>
            
        </text>
    </>
    )

}


export default Profile;