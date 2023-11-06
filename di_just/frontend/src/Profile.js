import axios from 'axios';
import getToken from './App';
import { useState } from "react";
import { useEffect } from 'react';
import Alert from 'react-bootstrap/Alert';
import { ListGroup } from 'react-bootstrap';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import {Routes, Route, useNavigate} from 'react-router-dom';
import Followers from './Followers.js';
import Follows from './Follows.js';
import './styles/UserProfile.css';



const API_URL = 'http://localhost:8000';


// TODO: follows lists + unfollow button;

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

function getFollowerInfo(fid) {
    const url = `http://127.0.0.1:8000/users/profile-info/${fid}/`;
    
    const data = axios.get(url).then(response => {return response.data});
    console.log(data);
    return data;
    
}




function Profile() {

    const [userInfo, setUserInfo] = useState(null);
    const [userId, setUserId] = useState(null);
    const [profileInfo, setProfileInfo] = useState(null);
    const [followers, setFollowers] = useState([]);
    const [follows, setFollows] = useState([]);
    const [flag, setFlag] = useState(false);
    const navigate = useNavigate();

    const editProfile = () => {
        // 👇️ navigate to /profile-edit
        navigate('/profile-edit');
    };

    const handleClick1 = () => {
        // navigate to /created-digests
        navigate('/created-digests')
    }

    const handleClick2 = () => {
        // navigate to /saved-digests
        navigate('/saved-digests')

    }

   

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

    useEffect(() => {
        if (profileInfo === null || flag) {
            return;
        }
        setFlag(true);
        console.log(2);
        console.log(profileInfo);


        const followersID = profileInfo.followed_by;
        const followsID = profileInfo.follows;

        followsID.map(function(fid) {
            let follow = {};
            follow["id"] = fid;
            follow["link"] = `http://localhost:3000/profile/${fid}`;
            getFollowerInfo(fid).then((res) => {
                follow["picture"] = res.picture;
                follow["username"] = res.user.username;
            });
            
            // follower["picture"] = followerInfo.picture;
            // follower["username"] = followerInfo.user.username;
            setFollows((prevFollowers) => [
                ...prevFollowers,
                follow,
            ]);
            
        })

        followersID.map(function(fid) {
            let follower = {};
            follower["id"] = fid;
            follower["link"] = `http://localhost:3000/profile/${fid}`;
            getFollowerInfo(fid).then((res) => {
                follower["picture"] = res.picture;
                follower["username"] = res.user.username;
            });
            
            // follower["picture"] = followerInfo.picture;
            // follower["username"] = followerInfo.user.username;
            setFollowers((prevFollowers) => [
                ...prevFollowers,
                follower,
            ]);
            
        })

    }, [profileInfo])
    
    
    console.log(followers);
    console.log(profileInfo);
    
   
    return (
    
    <div className="profile-page">

    <div className="user-profile">
      <h2>Personal information</h2>
      <div className="user-details">
        <p><strong>username:</strong> {userInfo != null ? userInfo.username: ""}</p>
        <p><strong>first name:</strong> {userInfo != null ? userInfo.first_name: ""}</p>
        <p><strong>last name:</strong> {userInfo != null ? userInfo.last_name: ""} </p>
        <p><strong>email:</strong> {userInfo != null ? userInfo.email: ""}</p>
      </div>
      <h2>Profile information</h2>
      <div className="user-details">
        <p><strong>age:</strong> {profileInfo != null ? profileInfo.age: ""}</p>
        <p><strong>bio:</strong> {profileInfo != null ? profileInfo.bio: ""}</p>
      </div>
      <div className="user-photo">
        <img src={profileInfo != null ? profileInfo.picture: ""} alt="user image" />
      </div>
      <p><Followers placement={"end"} name={"followers"} followers={followers}/> <Follows placement={"end"} name={"follows"} follows={follows}/></p>
      <Button variant="info" onClick={editProfile}>Edit profile</Button>
      
    </div>
        
    <Button variant="outline-info" onClick={handleClick1} className='user-profile'>Created digests</Button>
      <Button variant="outline-info" onClick={handleClick2} className='user-profile'>Saved digests</Button>
        


    
    </div>
    
    )

}


export default Profile;