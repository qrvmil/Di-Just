import React from 'react';
import './Login.css';
import PropTypes from 'prop-types';
import axios from 'axios';
import { useState } from "react";


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

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password
    });
    setToken(token);
    console.log(token)
  }


  return(
    <div className="login-wrapper">
      <h1>LogIn</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)}/>
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  )
}


Login.propTypes = {
  setToken: PropTypes.func.isRequired
}