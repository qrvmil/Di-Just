import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { useState } from "react";
import { useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// TODO: add profile edit
// TODO: add Image (picture) edit;
// TODO: email verification if changed;
// TODO: validate edited data;



function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}



const ProfileEdit = ({ props }) => {

    const [userInfo, setUserInfo] = useState(null);
    const [profileInfo, setProfileInfo] = useState(null);
    const [flag, setFlag] = useState(false);


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
        axios.get(url2, {
            headers: {
                "Authorization" : "Token " + token}}).then(response => {setProfileInfo(response.data)});
        console.log(1);
        //console.log(userInfo);
    }, [])

    //console.log(profileInfo);
    





    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const username = (formData.get('username') != '' ? formData.get('username') :userInfo.username);
        const email = (formData.get('email') != '' ? formData.get('email') :userInfo.email);
        const lastName = (formData.get('lastName') != '' ? formData.get('lastName') :userInfo.last_name);
        const firstName = (formData.get('firstName') != '' ? formData.get('firstName') :userInfo.first_name);
        // Делаем что-то с данными формы, например, отправляем на сервер


        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
        axios.put(`http://127.0.0.1:8000/users/update/${getUserId()}/`, {
            username: username,
            email: email,
            first_name: firstName,
            last_name: lastName
            }, {headers: {"Authorization" : "Token " + token}})
            .then(res => {
                console.log(res);
                console.log(res.data);})


        console.log('done');
        
    };

    return (
        <Form onSubmit={handleSubmit}>
        <Form.Group controlId="username">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" name="username" placeholder={userInfo ? userInfo.username: ""}/>
        </Form.Group>

        <Form.Group controlId="email">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" name="email" placeholder={userInfo ? userInfo.email: ""} />
        </Form.Group>

        <Form.Group controlId="firstName">
            <Form.Label>First Name</Form.Label>
            <Form.Control type="text" name="firstName" placeholder={userInfo ? userInfo.first_name: ""} />
        </Form.Group>

        <Form.Group controlId="lastName">
            <Form.Label>Last Name</Form.Label>
            <Form.Control type="text" name="lastName" placeholder={userInfo ? userInfo.last_name: ""} />
        </Form.Group>

        

        <Button variant="primary" type="submit">
            Submit
        </Button>
        </Form>
    );
};

export default ProfileEdit;
