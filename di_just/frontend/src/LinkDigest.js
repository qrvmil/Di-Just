import { useParams } from 'react-router-dom';
import { useState } from 'react';


export default function LinkDigest() {

    const [digest, setDigest] = useState();
    const params = useParams();
    const digestId = params.id;

    return(
    <>
        <p>Link digest {digestId}</p>


    </>)

}