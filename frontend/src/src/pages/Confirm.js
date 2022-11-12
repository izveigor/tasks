import React, { useEffect, useState, useRef } from 'react';
import { USERS_URL } from '../features/constants';
import './Confirm.css';
import { useNavigate } from 'react-router-dom';


export default function ConfirmEmail() {
    const [attemptsNumber, changeAttemptsNumber] = useState(0);
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    const firstNumber = useRef(null);
    const secondNumber = useRef(null);
    const thirdNumber = useRef(null);
    const fourthNumber = useRef(null);
    const fifthNumber = useRef(null);
    const sixthNumber = useRef(null);

    async function getAttemptsNumber() {
        await fetch(USERS_URL + "confirm_email/", {
            method: 'GET',
            headers: {
                "Authorization": "Token " + token,
            }
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.available_tries === 0) {
                navigate("..");
            } else {
                changeAttemptsNumber(data.available_tries);
            }
        })
    };

    function checkCode(event) {
        let code = (firstNumber.current.value +
                   secondNumber.current.value +
                   thirdNumber.current.value +
                   fourthNumber.current.value +
                   fifthNumber.current.value +
                   sixthNumber.current.value);
        fetch(USERS_URL + "confirm_email/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "Authorization": "Token " + token,
            },
            body: JSON.stringify({
                "code": code,
            })

        })
        .then((res) => res.json())
        .then((data) => {
            if(data.confirmed) {
                navigate("../main");
            } else {
                changeAttemptsNumber(data.available_tries)
            }
        })
        event.preventDefault();
    };

    useEffect(() => {
        getAttemptsNumber()
        let token = localStorage.getItem("token");
        if(token == null) {
            navigate("..");
        }
        fetch(USERS_URL + "authorization/", {
            method: "GET",
            headers: {
                "Authorization": "Token " + token,
            }
        })
        .then((response) => {
            if (response.status === 401) {
                navigate("..");
            }
        })
        .catch((error) => navigate(".."))

        fetch(USERS_URL + "authorization_with_email/", {
            method: "GET",
            headers: {
                "Authorization": "Token " + token,
            }
        }).then((response) => {
            if(response.ok) {
                navigate("../main");
            }
        })
    }, [])

    return (
            <div className="flex justify-center">
                <form onSubmit={checkCode} className="w-[32.5em] mt-10 bg-white rounded-md px-[4em] py-3">
                    <h1 className="text-center text-2xl">Введите проверочный код:</h1>
                    <div className="flex justify-between mt-2">
                        <input type="text" pattern="\d*" maxLength="1" ref={firstNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                        <p className="mt-5">—</p>
                        <input type="text" pattern="\d*" maxLength="1" ref={secondNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                        <p className="mt-5">—</p>
                        <input type="text" pattern="\d*" maxLength="1" ref={thirdNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                        <p className="mt-5">—</p>
                        <input type="text" pattern="\d*" maxLength="1" ref={fourthNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                        <p className="mt-5">—</p>
                        <input type="text" pattern="\d*" maxLength="1" ref={fifthNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                        <p className="mt-5">—</p>
                        <input type="text" pattern="\d*" maxLength="1" ref={sixthNumber} className="border pl-[18px] w-[3em] h-[3em] border-gray-400 py-2 px-2 rounded-md placeholder-gray-400 mt-2 focus:outline-gray-300" placeholder="0" required />
                    </div>
                    <div className="text-center mt-2">
                        <span className="text-sm">У вас осталось {attemptsNumber} попытки!</span>
                    </div>
                    <div className="flex justify-center mt-2">
                        <button type="submit" className="bg-indigo-700 py-1 px-2 w-[10em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Отправить</button>
                    </div>
                </form>
            </div>
    );
};