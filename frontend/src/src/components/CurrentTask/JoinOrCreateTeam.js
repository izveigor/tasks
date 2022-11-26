import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TASKS_URL } from '../../features/constants';
import { useSelector } from 'react-redux';


export default function JoinOrCreateTeam(props) {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);

    const createTeam = () => navigate("../create_team");
    const joinTeam = () => navigate("../join");

    const [isProccessingExist, changeProcessingExist] = useState();

    async function ProcessingTasksExist() {
        await fetch(TASKS_URL + "processing/", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                "Authorization": "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                changeProcessingExist(true);
            } else {
                changeProcessingExist(false);
            }
        })
    };

    async function GetNextTask() {
        await fetch(TASKS_URL + "current_task/", {
            method: "PUT",
            headers: {
                "Authorization": "Token " + token,
            }
        })
    }

    useEffect(() => {
        ProcessingTasksExist();
    })

    return (
        <div className="content-center grid rounded-md bg-white py-2 md:col-span-1 col-span-2">
            {!props.isTeammate ? (
            <div className="text-center">
                <h1 className="text-lg text-gray-600 mb-2">Вы не находитесь в команде!</h1>
                <div>
                    <button data-testid="create-team" onClick={createTeam} className="bg-indigo-700 py-[0.5em] w-[15em] rounded-md text-white mt-2 hover:bg-indigo-600">
                        Создать команду
                    </button>
                </div>
                <div>
                    <button data-testid="join-team" onClick={joinTeam} className="bg-indigo-700 py-[0.5em] w-[15em] rounded-md text-white mt-2 hover:bg-indigo-600">
                        Присоединиться к команде
                    </button>
                </div>
            </div>) : (<div className="text-center">
            <h1 data-testid="empty-current-task" className="text-lg text-gray-600 mb-2">Текущее задание отсутвует!</h1>
            {props.isTeammate && isProccessingExist && (<div>
                <button onClick={() => GetNextTask()} className="bg-indigo-700 py-[0.5em] w-[15em] rounded-md text-white mt-2 hover:bg-indigo-600">
                    Начать следующее задание
                </button>
            </div>)}
        </div>)}
        </div>
    );
};