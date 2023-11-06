import Register from "./Register.js";
import { useForm } from 'react-hook-form';
import { useEffect, useState } from "react";
import axios from 'axios';


function NewPassword() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [formSubmitted, setFormSubmitted] = useState(false);

    const onSubmit = (data) => {
        const pathname = window.location.pathname;
        axios.put("http://127.0.0.1:8000" + pathname, {password: data.password})
          .then(res => {
            console.log(res);
          }).then(res => {
      })
       
        setFormSubmitted(true);

  };

    return (
    <>
        {formSubmitted ? (
        <div>
            <p>Your password is successfully changed. Now you can login your account</p>
        </div>
        ) : (
        <div>
        <h2>Придумайте новый пароль</h2>
          <form onSubmit={handleSubmit(onSubmit)}>
            <div>
              <label>Новый пароль</label>
              <input type="password" {...register("password", { required: true })} />
            </div>
            <div>
              <label>Повторите пароль</label>
              <input type="password" {...register("password2", { required: true })} />
            </div>
            <button type="submit">Восстановить пароль</button>
          </form>
        </div>
        )}
    </>
    )

}

export default NewPassword;