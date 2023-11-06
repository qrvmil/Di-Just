import { useState } from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import {Routes, Route, useNavigate} from 'react-router-dom';


export default function Followers({ name, followers, ...props }) {
    const [show, setShow] = useState(false);
  
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();
    const goToProfile = (id) => {
      navigate(`/profile/${id}`)
  }
  
    return (
      <>
        <Button variant="primary" onClick={handleShow} className="me-2">
          {name}
        </Button>
        <Offcanvas show={show} onHide={handleClose} {...props}>
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>Followers</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            <ul>{followers.map(person => 
                <li>
                  <Card.Body>
                    <Card.Title>{person.username}</Card.Title>
                    <button onClick={() => goToProfile(person.id)}>Go to profile</button>
                  </Card.Body>
                </li>
                
                )}
            </ul>
            
            
          </Offcanvas.Body>
        </Offcanvas>
      </>
    );
  }
  