import axios from 'axios';
import { Button } from 'bootstrap';
import { useEffect, useState } from 'react';
import { ListGroup } from 'react-bootstrap';
import Alert from 'react-bootstrap/Alert';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
const API_URL = 'http://localhost:8000';



function getFollowerInfo(fid) {
    const url = `http://127.0.0.1:8000/users/profile-info/${fid}/`;
    
    const data = axios.get(url).then(response => {return response.data});
    console.log(data);
    return data;
    
}

function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}

function ProfileClose() {

    const uid = window.location.pathname.slice(9);
    const [profile, setProfile] = useState(null);
    const user = getUserId();
    const [userInfo, setUserInfo] = useState(null);
    const [isFollower, setIsFollower] = useState(true);

    useEffect(() => {
        getFollowerInfo(uid).then((res) => {
            setProfile(res);
        })
        getFollowerInfo(user).then((res) => {
            setUserInfo(res)
        })
    }, [])

   
    useEffect(() => {

        const following = userInfo !== null ? userInfo.follows: [];
        console.log(following);
        console.log(userInfo);
        const profile_user_id = profile !== null ? profile.user.id: 0;
        console.log(profile_user_id);
    
        if ((following !== []) & (profile_user_id in following)) {
            setIsFollower(false);
    }

    },)

    

    const followUser = (id) => {
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
        
        axios.put(`http://127.0.0.1:8000/users/follow/${id}/`, {}, {
            headers: {
            "Authorization" : "Token " + token}}).then(res => console.log(res));

        setIsFollower(!isFollower);

    }

    const unfollowUser = (id) => {
        const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;
       
        axios.put(`http://127.0.0.1:8000/users/unfollow/${id}/`, {}, {
            headers: {
            "Authorization" : "Token " + token}}).then(res => console.log(res));
        setIsFollower(!isFollower);
    }



    

    return (
    <>
        <Alert variant={"info"} className="d-none d-lg-block">Profile information</Alert>
        <ListGroup>
            
            <ListGroup.Item variant="dark">username: {profile != null ? profile.user.username: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">bio: {profile != null ? profile.bio: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">age: {profile != null ? profile.age: ""}</ListGroup.Item>
        </ListGroup>
        <Col xs={6} md={4}>
          <Image src={profile != null ? profile.picture: ""} rounded />
          
        </Col>
        {console.log(isFollower)}
        {!isFollower ? <button onClick={() => followUser(profile.id)}>Follow user</button>: <button onClick={() => unfollowUser(profile.id)}>Unfollow user</button>}
    </>
    )

}

export default ProfileClose;