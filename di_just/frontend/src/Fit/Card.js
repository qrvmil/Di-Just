import './Card.css';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';

export default function Card ({ digestType, info }) {

    const navigate = useNavigate();


    const handleClick = (id) => {
        if (digestType == "img") {
            console.log('clicked');
            navigate(`/img-digest/${id}/`);
        }
        else {
            console.log('clicked');
            navigate(`/link-digest/${id}/`);
        }
        

    }

    console.log(info);



    return (
    <div className="card">
        <h5>{info["name"] !== '' ? info["name"]: 'No name'}</h5>
        <p>{info["created_timestamp"].slice(0, 10)}</p>
        <div>Introduction: {info["introduction"]}</div>
        <div>Topics: {info["topic"].join(', ')}</div>
        <Button variant="outline-info" onClick={() => handleClick(info["id"])}>dive into digest</Button>
    </div>
    )


}