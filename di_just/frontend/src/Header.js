import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { NavLink } from 'react-router-dom'
import { BrowserRouter, Routes, Route, Link, redirect, useNavigate} from 'react-router-dom';
import './styles/buttonStyle.css';
import './Navbar.css'; // Импорт стилей



export default function Header() {
  

    const tokenString = localStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    const token = userToken?.token;
    const navigate = useNavigate();

    const handleLogout = () => {
      navigate(`/login`);
      axios.post('http://127.0.0.1:8000/users/logout/', {headers: {"Authorization": "Token " + token}}).catch((error) => {return});
      localStorage.clear();
      
    }

    return (
    <>
    {!token && 
    <nav className="navbar">
      <div className="navbar__title">Di-Just</div>
      <div className="navbar__links">
        
        <Link to="/login" className='logout-button'>login</Link>
        <Link to="/register" className='logout-button'>register</Link>
        
      </div>
    </nav>
    }
      {token && 
      <nav className="navbar">
      <div className="navbar__title">Di-Just</div>
      <div className="navbar__links">
        <Link to="/home" className='logout-button'>home</Link>
        
        <Link to="/profile" className='logout-button'>profile</Link>
        <button onClick={() => handleLogout()} className='logout-button'>Logout</button>
      </div>
    </nav>}


      

    </>
  );

}