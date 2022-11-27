import React from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';


export default function Menu(props) {
    const token = useSelector((state) => state.user.token);
    const isCreator = useSelector((state) => state.user.isCreator);

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
            {isCreator && <li>
                <Link to="/create_task" className="bg-gray-800 text-white ml-10 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                    Создать задание
                </Link>
            </li>
            }
        </ul>
    );
};