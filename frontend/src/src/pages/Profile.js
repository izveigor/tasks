import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';


export default function Profile() {
    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    const [userData, changeUserData] = useState({}); 
    const [isLoaded, changeIsLoaded] = useState(false);

    async function getProfile() {
        await fetch(USERS_URL + "settings/", {
            method: "GET",
            headers: {
                'Content-Type': "application/json",
                'Authorization': "Token " + token,
            },
        }).then((response) => response.json())
        .then((data) => {
            changeUserData(data);
            changeIsLoaded(true);
        })
    }

    useEffect(() => {
        getProfile();
        if(token == null) {
            navigate("confirm");
        }
        fetch(USERS_URL + "authorization_with_email/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.status === 403) {
                navigate("confirm");
            }
        })
        .catch((error) => navigate("/confirm"))
    }, []);

    return (
        <div className="bg-white rounded-md py-2 px-2">
            {isLoaded && (<div>
                <h1 className="text-xl text-center">{userData.user.first_name + " " + userData.user.last_name} <span className="text-gray-600">({userData.user.username})</span></h1>
                <div className="grid grid-cols-4 mt-2">
                    <div className="border-2 w-40 h-40 rounded-sm px-1 py-1 border-gray-400">
                        <img className="w-[100%] h-[100%]" src={USERS_URL_WITHOUT_SLASH + userData.image} />
                    </div>
                    <div className="w-70 col-span-3 border-2 border-gray-400 rounded-sm py-2 px-4">
                        <p><b>Должность:</b> {userData.job_title}</p>
                        <p><b>Описание:</b> {userData.description}</p>
                    </div>
                </div>
            </div>)}
        </div>
    );
};