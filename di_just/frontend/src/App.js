import { useState } from "react";
import Register from "./Register.js";
import Home from "./Home.js";
import Check from "./Check.js";
import Reset from "./Reset.js";
import NewPassword from "./NewPassword";
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {




    return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/activate/:uid/:token" element={<Check />} />
        <Route path="/reset" element={<Reset />} />
        <Route path="/login" element={<Register />} />
        <Route path="/restore/:uid/:token" element={<NewPassword />} />

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