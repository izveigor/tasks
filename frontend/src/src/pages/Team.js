import React, { useEffect, useState } from 'react';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';
import { useNavigate } from 'react-router-dom';


export default function Team() {
    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    const [myTeamData, changeMyTeamData] = useState({});
    const [isLoaded, changeIsLoaded] = useState(false);

    async function getTeam() {
        await fetch(USERS_URL + "team/", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
        })
        .then((response) => response.json())
        .then((data) => {
            changeIsLoaded(true);
            changeMyTeamData(data);
        })
    }

    useEffect(() => {
        getTeam()
        if(token == null) {
            navigate("/confirm");
        }
        fetch(USERS_URL + "authorization_with_email/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.status === 403) {
                navigate("/confirm");
            }
        })
        .catch((error) => navigate("/confirm"))
    }, []);

    return (
        <div className="bg-white rounded-md inline py-2 px-2 grid">
            {isLoaded && (<div>
            <div className="text-center my-2">
                <h1 className="text-2xl">Моя команда:</h1>
            </div>
            <div className="text-center my-2">
                <h1 className="text-xl">{myTeamData.name}</h1>
            </div>
            <div className="grid grid-cols-4">
                <div className="border-2 w-40 h-40 rounded-sm px-1 py-1 border-gray-400">
                    <img className="w-[100%] h-[100%]" src={USERS_URL_WITHOUT_SLASH + myTeamData.image} />
                </div>
                <div className="w-70 col-span-3 border-2 border-gray-400 rounded-sm py-2 px-4">
                    <p><b>Описание:</b> {myTeamData.description}</p>
                </div>
            </div></div>)}
        </div>
    );
};