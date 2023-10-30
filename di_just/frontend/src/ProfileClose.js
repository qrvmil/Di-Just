import axios from 'axios';
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
function ProfileClose() {

    const uid = window.location.pathname.slice(9);
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        getFollowerInfo(uid).then((res) => {
            setProfile(res);
        })
    }, [])

    console.log(profile);


    

    return (
    <>
        <Alert variant={"info"} className="d-none d-lg-block">Personal information</Alert>
        <ListGroup>
            <ListGroup.Item variant="dark">username: {profile != null ? profile.user.username: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">bio: {profile != null ? profile.bio: ""}</ListGroup.Item>
            <ListGroup.Item variant="dark">age: {profile != null ? profile.age: ""}</ListGroup.Item>
        </ListGroup>
        <Col xs={6} md={4}>
          <Image src={profile != null ? profile.picture: ""} rounded />
        </Col>
    </>
    )

}

export default ProfileClose;