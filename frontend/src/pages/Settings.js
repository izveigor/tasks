import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';


export default function Settings() {
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    const [currentUserData, changeUserData] = useState({});
    const [selectedImage, setSelectedImage] = useState(null);
    const [selectedImageSrc, setSelectedImageSrc] = useState(null);
    const [successChanged, changeSuccessChanged] = useState(false);
    const [isLoaded, changeIsLoaded] = useState(false);

    const changePassword = () => navigate("../change_password");
    const changeUsername = () => navigate("../change_username");

    const firstNameRef = useRef(null);
    const lastNameRef = useRef(null);
    const jobTitleRef = useRef(null);
    const descriptionRef = useRef(null);

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            let reader = new FileReader();
            setSelectedImageSrc(URL.createObjectURL(event.target.files[0]));
            setSelectedImage(event.target.files[0]);
        }
    }

    function getCurrentUserData() {
        fetch(USERS_URL + "settings/", {
            method: 'GET',
            headers: {
                'Authorization': "Token " + token,
            },
        })
        .then((res) => res.json())
        .then((userData) => {
            changeUserData(userData)
            setSelectedImage(userData.image);
            changeIsLoaded(true);
        })
    };

    function changeSettings(event) {
        let form_data = new FormData();
        form_data.append('image', selectedImage, selectedImage.name);
        form_data.append('job_title', jobTitleRef.current.value);
        form_data.append('description', descriptionRef.current.value);
        form_data.append('first_name', firstNameRef.current.value);
        form_data.append('last_name', lastNameRef.current.value);

        fetch(USERS_URL + "settings/", {
            method: "PUT",
            headers: {
                'Authorization': "Token " + token,
            },
            body: form_data,
        })
        .then((response) => {
            if(response.ok) {
                changeSuccessChanged(true);
            }
        })
        event.preventDefault();
    }

    useEffect(() => {
        getCurrentUserData();
        if(token == null) {
            navigate("/confirm");
        }
        fetch(USERS_URL + "authorization_with_email/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.status === 403) {
                navigate("/confirm");
            }
        })
        .catch((error) => navigate("/confirm"))
    }, []);

    return (
        <div className="bg-white rounded-md py-2 px-2 mt-5">
            <div className="text-center py-2">
                <h1 className="text-2xl">Настройки:</h1>
            </div>
            {isLoaded && (<form onSubmit={changeSettings} className="px-6 mb-6 w-100 grid grid-rows-12">
                <div className="mb-2">
                    <img className="h-[8em] w-[8em] object-cover rounded-full" src={selectedImageSrc ? selectedImageSrc : USERS_URL_WITHOUT_SLASH + currentUserData.image} />
                    <label id="change-picture" htmlFor="picture" type="button" className="w-[2em] h-[2em] absolute mt-[-2.3em] ml-[1.3em] bg-white text-sm border border-gray-400 rounded-md px-1 py-1 hover:bg-gray-200">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />                
                        </svg>
                        <input onChange={onImageChange} hidden="true" style={{zIndex: -1}} id="picture" type="file" className="absolute w-[0.1px] h-[0.1px]" />
                    </label>
                </div>
                <div className="grid grid-cols-2 gap-2">
                    <input ref={firstNameRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Имя" defaultValue={currentUserData.user.first_name} required />
                    <input ref={lastNameRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Фамилия" defaultValue={currentUserData.user.last_name} required />
                </div>
                <input ref={jobTitleRef} className="border pl-[14px] border-gray-400 w-[100%] py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Должность:" defaultValue={currentUserData.job_title} required />
                <textarea ref={descriptionRef} style={{resize: "none"}} className="h-[10em] w-[100%] border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Описание" defaultValue={currentUserData.description}></textarea>
                <div className="flex justify-center mt-2">
                    <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Изменить</button>
                </div>
            </form>)}
            <div className="flex justify-center gap-5 mt-2">
                <button onClick={changePassword} className="bg-red-700 py-1 px-2 w-[15em] text-white rounded-md h-[2.5em] hover:bg-red-600" type="button">Сменить пароль</button>
                <button onClick={changeUsername} className="bg-red-700 py-1 px-2 w-[15em] text-white rounded-md h-[2.5em] hover:bg-red-600" type="button">Сменить имя пользователя</button>
            </div>
            {successChanged && <span className="h-[20px] py-1 text-sm text-green-500">Настройки были успешно изменены!</span>}
        </div>
    );
};