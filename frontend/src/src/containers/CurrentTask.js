import React, { useState, useEffect } from 'react';
import { TASKS_URL, USERS_URL } from '../features/constants';
import Task from '../components/CurrentTask/Task';
import JoinOrCreateTeam from '../components/CurrentTask/JoinOrCreateTeam';
import { useSelector } from 'react-redux';


export default function CurrentTask() {
    const [currentTaskData, changeCurrentTaskData] = useState({});
    const [showTeamButtons, changeShowTeamButtons] = useState(true);

    const isTeammate = useSelector((state) => state.user.isTeammate);
    const token = useSelector((state) => state.user.token);

    function close(event, status) {
        fetch(TASKS_URL + "close/", {
            method: "PUT",
            headers: {
                'Authorization': "Token " + token,
                'Content-Type': "application/json",
            },
            body: JSON.stringify({
                status: status,
            }),
        }).then((response) => {
            if (response.ok) {
                changeShowTeamButtons(true);
                changeCurrentTaskData({});
            }
        })
    };

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
            }
        })
    };

    useEffect(() => {
        if(isTeammate) {
            getCurrentTask();
        }
    }, []);

    return (
        <div>
            {showTeamButtons ?
                <JoinOrCreateTeam isTeammate={isTeammate} />
                : <Task close={close} task={showTeamButtons ? null : currentTaskData}/>
            }
        </div>
    );
};