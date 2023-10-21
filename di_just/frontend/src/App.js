import { useState } from "react";
import Register from "./Register.js";
import Home from "./Home.js"
import Check from "./Check.js"
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {



    return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/activate/:uid/:token" element={<Check />} />
      </Routes>
    </BrowserRouter>
  );


}

export default App;