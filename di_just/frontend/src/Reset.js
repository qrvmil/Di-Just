import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useState } from "react";

function Reset() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [emailSent, setEmailSent] = useState(true);

  const onSubmit = (data) => {

    console.log(data)



    axios.put("http://127.0.0.1:8000/users/profile/restore/email/", {
    email: data.email,
     })
      .then(res => {
        console.log(res);
        
      })
    setEmailSent(false);
    console.log(data);
    localStorage.clear();

  };



  return (

    <div>
    {emailSent ? (
    <div style={{maxWidth: '600px', margin: 'auto'}}>
    <h2 style={{color: "white"}}>Восстановление пароля</h2>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label style={{color: "white"}}>Адрес электронной почты</label>
          <input type="email" {...register("email", { required: true })} />
        </div>
        <button type="submit">Восстановить пароль</button>
      </form>
    </div>
    ): (
    <div>
    <p>password-reset link has been sent to your email</p>
    </div>
    )}

  </div>
);
};

export default Reset;