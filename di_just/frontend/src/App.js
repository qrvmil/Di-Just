import { useState } from "react";
import Register from "./Register.js";
import Home from "./Home.js";
import Check from "./Check.js";
import Reset from "./Reset.js";
import NewPassword from "./NewPassword";
import Login from "./Login.js";
import Test from "./Test.js";
import Profile from "./Profile.js";
import Header from './Header.js';
import useToken from './useToken';


import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';



function setToken(userToken) {
    localStorage.setItem('token', JSON.stringify(userToken));
}

function getToken() {
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.token
}




function App() {

    const { token, setToken } = useToken();


    if(!token) {
        return <Login setToken={setToken} />
    }

	console.log(getToken());

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
        <Route path="/profile/" element={<Profile />} />
       

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
	  <li>
	  	<Link to="/profile/">Profile</Link>
	  </li>

    </BrowserRouter>
    </>
  );


}

export default App;