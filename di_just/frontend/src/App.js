import { useState } from "react";
import Cookies from 'js-cookie';
import Register from "./Register.js";
import Home from "./Home.js";
import Check from "./Check.js";
import Reset from "./Reset.js";
import NewPassword from "./NewPassword";
import Login from "./Login.js";
import Fit from "./Fit/Fit.js";
import Profile from "./Profile.js";
import Header from './Header.js';
import useToken from './useToken';
import ProfileClose from './ProfileClose.js';
import ProfileEdit from "./ProfileEdit.js";
import DigestType from './DigestType.js';
import CreateImageDigest from "./CreateImageDigest.js";
import CreateLinkDigest from "./CreateLinkDigest.js";
import CreatedDigests from "./CreatedDigests.js";
import SavedDigests from "./SavedDigests.js";
import ImgDigest from "./ImgDigest.js";
import LinkDigest from "./LinkDigest.js";
import EditImgDigest from "./EditImgDigest.js";
import EditLinkDigest from "./EditLinkDigest.js";
import Start from './Start.js';
import Tastemaker from "./Tastemaker.js"




import { BrowserRouter, Routes, Route, Link, Router } from 'react-router-dom';



function setToken(userToken) {
    localStorage.setItem('token', JSON.stringify(userToken));
    Cookies.set('test', 'hello&mi')
    Cookies.set('token', JSON.stringify(userToken));
    const test = Cookies.get("token");
    console.log('-------')
    console.log(test);
}

function getToken() {
    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.token;
}




function App() {

    const { token, setToken } = useToken();
    
  


    // if(!token) {
    //     return <Login setToken={setToken} />
    // }

	console.log(getToken());

    return (
    <div>

    

    <BrowserRouter>
    <Header/>
      <Routes>
        <Route path="/" element={<Start />}/>
        <Route path="/register" element={<Register />} />
        <Route path="/test" element={<Home />} />
        <Route path="/activate/:uid/:token" element={<Check />} />
        <Route path="/reset" element={<Reset />} />
        <Route path="/login" element={<Login setToken={setToken}/>} />
        <Route path="/restore/:uid/:token" element={<NewPassword />} />
        <Route path="/home" element={<Fit />} />
        <Route path="/profile/" element={<Profile />} />
        <Route path="/profile-edit/" element={<ProfileEdit />} />
        <Route path="/profile/:uid" element={<ProfileClose />} />
        <Route path="/type" element={<DigestType />} />
        <Route path="/create-img-digest" element={<CreateImageDigest/>}/>
        <Route path="/create-link-digest" element={<CreateLinkDigest/>}/>
        <Route path="/created-digests" element={<CreatedDigests/>} />
        <Route path="/saved-digests" element={<SavedDigests/>}/>
        <Route path="/img-digest/:id/" element={<ImgDigest/>} />
        <Route path="/link-digest/:id/" element={<LinkDigest/>} />
        <Route path="/img-edit/:id" element={<EditImgDigest/>}/>
        <Route path="/link-edit/:id" element={<EditLinkDigest/>}/>
        <Route path="/test2/" element={<Tastemaker/>}/>
       

      </Routes>


    </BrowserRouter>

    
    </div>
  );


}

export default App;