import React, { useEffect } from 'react';

import { useNavigate } from 'react-router-dom';
import RecentTasks from '../containers/RecentTasks';
import CurrentTask from '../containers/CurrentTask';
import { USERS_URL } from '../features/constants';
import { useSelector } from 'react-redux';


export default function Main() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isEmailConfirmed = useSelector((state) => state.user.isEmailConfirmed);

    useEffect(() => {
        if(token == null || !isEmailConfirmed) {
            navigate("../confirm");
        }
    }, []);

    return (
        <div className="grid grid-cols-2 gap-10">
            <RecentTasks />
            <CurrentTask />
        </div>
    );
};