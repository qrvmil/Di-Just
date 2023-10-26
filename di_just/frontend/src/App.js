import { useState } from "react";
import Register from "./Register.js";
import Home from "./Home.js";
import Check from "./Check.js";
import Reset from "./Reset.js";
import NewPassword from "./NewPassword";
import Login from "./Login.js";
import Test from "./Test.js";
import useToken from './useToken';
import Header from './Header.js';

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';



function setToken(userToken) {
    sessionStorage.setItem('token', JSON.stringify(userToken));
}

function getToken() {
    const tokenString = sessionStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.token
}


function App() {

    const { token, setToken } = useToken();


    if(!token) {
        return <Login setToken={setToken} />
    }

    return (
    <>

    <Header/>

    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/activate/:uid/:token" element={<Check />} />
        <Route path="/reset" element={<Reset />} />
        <Route path="/login" element={<Login />} />
        <Route path="/restore/:uid/:token" element={<NewPassword />} />
        <Route path="/test" element={<Test />} />

      </Routes>

      <li>
        <Link to="/register">Register</Link>
      </li>
      <li>
        <Link to="/home">Home</Link>
      </li>
      <li>
        <Link to="/reset">Reset password</Link>
      </li>
      <li>
        <Link to="/login">Login</Link>
      </li>

    </BrowserRouter>
    </>
  );


}

export default App;