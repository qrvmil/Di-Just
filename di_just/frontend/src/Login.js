import React from 'react';

import PropTypes from 'prop-types';
import axios from 'axios';
import Header from './Header.js';
import { useState } from "react";
import Register from './Register';
import { Routes, Route, useNavigate } from 'react-router-dom';

import './styles/LoginPage.css';
import './styles/buttonStyle.css';


async function loginUser(data) {

  


    return axios.post("http://127.0.0.1:8000/users/login/", {
    username: data.username,
    password: data.password,
     })
      .then(res => res.data)
}


export default function Login({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const navigate = useNavigate();




  
  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password
    });
    setToken(token);
    console.log(token);
    navigate('/home');
  }

  const handlePassword = () => {
    navigate('/reset')
  }



  return(
    <>
    <div className='login-page'>
      
      <form onSubmit={handleSubmit} className='login-form'>
      <h2 className="login-title">Login</h2>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)} />
        </label>
        <div>
          <button type="submit" >Submit</button>
        </div>
      </form>
    </div>

    <button onClick={() => handlePassword()} className=''>Forgot password</button>
  
    </>
  )
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
}