import { useState } from 'react';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';


export default function Followers({ name, followers, ...props }) {
    const [show, setShow] = useState(false);
  
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
  
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
                <li>{<Card body><a href={person.link}>{person.username}</a></Card>}</li>
                )}
            </ul>
            
            
          </Offcanvas.Body>
        </Offcanvas>
      </>
    );
  }
  