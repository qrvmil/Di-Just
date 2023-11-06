import { useEffect, useState } from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8000';
function getUserId() {
	const userStringId = localStorage.getItem('token')
	const userId = JSON.parse(userStringId);
	return userId.user;
}


export default function Comments({ name, comments, type, digest, ...props }) {
    const [show, setShow] = useState(false);
    const [users, setUsers] = useState([]);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [add, setAdd] = useState(false);
    const [comment, setComment] = useState('');
    const [newComments, setNewComment] = useState([]);
    
    
    
    const navigate = useNavigate();
    const goToProfile = (id) => {
        navigate(`/profile/${id}`)
    }
    const tokenString = localStorage.getItem('token');
        const userToken = JSON.parse(tokenString);
        const token = userToken?.token;

    function getUserProfileId(id) {
       
        const url1 = `${API_URL}/users/user/${id}/`;
        
        return axios.get(url1, {
            headers: {
            "Authorization" : "Token " + token}}).then(response => {return response.data});
    }

    useEffect(() => {
      console.log(comments);
      setNewComment(comments.slice());
    }, [comments]);


    useEffect (() => {
        comments.map(elem => {
            getUserProfileId(elem.user).then(val => {
                setUsers([...users, val])
            })
          
        })
    }, [])
    //console.log(users);

    function addComment() {
      if (type == "image") {
        axios.post("http://127.0.0.1:8000/digest/comment/create/", {
          user: getUserId(),
          text: comment,
          img_digest: digest
          }, {
          headers: {
          "Authorization" : "Token " + token}}).then(response => {return response.data});

      setAdd(false);
      setNewComment([{user: getUserId(), text: comment, img_digest: digest}, ...newComments])
      setComment("");
      }
      else {
        axios.post("http://127.0.0.1:8000/digest/comment/create/", {
            user: getUserId(),
            text: comment,
            link_digest: digest
        }, {
            headers: {
            "Authorization" : "Token " + token}}).then(response => {return response.data});

        setAdd(false);
        setNewComment([{user: getUserId(), text: comment, img_digest: digest}, ...newComments])
        setComment("");
      }
    }

    

    
  
    return (
      <>
        <Button variant="primary" onClick={handleShow} className="me-2">
          {name}
        </Button>
        <Offcanvas show={show} onHide={handleClose} {...props}>
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>Comments</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            <ul>{ newComments !== null ? newComments.map((comment, ind) => 
                <li>
                  <Card.Body>
                    <Card.Title>{comment.text}</Card.Title>
                    <button onClick={() => goToProfile(comment.user)}>Go to profile</button>
                  </Card.Body>
                </li>
                ): ''}
            </ul>

            <button onClick={() => {setAdd(true)}}>add comment</button>
            {add && 
            <>
            <form onSubmit={addComment}>
                <textarea
                value={comment}
                onChange={e => setComment(e.target.value)}
                />
            <button type="submit">submit</button>
            </form>
            
            </>
            }
            
            
          </Offcanvas.Body>
        </Offcanvas>
      </>
    );
  }
  