import React, { useState, useEffect, useRef} from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL } from '../features/constants';


export default function ChangeUsername() {
    const token = localStorage.getItem("token");
    const navigate = useNavigate();
    const [successChanged, changeSuccessChanged] = useState(false);
    const [isUsernameExist, changeIsUsernameExist] = useState(false);

    const usernameRef = useRef(null);

    function changeUsername(event) {
        fetch(USERS_URL + "change_username/", {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                username: usernameRef.current.value,
            })
        })
        .then((response) => {
            if(response.ok) {
                changeSuccessChanged(true);
            } else {
                changeSuccessChanged(false);
            }
        })
        event.preventDefault();
    };

    async function checkUsernameExist() {
        await fetch(USERS_URL + "check_username/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: usernameRef.current.value,
            })
        })
        .then((res) => res.json())
        .then((data) => {changeIsUsernameExist({'exist': data.exist, 'available': data.available})})
    };

    useEffect(() => {
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
        <form onSubmit={changeUsername} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Сменить имя пользователя:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input ref={usernameRef} onChange={async() => await checkUsernameExist()} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Имя пользователя:" required />
            </div>
            <div className="text-center">
                {isUsernameExist.exist && <span className="h-[20px] py-1 text-center text-sm text-red-500">Такой пользователь уже существует! Доступное имя: "{isUsernameExist.available}".</span>}
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Сменить</button>
            </div>
            <div className="text-center">
                {successChanged && <span className="h-[20px] py-1 text-sm text-green-500">Имя пользователя было успешно изменено!</span>}
            </div>
        </form>
    );
};