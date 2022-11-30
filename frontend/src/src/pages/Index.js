import React, { useEffect } from 'react';
import InformationAboutSite from '../containers/InformationAboutSite';
import RegisterLoginForm from '../containers/RegisterLoginForm';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';


export default function Index() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);

    useEffect(() => {
        if(token !== null) {
            navigate("/main");
        }
    }, [])

    return (
        <div className="inline h-32 grid gap-5 md:grid-cols-2 mt-8">
            <InformationAboutSite />
            <RegisterLoginForm />
        </div>
    );
};