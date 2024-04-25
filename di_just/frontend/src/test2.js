import { useForm } from 'react-hook-form';
import axios from 'axios';
import Form from 'react-bootstrap/Form';


function Test2() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
    axios.post("http://127.0.0.1:8000/register/", {
    username: data.username,
    email: data.email,
    password: data.password,
    first_name: data.first_name,
    last_name: data.last_name
     })
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
    console.log(data);

  };




  return (
    <Form>
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>Username</label>
      <input type="username" {...register("username", { required: true })} />
      {errors.username && <p>Username is required</p>}

      <label>First name</label>
      <input type="first_name" {...register("first_name", { required: true })} />
      {errors.username && <p>Username is required</p>}

      <label>Last name</label>
      <input type="last_name" {...register("last_name", { required: true })} />
      {errors.username && <p>Username is required</p>}

      <div class="row mb-3">
      <label for="inputEmail3" class="col-sm-2 col-form-label">Email</label>
      <div class="col-sm-10">
        <input type="email" {...register("email", { required: true, pattern: /^\S+@\S+$/i })} class="form-control" id="inputEmail3"/>
      </div>
      {errors.email && <p>Email is required and must be valid</p>}
      </div>

      <label>Password</label>
      <input type="password" {...register("password", { required: true })} />
      {errors.password && <p>Password is required</p>}

      <button type="submit">Submit</button>
    </form>
    </Form>
  );
}

export default Test2;