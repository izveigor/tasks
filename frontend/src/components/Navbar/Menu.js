import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { USERS_URL } from '../../features/constants';


export default function Menu(props) {
    let token = localStorage.getItem("token");
    const [showCreatorTeamMenu, changeShowCreatorTeamMenu] = useState(false);

    useEffect(() => {
        token = localStorage.getItem("token");
        fetch(USERS_URL + "check_creator_team/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if (response.ok) {
                changeShowCreatorTeamMenu(true);
            }
        })
    })

    return (
        <ul className="flex w-50 items-baseline justify-between mt-1">
            <li>
                <Link to={token ? "/main" : "/"} className="bg-gray-800 text-white ml-10 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                    Главная
                </Link>
            </li>
            {props.isTeammate && <li>
                <Link to="/team" className="bg-gray-800 text-white ml-10 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                    Команда
                </Link>
            </li>}
            <li>
                <Link to="/about" className="bg-gray-800 text-white ml-10 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                    О нас
                </Link>
            </li>
            {showCreatorTeamMenu && <li>
                <Link to="/create_task" className="bg-gray-800 text-white ml-10 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                    Создать задание
                </Link>
            </li>
            }
        </ul>
    );
};