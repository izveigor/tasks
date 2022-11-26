import React from 'react';
import { useState, useRef } from "react";
import { USERS_URL } from '../../features/constants';
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux';
import { userUpdated } from '../../features/userSlice';


export default function RegisterForm() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [usernameData, changeUsernameData] = useState({});
    const [isEmailExist, changeEmailExist] = useState(false);
    const [passwordState, changePasswordState] = useState(false);

    let submitState = false

    const firstNameRef = useRef(null);
    const lastNameRef = useRef(null);
    const usernameRef = useRef(null);
    const emailRef = useRef(null);
    const passwordRef = useRef(null);

    const numberRegex = new RegExp("[0-9]");
    const lowerRegex = new RegExp("[a-z]");
    const upperRegex = new RegExp("[A-Z]");

    async function checkUsernameExist() {
        if(usernameRef.current.value == "") {
            return () => changeUsernameData({'exist': false, 'available': null});
        }

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
        .then((data) => {changeUsernameData({'exist': data.exist, 'available': data.available})})
    };

    async function checkEmailExist() {
        if(emailRef.current.value == "") {
            return () => changeEmailExist(false);
        }

        await fetch(USERS_URL + "check_email/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: emailRef.current.value,
            })
        })
        .then((res) => res.json())
        .then((data) => changeEmailExist(data.exist))
    };

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
    
    function isSubmitted() {
        if(
            firstNameRef.current.value != "" &&
            lastNameRef.current.value != "" &&
            !usernameData.exist && !isEmailExist
            && !passwordState
        ) submitState = true;
        else submitState = false;
    };
    
    function register(event) {
        isSubmitted();
        if(submitState) {
            fetch(USERS_URL + "register/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: firstNameRef.current.value,
                    last_name: lastNameRef.current.value,
                    username: usernameRef.current.value,
                    email: emailRef.current.value,
                    password: passwordRef.current.value,
                })
            })
            .then((res) => res.json())
            .then((res) => {
                dispatch(userUpdated({"token": res.token}));
                navigate('/confirm');
            })
        };
        event.preventDefault();
    };

    return (
        <form onSubmit={register}>
            <div className="grid grid-cols-2">
                <input id="first_name" data-testid="first-name-input" ref={firstNameRef} type="text" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 outline-1 focus:outline-gray-300" placeholder="First name" required />
                <input id="last_name" data-testid="last-name-input" ref={lastNameRef} type="text" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 ml-2 focus:outline-gray-300" placeholder="Last name" required />
            </div>
            <div className="grid grid-rows-4">
                <input id="username" data-testid="username-input" ref={usernameRef} onChange={async() => {await checkUsernameExist()}} type="text" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Username" required />
                {usernameData.exist && <span data-testid="username-span" className="h-[20px] py-1 text-center text-sm text-red-500">Такой пользователь уже существует! Доступное имя: "{usernameData.available}".</span>}
                <input id="email" data-testid="email-input" ref={emailRef} onChange={async () => {await checkEmailExist()}} type="email" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Email" required />
                {isEmailExist && <span data-testid="email-span" className="h-[20px] py-1 text-center text-sm text-red-500">Пользователь с таким электронным адресом уже существует!</span>}
                <input id="password" data-testid="password-input" ref={passwordRef} onChange={async () => {await checkPassword()}} type="password" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Password" required />
                {passwordState && <span data-testid="password-span" className="h-[50px] py-1 text-center text-sm text-red-500">Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!</span>}
                <button type="submit" className="bg-indigo-700 py-1 px-2 rounded-md text-white mt-2 hover:bg-indigo-600">Зарегистрироваться</button>
            </div>
        </form>
    );
};