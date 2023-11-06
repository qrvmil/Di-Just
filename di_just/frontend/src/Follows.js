import { useState } from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import axios from 'axios';
import {Routes, Route, useNavigate} from 'react-router-dom';
import './styles/buttonStyle.css';

export default function Follows({ name, follows, ...props }) {
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
            <Offcanvas.Title>You follow</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            <ul>{follows.map(person => 
                  <Card.Body>
                    <Card.Title>{person.username}</Card.Title>
                    <button onClick={() => goToProfile(person.id)} className='logout-button'>Go to profile</button>
                  </Card.Body>
                )}
            </ul>
            
            
          </Offcanvas.Body>
        </Offcanvas>
      </>
    );
  }
  