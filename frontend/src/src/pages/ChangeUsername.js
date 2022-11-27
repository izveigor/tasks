import React, { useState, useEffect, useRef} from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL } from '../features/constants';
import checkUsernameExist from '../features/checkUsernameExist';
import { useSelector } from 'react-redux';


export default function ChangeUsername() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isEmailConfirmed = useSelector((state) => state.user.isEmailConfirmed);

    const [successChanged, changeSuccessChanged] = useState(false);
    const [isUsernameExist, changeIsUsernameExist] = useState({});

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

    useEffect(() => {
        if(token == null || !isEmailConfirmed) {
            navigate("/confirm");
        }
    }, []);
    
    return (
        <form onSubmit={changeUsername} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Сменить имя пользователя:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input data-testid="username-input" ref={usernameRef} onChange={async() => changeIsUsernameExist(await checkUsernameExist(usernameRef.current.value))} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Имя пользователя:" required />
            </div>
            <div className="text-center">
                {isUsernameExist.exist && <span data-testid="username-exist" className="h-[20px] py-1 text-center text-sm text-red-500">Такой пользователь уже существует! Доступное имя: "{isUsernameExist.available}".</span>}
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Сменить</button>
            </div>
            <div className="text-center">
                {successChanged && <span data-testid="changed-successfully" className="h-[20px] py-1 text-sm text-green-500">Имя пользователя было успешно изменено!</span>}
            </div>
        </form>
    );
};