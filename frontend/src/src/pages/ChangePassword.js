import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL } from '../features/constants';


export default function ChangePassword() {
    const token = localStorage.getItem("token");
    const navigate = useNavigate();
    const passwordRef = useRef(null);
    const repeatedPasswordRef = useRef(null);

    const [successChanged, changeSuccessChanged] = useState(false);
    const [passwordState, changePasswordState] = useState(false);
    const [repeatedPasswordState, changeRepeatedPasswordState] = useState(false);

    const numberRegex = new RegExp("[0-9]");
    const lowerRegex = new RegExp("[a-z]");
    const upperRegex = new RegExp("[A-Z]");

    function changePassword(event) {
        if (!passwordState && !repeatedPasswordState) {
            fetch(USERS_URL + "change_password/", {
                method: "PUT",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Token " + token,
                },
                body: JSON.stringify({
                    "password": passwordRef.current.value,
                    "repeated_password": repeatedPasswordRef.current.value,
                })
            }).then((response) => {
                if(response.ok) {
                    changeSuccessChanged(true);
                }
            })
            event.preventDefault();
        }
    }

    const checkPassword = async() => {
        let password = passwordRef.current.value;
        let isUpper = false,
            isLower = false,
            isDigit = false;

        if(password.length < 10) {
            changePasswordState(true);
            return 
        }

        for(let i = 0; i < password.length; i ++) {
            if(password[i].match(numberRegex) !== null) {
                isDigit = true;
                continue;
            }

            if(password[i].match(lowerRegex) !== null) {
                isUpper = true;
                continue;
            }

            if(password[i].match(upperRegex) !== null) {
                isLower = true;
                continue;
            }
        }

        if(isUpper && isLower && isDigit) {
            changePasswordState(false);
        } else {
            changePasswordState(true);
        }
        return 
    };

    const checkRepeatedPassword = async() => {
        if (passwordRef.current.value == repeatedPasswordRef.current.value) {
            changeRepeatedPasswordState(false);
        } else {
            changeRepeatedPasswordState(true);
        }
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
        <form onSubmit={changePassword} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Сменить пароль:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input ref={passwordRef} onChange={async() => await checkPassword()} type="password" className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Пароль:" required />
                <input ref={repeatedPasswordRef} onChange={async() => await checkRepeatedPassword()} type="password" className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Повторить пароль:" required />
                {passwordState && <span className="h-[50px] py-1 text-center text-sm text-red-500">Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!</span>}
                {repeatedPasswordState && <span className="h-[50px] py-1 text-center text-sm text-red-500">Пароли не совпадают!</span>}
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Сменить</button>
            </div>
            {successChanged && <span className="h-[20px] py-1 text-sm text-green-500">Пароль был успешно изменен!</span>}
        </form>
    );
};