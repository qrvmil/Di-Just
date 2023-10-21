import { useState } from "react";
import Register from "./Register.js";
import Home from "./Home.js"
import Check from "./Check.js"
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {

    const ui = /(?P<uidb64>[0-9A-Za-z_\-]+)/;
    const tok = /(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/;

    return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/activate/{ui}/{tok}" element={<Check />} />
      </Routes>
    </BrowserRouter>
  );


}

export default App;