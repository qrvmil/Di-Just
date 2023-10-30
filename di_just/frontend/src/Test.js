import React, { useState } from 'react';
import { Container, Button } from 'react-bootstrap';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

const MyForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    firstName: '',
    lastName: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Отправка POST-запроса на сервер с данными из формы
    fetch('ссылка_на_сервер', {
      method: 'POST',
      body: JSON.stringify(formData)
    })
      .then((response) => response.json())
      .then((data) => {
        // Обработка ответа от сервера
        console.log(data);
      })
      .catch((error) => {
        // Обработка ошибок
        console.error(error);
      });
  };

  return (
    <Container>
      <Form onSubmit={handleSubmit} className="my-form">
        <Form.Group controlId="formUsername" className="form-group">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group controlId="formEmail" className="form-group">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group controlId="formPassword" className="form-group">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group controlId="formFirstName" className="form-group">
          <Form.Label>First Name</Form.Label>
          <Form.Control
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group controlId="formLastName" className="form-group">
          <Form.Label>Last Name</Form.Label>
          <Form.Control
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
          />
        </Form.Group>

        <Button variant="primary" type="submit" className="submit-button">
          Submit
        </Button>
      </Form>

      <div style={{ display: 'block',
                  width: 900,
                  padding: 50}} >

      <Form className='container mt-3 mb-3 m-auto'>
        <Row className="mb-3">
          <Form.Group as={Col} controlId="formGridEmail">
            <Form.Control type="username" placeholder="Username" />
          </Form.Group>

          <Form.Group as={Col} controlId="formGridPassword">
            <Form.Control type="password" placeholder="Password" />
          </Form.Group>
        </Row>

        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
          <Form.Control type="email" placeholder="name@example.com" />
        </Form.Group>

        <Row>
          <Col>
            <Form.Control placeholder="First name" />
          </Col>
          <Col>
            <Form.Control placeholder="Last name" />
          </Col>
        </Row>
      </Form>
      </div>
    </Container>
  );
};

export default MyForm;
