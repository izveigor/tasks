import React, { useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import RecentTasks from '../containers/RecentTasks';
import CurrentTask from '../containers/CurrentTask';
import { USERS_URL } from '../features/constants';

export default function Main() {
    const navigate = useNavigate();

    useEffect(() => {
        let token = localStorage.getItem("token");
        if(token == null) {
            navigate("../confirm");
        }
        fetch(USERS_URL + "authorization_with_email/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.status === 401) {
                navigate("../confirm");
            }
        })
        .catch((error) => navigate("../confirm"))
    }, []);

    return (
        <div className="grid grid-cols-2 gap-10">
            <RecentTasks />
            <CurrentTask />
        </div>
    );
};