import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL_WITHOUT_SLASH, USERS_URL } from '../features/constants';


export default function TeamSettings() {
    const navigate = useNavigate();
    const defaultImage = USERS_URL + "images/default.png";
    const [isTeamNameExist, changeTeamNameExist] = useState(false);
    const [selectedImage, setSelectedImage] = useState(defaultImage);
    const [selectedImageSrc, setSelectedImageSrc] = useState(null);
    const [successChanged, changeSuccessChanged] = useState(false);

    const [currentSettings, changeCurrentSettings] = useState({});

    const token = localStorage.getItem("token");
    const teamNameRef = useRef(null);
    const descriptionRef = useRef(null);

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            let reader = new FileReader();
            setSelectedImageSrc(URL.createObjectURL(event.target.files[0]));
            setSelectedImage(event.target.files[0]);
        }
    }

    async function getCurrentSettings() {
        await fetch(USERS_URL + "team/", {
            method: 'GET',
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => response.json())
        .then((data) => changeCurrentSettings(data))
    }

    useEffect(() => {
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
        getCurrentSettings()
    }, []);

    async function checkTeamName() {
        await fetch(USERS_URL + "check_team_name/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: teamNameRef.current.value,
            })
        })
        .then((res) => res.json())
        .then((data) => changeTeamNameExist(data.exist))
    };

    function changeTeamSettings(event) {
        if(!isTeamNameExist) {
            let form_data = new FormData()
            form_data.append('image', selectedImage, selectedImage.name);
            form_data.append('name', teamNameRef.current.value);
            form_data.append('description', descriptionRef.current.value);

            fetch(USERS_URL + "team/", {
                method: 'PUT',
                headers: {
                    'Authorization': "Token " + token,
                },
                body: form_data,
            })
            .then((response) =>{
                if(response.ok) {
                    changeSuccessChanged(true);
                }
            })
        };
        event.preventDefault();
    };

    return (
        <form onSubmit={changeTeamSettings} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Настройки команды:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <div className="mb-2">
                    <img className="h-[8em] w-[8em] object-cover rounded-full" src={selectedImageSrc ? selectedImageSrc : USERS_URL_WITHOUT_SLASH + currentSettings.image} alt="Current team image" />
                <label id="change-picture" htmlFor="picture" type="button" className="w-[2em] h-[2em] absolute mt-[-2.3em] ml-[1.3em] bg-white text-sm border border-gray-400 rounded-md px-1 py-1 hover:bg-gray-200">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                    </svg>
                <input onChange={onImageChange} hidden={true} style={{ zIndex: -1 }} id="picture" type="file" className="absolute w-[0.1px] h-[0.1px]" />
                </label>
                </div>
                <input defaultValue={currentSettings.name} onChange={async () => {await checkTeamName()}} ref={teamNameRef} type="text" className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Название команды:" required />
                {isTeamNameExist && <span data-testid="team-name-span-test" className="h-[20px] py-1 text-center text-sm text-red-500">Команда с таким именем уже существует!</span>}
                <textarea ref={descriptionRef} type="text" style={{resize: "none"}} className="h-[10em] w-100 border pl-[14px] grid border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Введите описание команды:" defaultValue={currentSettings.description}></textarea>
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Изменить</button>
            </div>
            <div className="text-center mt-2">
                {successChanged && <span className="h-[20px] py-1 text-sm text-green-500">Настройки команды были успешно изменены!</span>}
            </div>
        </form>
    );
};