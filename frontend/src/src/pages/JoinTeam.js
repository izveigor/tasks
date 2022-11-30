import React, { useState, useRef, useEffect } from 'react';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';


export default function JoinTeam() {
    const navigate = useNavigate();
    
    const token = useSelector((state) => state.user.token);
    const isTeammate = useSelector((state) => state.user.isTeammate);

    const [suggestedTeam, changeSuggestedTeam] = useState({});
    const [showSuggestedTeam, changeShowSuggestedTeam] = useState(false);
    const [nameDoesNotExist, changeNameDoesNotExist] = useState(false);
    const [showSuccessMessage, changeShowSuccessMessage] = useState(false);
    const [showNoFound, changeShowNoFound] = useState(false);

    const teamNameRef = useRef(null);

    function Authorization() {
        if(isTeammate) {
            navigate("../main");
        }
    }

    useEffect(() => {
        Authorization();
    }, [])

    function joinTeam(event) {
        fetch(USERS_URL + "join/", {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                name: teamNameRef.current.value,
            }),
        })
        .then((response) => {
            if (response.ok) {
                return true;
            } else {
                return false;
            }
        })
        .then((data) => {
            if (data) {
                changeNameDoesNotExist(false);
                changeShowSuccessMessage(true);
            } else {
                changeNameDoesNotExist(true);
                changeShowSuccessMessage(false);
            }
        })
        event.preventDefault();
    }

    async function suggestTeam() {
        await fetch(USERS_URL + "suggest_team/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                name: teamNameRef.current.value,
            }),
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
                changeShowSuggestedTeam(true);
                changeSuggestedTeam(data);
                changeShowNoFound(false);
            } else {
                changeShowNoFound(true);
                changeShowSuggestedTeam(false);
            }
        })
    };

    return (
        <form onSubmit={joinTeam} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Присоединиться к команде:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input data-testid="name-input" onChange={async() => await suggestTeam()} ref={teamNameRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Название команды:" required />
            </div>
            {showSuggestedTeam && (<div data-testid="team-information" className="flex">
                <div className="ml-3 w-[3em] h-[3em]">
                    <img data-testid="team-image" className="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + suggestedTeam.image} />
                </div>
                <div className="ml-[1em] grid">
                    <span data-testid="team-name">{suggestedTeam.name}</span>
                </div>
            </div>)}
            {showNoFound && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Отправить</button>
            </div>
            {nameDoesNotExist && <span className="h-[20px] py-1 text-sm text-red-500">Такой команды не существует!</span>}
            {showSuccessMessage && <span className="h-[20px] py-1 text-sm text-green-500">Вы отправили заявку на вступление в команду!</span>}
        </form>
    );
};