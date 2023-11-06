import Register from "./Register.js";
import { useEffect } from "react";
import axios from 'axios';


function Check() {

    useEffect (() => {
        const pathname = window.location.pathname;
        axios.put("http://127.0.0.1:8000" + pathname)
          .then(res => {
            console.log(res);
            console.log(res.data);
          })
    })

    return (
    <>
        <p style={{color: "white"}}>Email is verified!</p>
    </>
    )

}

export default Check;