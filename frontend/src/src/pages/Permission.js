import React, { useState, useEffect, useRef } from "react";
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from "../features/constants";
import { useNavigate } from "react-router-dom";
import { useSelector } from 'react-redux';


export default function Permission() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isEmailConfirmed = useSelector((state) => state.user.isEmailConfirmed);
    const isAdmin = useSelector((state) => state.user.isAdmin);

    const supervisorRef = useRef(null);
    const subordinateRef = useRef(null);

    const [showSuccessMessage, changeShowSuccessMessage] = useState(false);
    const [supervisorUserData, changeSupervisorUserData] = useState({});
    const [subordinateUserData, changeSubordinateUserData] = useState({});
    const [showSupervisorUser, changeShowSupervisorUser] = useState(false);
    const [showSubordinateUser, changeSubordinateUser] = useState(false);
    const [showNoFoundSupervisor, changeShowNoFoundSupervisor] = useState(false);
    const [showNoFoundSubordinate, changeShowNoFoundSubordinate] = useState(false);

    async function getSupervisor() {
        await fetch(USERS_URL + "suggest_employee/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                username: supervisorRef.current.value,
            })
        })
        .then((response) => {
            if(response.ok) {
                return response.json();
            } else {
                return null;
            }
        })
        .then((data) => {
            if (data !== null) {
                changeShowSupervisorUser(true);
                changeSupervisorUserData(data);
                changeShowNoFoundSupervisor(false)
            } else {
                changeShowSupervisorUser(false);
                changeShowNoFoundSupervisor(true);
            }
        })
    }

    async function getSubordinate() {
        await fetch(USERS_URL + "suggest_employee/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                username: subordinateRef.current.value,
            })
        })
        .then((response) => {
            if(response.ok) {
                return response.json();
            } else {
                return null;
            }
        })
        .then((data) => {
            if (data !== null) {
                changeSubordinateUser(true);
                changeSubordinateUserData(data);
                changeShowNoFoundSubordinate(false);
            } else {
                changeSubordinateUser(false);
                changeShowNoFoundSubordinate(true);
            }
        })
    }

    function getPermission(event) {
        fetch(USERS_URL + "/permission", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                supervisor: supervisorRef.current.value,
                subordinate: subordinateRef.current.value,
            })
        }).then((response) => {
            if(response.ok) {
                changeShowSuccessMessage(true);
            }
        })
        event.preventDefault();
    }
    useEffect(() => {
        if(token == null || !isEmailConfirmed || !isAdmin) {
            navigate("/confirm");
        }
    }, [])

    return (
        <form onSubmit={getPermission} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Дать разрешение:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input data-testid="supervisor-input" onChange={getSupervisor} ref={supervisorRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Руководитель:" required />
                {showSupervisorUser && (<div data-testid="supervisor" className="flex">
                    <div className="ml-3 w-[3em] h-[3em]">
                        <img data-testid="supervisor-image" className="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + supervisorUserData.image} />
                    </div>
                    <div className="ml-[1em] grid">
                        <span data-testid="supervisor-fullname">{supervisorUserData.user.first_name + " " + supervisorUserData.user.last_name}</span>
                        <span data-testid="supervisor-username" className="text-sm text-gray-600">{supervisorUserData.user.username}</span>
                    </div>
                </div>)}
                {showNoFoundSupervisor && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
                <input data-testid="subordinate-input" onChange={getSubordinate} ref={subordinateRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Подчиненный:" required />
                {showSubordinateUser && (<div data-testid="subordinate" className="flex">
                    <div className="ml-3 w-[3em] h-[3em]">
                        <img data-testid="subordinate-image" className="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + subordinateUserData.image} />
                    </div>
                    <div className="ml-[1em] grid">
                        <span data-testid="subordinate-fullname">{subordinateUserData.user.first_name + " " + subordinateUserData.user.last_name}</span>
                        <span data-testid="subordinate-username" className="text-sm text-gray-600">{subordinateUserData.user.username}</span>
                    </div>
                </div>)}
                {showNoFoundSubordinate && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Отправить</button>
            </div>
            {showSuccessMessage && <span data-testid="set-permission-successfully" className="h-[20px] py-1 text-sm text-green-500">Пользователь {supervisorRef.current.value} стал руководителем для пользователя {subordinateRef.current.value}!</span>}
        </form>
    );
};