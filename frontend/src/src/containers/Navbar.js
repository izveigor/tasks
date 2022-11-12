import React, { useEffect, useState } from 'react';
import Avatar from '../components/Navbar/Avatar';
import Bell from '../components/Navbar/Bell';
import Menu from '../components/Navbar/Menu';
import { USERS_URL } from '../features/constants';


export default function Navbar() {
    const [avatar, changeAvatar] = useState({});
    const [showAvatar, changeShowAvatar] = useState(false);

    const [isAdmin, changeIsAdmin] = useState(false);
    const [isTeammate, changeIsTeammate] = useState(false);

    let token = localStorage.getItem("token");

    async function AuthorizationLikeTeammate() {
        fetch(USERS_URL + "check_team/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                changeIsTeammate(true);
            }
        })
    }
    
    async function AuthorizationLikeAdmin() {
        fetch(USERS_URL + "check_admin/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                changeIsAdmin(true);
            }
        })
    }

    useEffect(() => {
            fetch(USERS_URL + "avatar/", {
                method: "GET",
                headers: {
                    'Authorization': "Token " + token,
                }
            })
            .then((response) => {
                if(response.ok) {
                    return response.json()
                } else {
                    return null;
                }
            })
            .then((data) => {
                if (data !== null) {
                    changeShowAvatar(true);
                    changeAvatar(data);
                }
            })
            AuthorizationLikeAdmin();
            AuthorizationLikeTeammate();
    }, [])

    return (
        <nav className="w-100 py-5 bg-gray-800 flex justify-between">
            <div>
                <Menu isTeammate={isTeammate} />
            </div>
            {showAvatar && (<div>
                <div className="flex justify-between gap-4">
                    <Bell />
                    <Avatar isAdmin={isAdmin} isTeammate={isTeammate} avatar={avatar} />
                </div>
            </div>)}
        </nav>
    );
};