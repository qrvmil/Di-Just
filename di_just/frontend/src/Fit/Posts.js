import axios from 'axios';
import { useState, useEffect } from 'react';
import Card from './Card';
import './Posts.css';
const API_URL = 'http://localhost:8000';






function listOfLinkDigests (info) {
    return axios.get(`${API_URL}/link-all/`, {params: info}).then(res => res.data)

}




export default function Posts({ digestType, type, content}) {

    const [fit, setFit] = useState(null);
    const [previous, setPrevious] = useState();
    const [next, setNext] = useState();
    const [error, setError] = useState(false);

    function listOfDigests (info) {
        if (digestType == "img") {
            return axios.get(`${API_URL}/img-all/`, {params: info}).then(res => {
                setError(false);
                if (res.data == "failed") {
                    setError(true);
                }
                setNext(res.headers["next"]);
                setPrevious(res.headers["previous"]);
                return res.data
            })
        }
        return axios.get(`${API_URL}/link-all/`, {params: info}).then(res => {
            setError(false);
            if (res.data == "failed") {
                setError(true);
            }
            setNext(res.headers["next"]);
            setPrevious(res.headers["previous"]);
            return res.data
        })
        
        
    }

    function listOfDigestsPag (link) {
        return axios.get(link).then(res => {
            setNext(res.headers["next"]);
            setPrevious(res.headers["previous"]);
            return res.data;
        })
        
    }

    const handlePreviousPage = () => {
        listOfDigestsPag(previous).then(resp => {
            setFit(resp);
        });

        
    }

    const handleNextPage = () => {
        listOfDigestsPag(next).then(resp => {
            setFit(resp);
        });
    }
    
    
    useEffect (() => {

        // console.log(key);
        let params;
        if (type === "topics") {
            params = { topics: content }
        }
        else if (type === "owner") {
            params = { owner: content }
        }
        else {
            params = { time: content }
        }
        console.log(1);

        listOfDigests(params)
          .then(items => {
                if (items === "failed") {return}
                setFit(items);
                // setNext(items.headers["next"]);
                // setPrevious(items.headers["previous"])
                console.log(items);
          })
    }, [type, content, digestType])


    

    return (
    <>
    {(!error) && <>
    <div className="wrapper">
    {(fit != null) && fit.map(digest => <Card digestType={digestType} info={digest} />)}
    </div>
    {(previous != "None") &&  <button onClick={handlePreviousPage}>Previos</button>} {(next != "None") && <button onClick={handleNextPage}>Next</button>}
    </>}
    
    </>
    )

}