import React, { useState, useEffect } from 'react';
import { TASKS_URL, USERS_URL } from '../features/constants';
import Task from '../components/CurrentTask/Task';
import JoinOrCreateTeam from '../components/CurrentTask/JoinOrCreateTeam';


export default function CurrentTask() {
    const [currentTaskData, changeCurrentTaskData] = useState({});
    const [showTeamButtons, changeShowTeamButtons] = useState(true);
    const [isTeammate, changeIsTeammate] = useState(false);

    let token = localStorage.getItem("token");

    async function TeamAuthorization() {
        await fetch(USERS_URL + "check_team/", {
            method: "GET",
            headers: {
                "Authorization": "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                changeIsTeammate(true);
            }
        })
    }

    async function getCurrentTask() {
        await fetch(TASKS_URL + "current_task/", {
            method: 'GET',
            headers: {
                "Authorization": "Token " + token,
            }
        })
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                return null;
            }
        })
        .then((data) => {
            if (data !== null) {
                changeShowTeamButtons(false);
                changeCurrentTaskData(data);
                TeamAuthorization();
            }
        })
    };

    useEffect(() => {
        TeamAuthorization();
        getCurrentTask();
    }, []);

    return (
        <div>
            {showTeamButtons ?
                <JoinOrCreateTeam isTeammate={isTeammate} />
                : <Task task={showTeamButtons ? null : currentTaskData}/>
            }
        </div>
    );
};