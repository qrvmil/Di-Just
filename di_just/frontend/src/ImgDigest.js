import { useParams } from 'react-router-dom';
import { useState } from 'react';


export default function ImgDigest() {

    const [digest, setDigest] = useState();
    const params = useParams();
    const digestId = params.id;

    return(
    <>
        <p>Image digest {digestId}</p>


    </>)

}