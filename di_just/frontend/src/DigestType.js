import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import {Routes, Route, useNavigate} from 'react-router-dom';


export default function DigestType() {

    const navigate = useNavigate();

    const handleClick1 = () => {
        navigate('/create-img-digest');
    }

    const handleClick2 = () => {
        navigate('/create-link-digest');
    }




    return (
        <>
            <Alert variant={"info"} className="d-none d-lg-block">Please click on the preferable option</Alert>
            <Button variant="outline-info" onClick={handleClick1}>Image digest</Button>
            <Button variant="outline-info" onClick={handleClick2}>Link digest</Button>
        </>
    )
}