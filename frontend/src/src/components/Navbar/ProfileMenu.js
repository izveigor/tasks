import React, { useState, useEffect } from 'react';
import {
    Link,
    useNavigate,
} from 'react-router-dom';
import { USERS_URL } from '../../features/constants';


export default function ProfileMenu(props) {
    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    const signOut = () => {
        localStorage.removeItem("token");
        navigate("../confirm");
    };

    const leaveTeam = () => {
        fetch(USERS_URL + "leave_team/", {
            method: "DELETE",
            headers: {
                'Authorization': "Token " + token,
            }
        })
    };

    const deleteTeam = () => {
        fetch(USERS_URL + "team/", {
            method: "DELETE",
            headers: {
                'Authorization': "Token " + token,
            }
        }).then((response) => {
            if(response.ok) {
                localStorage.removeItem("token");
                navigate("../confirm");
            }
        })
    }

    return (
        <div data-testid="profile-menu">
            <div className="absolute z-10 w-0 h-0 border-[5px] ml-[0.6em]" style={{borderColor: "transparent transparent white transparent"}}></div>
            <div className="absolute drop-shadow-md ml-[-10em] z-10 mt-2 w-48 rounded-md bg-white py-1 shadow-lg">
                <ul>
                    <li><Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200">Мой профиль</Link></li>
                    <li><Link to="/settings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200">Настройки</Link></li>
                    <li><Link onClick={signOut} data-testid="sign-out" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 text-red-600">Выйти</Link></li>
                    {(props.isAdmin || props.isTeammate) && <hr />}
                    {(props.isAdmin && props.isTeammate) && (
                        <div>
                            <li><Link to="/permission" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200">Дать разрешение</Link></li>
                            <li><Link to="/team_settings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200">Настройки команды</Link></li>
                            <li><Link data-testid="delete-team" onClick={deleteTeam} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 text-red-600">Удалить команду</Link></li>
                        </div>
                    )}
                    {(props.isTeammate && !props.isAdmin) && (
                        <li><Link onClick={leaveTeam} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-200 text-red-600">Выйти из команды</Link></li>
                    )}
                </ul>
            </div>
        </div>
    );
};