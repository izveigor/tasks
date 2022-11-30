import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { TASKS_URL, USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';
import { useSelector } from 'react-redux';


export default function CreateTask() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isCreator = useSelector((state) => state.user.isCreator);

    const usernameRef = useRef(null);
    const previousRef = useRef(null);
    const subsequentRef = useRef(null);
    const titleRef = useRef(null);
    const timeRef = useRef(null);
    const descriptionRef = useRef(null);

    const [showNoFound, changeShowNoFound] = useState(false);
    const [showUserData, changeShowUserData] = useState(false);
    const [userData, changeUserData] = useState(false);
    
    const numberRegex = new RegExp("[0-9]");

    const [previousIds, changePreviousIds] = useState([]);
    const [subsequentIds, changeSubsequentIds] = useState([]);

    const [showErrorPreviousIds, changeShowErrorPreviousIds] = useState(false);
    const [showErrorSubsequentIds, changeShowErrorSubsequentIds] = useState(false);

    const [showPreviousIds, changeShowPreviousIds] = useState(false);
    const [showSubsequentIds, changeShowSubsequentIds] = useState(false);

    const [successCreated, changeSuccessCreated] = useState(false);

    const addPreviousId = () => {
        let value = previousRef.current.value;
        if(value.match(numberRegex)) {
            const index = previousIds.indexOf(value);
            if (index === -1) {
                changePreviousIds([...previousIds, value]);
                changeShowErrorPreviousIds(false);
                changeShowPreviousIds(true);
            }
        } else {
            changeShowErrorPreviousIds(true);
            changeShowPreviousIds(false);
        }
    };

    const addSubsequentId = () => {
        let value = subsequentRef.current.value;
        if(value.match(numberRegex)) {
            const index = subsequentIds.indexOf(value);
            if (index === -1) {
                changeSubsequentIds([...subsequentIds, value])
                changeShowErrorSubsequentIds(false);
                changeShowSubsequentIds(true);
            }
        } else {
            changeShowErrorSubsequentIds(true);
            changeShowSubsequentIds(false);
        }
    };

    const removePreviousId = (event, item) => {
        const index = previousIds.indexOf(item);
        if (index > -1) {
            changePreviousIds([
                ...previousIds.slice(0, index),
                ...previousIds.slice(index + 1)
            ]);
        }
    };

    const removeSubsequentId = (event, item) => {
        const index = subsequentIds.indexOf(item);
        if (index > -1) {
            changeSubsequentIds([
                ...subsequentIds.slice(0, index),
                ...subsequentIds.slice(index + 1)
            ]);
        }
    };

    async function getEmployee() {
        await fetch(USERS_URL + "suggest_employee/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                username: usernameRef.current.value,
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
                changeUserData(data);
                changeShowUserData(true);
                changeShowNoFound(false);
            } else {
                changeShowNoFound(true);
                changeShowUserData(false);
            }
        })
    }

    useEffect(() => {
        if(token == null || !isCreator) {
            navigate("/confirm");
        }
    }, []);

    function createTask(event) {
        fetch(TASKS_URL + "tasks/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Token " + token,
            },
            body: JSON.stringify({
                previous_tasks_ids: previousIds,
                subsequent_tasks_ids: subsequentIds,
                title: titleRef.current.value,
                time: timeRef.current.value,
                description: descriptionRef.current.value,
                receiver_username: usernameRef.current.value,
            })
        })
        .then((response) => {
            if(response.status === 201) {
                changeSuccessCreated(true);
            }
        })
        event.preventDefault();
    }

    return (
        <div className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Создать задание:</h1>
            </div>
            <form onSubmit={createTask} className="px-6 mb-6 w-100 grid grid-rows-12">
                <input data-testid="employee-input" ref={usernameRef} onChange={getEmployee} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Выберите сотрудника:" required />
                {showUserData && (<div data-testid="employee-data" className="flex">
                    <div className="ml-3 w-[3em] h-[3em]">
                        <img data-testid="employee-image" className="rounded-full align-middle" src={USERS_URL_WITHOUT_SLASH + userData.image} />
                    </div>
                    <div className="ml-[1em] grid">
                        <span data-testid="employee-fullname">{userData.user.first_name + " " + userData.user.last_name}</span>
                        <span data-testid="employee-username" className="text-sm text-gray-600">{userData.user.username}</span>
                    </div>
                </div>)}
                {showNoFound && <span className="h-[20px] py-1 text-md text-gray-600">Не найдено ни одной команды!</span>}
                <input data-testid="title-input" ref={titleRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Название задания:" required />
                <input data-testid="time-input" ref={timeRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" type="time" required />
                <div>
                    <input data-testid="previous-input" ref={previousRef} className="border pl-[14px] w-[74%] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Предыдущее задание:" />
                    <button data-testid="previous-button" onClick={() => addPreviousId()} type="button" className="bg-indigo-700 py-1 px-2 w-[25%] ml-[3px] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Добавить</button>
                </div>
                {showErrorPreviousIds && <span className="h-[20px] py-1 text-sm text-red-500">Вводить можно только десятичные числа (id заданий)!</span>}
                <div className="grid mt-2 gap-3 grid-cols-8">
                    {showPreviousIds && previousIds.map((item, index) => (<div data-testid="previous-badge" key={index} className="text-center w-[5em] text-white bg-sky-600 rounded-full py-1 px-1">
                        {item} <button onClick={(event) => removePreviousId(event, item)} type="button" className="align-middle mb-[0.1em] hover:text-gray-200"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg></button>
                    </div>))}
                </div>
                <div>
                    <input data-testid="subsequent-input" ref={subsequentRef} className="border pl-[14px] w-[74%] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Последующее задание:" />
                    <button data-testid="subsequent-button" onClick={() => addSubsequentId()} type="button" className="bg-indigo-700 py-1 px-2 w-[25%] ml-[3px] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Добавить</button>
                </div>
                {showErrorSubsequentIds && <span className="h-[20px] py-1 text-sm text-red-500">Вводить можно только десятичные числа (id заданий)!</span>}
                <div className="grid mt-2 gap-3 grid-cols-8">
                    {showSubsequentIds && subsequentIds.map((item, index) => (<div data-testid="subsequent-badge" key={index} className="text-center w-[5em] text-white bg-sky-600 rounded-full py-1 px-1">
                        {item} <button onClick={(event) => removeSubsequentId(event, item)} type="button" className="align-middle mb-[0.1em] hover:text-gray-200"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>))}
                </div>
                <textarea data-testid="description-textarea" ref={descriptionRef} style={{resize: "none"}} className="h-[10em] w-100 border pl-[14px] grid border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Введите описание задания:"></textarea>
                <div className="flex justify-center">
                    <button data-testid="create-button" type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Опубликовать</button>
                </div>
            </form>
            {successCreated && <span data-testid="created-successfully" className="h-[20px] py-1 text-sm text-green-500">Задание успешно создано!</span>}
        </div>
    );
};