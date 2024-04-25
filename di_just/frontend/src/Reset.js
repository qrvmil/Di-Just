import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useState } from "react";
import './styles/Reset.css';
import './styles/buttonStyle.css';

function Reset() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [emailSent, setEmailSent] = useState(true);
  const [error, setError] = useState(false);

  const onSubmit = (data) => {

    console.log(data)



    axios.put("http://127.0.0.1:8000/users/profile/restore/email/", {
    email: data.email,
     })
      .then(res => {
        console.log(res);
        
      }).catch(function (error) {
        alert("No user with such email");
        setError(true);
      })
    setEmailSent(false);
    console.log(data);
    localStorage.clear();

  };



  return (

    <div class='reset-page'>
    {emailSent ? (
   
    
      <form onSubmit={handleSubmit(onSubmit)} className='login-form'>
      <h2 className="reset-title">Reset your password</h2>
        <div>
          <label style={{color: "white"}}>Email address:</label>
          <input type="email" {...register("email", { required: true })} />
        </div>
        <button type="submit">Восстановить пароль</button>
      </form>
    
    ): ( error === false? 
    (<div>
    <p style={{color: "white"}}>password-reset link has been sent to your email</p>
    </div>) : <h5 style={{color: "white"}}>Sorry, we can't send email to you. Try again and make sure email is correct.</h5>
    )}

  </div>
);
};

export default Reset;