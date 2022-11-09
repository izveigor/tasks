import React, { useState, useEffect, useRef } from "react";
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from "../features/constants";
import { useNavigate } from "react-router-dom";


export default function Permission() {
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    const supervisorRef = useRef(null);
    const subordinateRef = useRef(null);

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
    }, [])

    return (
        <form class="bg-white rounded-md py-2 px-2">
            <div class="text-center py-2">
                <h1 class="text-2xl">Дать разрешение:</h1>
            </div>
            <div class="px-6 mb-6 w-100 grid grid-rows-12">
                <input onChange={getSupervisor} ref={supervisorRef} class="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Руководитель:" required />
                {showSupervisorUser && (<div class="flex">
                    <div class="ml-3 w-[3em] h-[3em]">
                        <img class="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + supervisorUserData.image} />
                    </div>
                    <div class="ml-[1em] grid">
                        <span>{supervisorUserData.user.first_name + " " + supervisorUserData.user.last_name}</span>
                        <span class="text-sm text-gray-600">{supervisorUserData.user.username}</span>
                    </div>
                </div>)}
                {showNoFoundSupervisor && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
                <input onChange={getSubordinate} ref={subordinateRef} class="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Подчиненный:" required />
                {showSubordinateUser && (<div class="flex">
                    <div class="ml-3 w-[3em] h-[3em]">
                        <img class="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + subordinateUserData.image} />
                    </div>
                    <div class="ml-[1em] grid">
                        <span>{subordinateUserData.user.first_name + " " + subordinateUserData.user.last_name}</span>
                        <span class="text-sm text-gray-600">{subordinateUserData.user.username}</span>
                    </div>
                </div>)}
                {showNoFoundSubordinate && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
            </div>
            <div class="flex justify-center">
                <button type="submit" class="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Отправить</button>
            </div>
        </form>
    );
};