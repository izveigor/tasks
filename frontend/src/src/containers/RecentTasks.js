import React, { useState, useEffect } from 'react';
import { TASKS_URL } from '../features/constants';
import NoTasks from '../components/RecentTasks/NoTasks';
import Tasks from '../components/RecentTasks/Tasks';
import { useSelector } from 'react-redux';


export default function RecentTasks() {
    const token = useSelector((state) => state.user.token);

    const [recentTasksData, changeRecentTasksData] = useState([]);
    const [showNoTasks, changeShowNoTasks] = useState(true);

    async function getRecentTasks() {
        await fetch(TASKS_URL + "tasks/?page=1", {
            method: 'GET',
            headers: {
                "Authorization": "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                return response.json();
            } else {
                return null;
            }
        })
        .then((data) => {
            if(data !== null) {
                changeShowNoTasks(false);
                changeRecentTasksData(data);
            }
        })
    };

    useEffect(() => {
        getRecentTasks();
    }, []);

    return (
        <div className="rounded-md bg-white py-2 md:col-span-1 col-span-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">История заданий:</h1>
            </div>
            <div>
                {showNoTasks ?
                <NoTasks />
                : <Tasks tasks={recentTasksData} />
                }
            </div>
        </div>
    );
};