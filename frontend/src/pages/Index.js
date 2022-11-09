import React, { useEffect } from 'react';
import InformationAboutSite from '../containers/InformationAboutSite';
import RegisterLoginForm from '../containers/RegisterLoginForm';
import { useNavigate } from 'react-router-dom';
import { USERS_URL } from '../features/constants';


export default function Index() {
    const navigate = useNavigate();
    useEffect(() => {
        let token = localStorage.getItem("token");
        if(token != null) {
            fetch(USERS_URL + "authorization/", {
                method: "GET",
                headers: {
                    "Authorization": "Token " + token,
                }
            })
            .then((response) => {
                if (response.status !== 401) {
                    navigate("/main");
                }
            })
        }
    }, [])

    return (
        <div className="inline h-32 grid gap-5 md:grid-cols-2 mt-8">
            <InformationAboutSite />
            <RegisterLoginForm />
        </div>
    );
};