import React from 'react';
import { useNavigate } from 'react-router';
import { TASKS_URL } from '../../features/constants';


export default function Task(props) {
    const token = localStorage.getItem("token");
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
        })
    }

    return (
        <div className="rounded-md bg-white py-2 md:col-span-1 col-span-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Текущее задание:</h1>
            </div>
            <hr className="border-gray-300" />
            <div className="mt-4 px-2">
            <div className="mt-5 text-center">
                <h2 className="text-xl" data-testid="task-title-test">{props.task.title} #{props.task.id}</h2>
            </div>
            <div style={{overflowY: "scroll"}} className="mt-4 border-dashed border-2 border-gray-300 h-[10em] py-2 px-2">
                <span data-testid="task-description-test">{props.task.description}</span>
            </div>
            <div className="text-center mt-4">
                <span className="text-xl text-gray-400" data-testid="task-time-test">{props.task.time.replace('T', ' ').split('.')[0]}</span>
            </div>
                <div className="mt-5 flex justify-center">
                    <button onClick={(event) => close(event, "Успешно")} className="mr-4 w-[10em] bg-green-200 hover:bg-green-100 py-2 px-2 text-green-600 rounded-md">
                        Закрыть успешно
                    </button>
                    <button onClick={(event) => close(event, "Закрыто")} className="ml-4 w-[10em] bg-red-200 hover:bg-red-100 py-2 px-2 text-red-600 rounded-md">
                        Закрыть
                    </button>
                </div>
            </div>
        </div>
    );
};