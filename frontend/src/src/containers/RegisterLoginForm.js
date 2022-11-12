import React from 'react';
import { useState } from "react";

import FormName from "../components/RegisterForm/FormName";
import LoginForm from "../components/RegisterForm/LoginForm";
import RegisterForm from '../components/RegisterForm/RegisterForm';
import ChangeLoginRegisterButton from '../components/RegisterForm/ChangeLoginRegisterButton';


export default function RegisterLoginForm() {
    const [isRegisterForm, changeForm] = useState(true);
    const changeFormFunction = () => changeForm(!isRegisterForm);

    return (
        <div className="inline rounded-md bg-white py-5 px-5 text-center rounded-md">
            <FormName name={isRegisterForm ? "Форма регистрации:" : "Форма входа:"} />
            {isRegisterForm ? <RegisterForm /> : <LoginForm />}
            <ChangeLoginRegisterButton changeForm={changeFormFunction} name={isRegisterForm ? "Войти" : "Зарегистрироваться"} />
        </div>
    );
};