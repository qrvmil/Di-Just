import './Card.css';
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
            navigate(`/-digest/${id}/`);
        }
        

    }

    console.log(info);



    return (
    <div className="card">
        <p>{info["name"] !== '' ? info["name"]: 'No name'}  ||  {info["created_timestamp"].slice(0, 10)}</p>
        <div>Introduction: {info["introduction"]}</div>
        <div>Topics: {info["topic"].join(', ')}</div>
        <button onClick={() => handleClick(info["id"])}>dive into digest</button>
    </div>
    )


}