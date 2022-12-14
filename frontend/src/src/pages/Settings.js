import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';
import { useSelector } from 'react-redux';


export default function Settings() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isEmailConfirmed = useSelector((state) => state.user.isEmailConfirmed);

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
            reader.onload = () => {
                setSelectedImageSrc(URL.createObjectURL(event.target.files[0]));
                setSelectedImage(event.target.files[0]);
            }
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
        form_data.append('image', selectedImage);
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
        if(token === null || !isEmailConfirmed) {
            navigate("/confirm");
        }
        getCurrentUserData();
    }, []);

    return (
        <div className="bg-white rounded-md py-2 px-2 mt-5">
            <div className="text-center py-2">
                <h1 className="text-2xl">??????????????????:</h1>
            </div>
            {isLoaded && (<form onSubmit={changeSettings} className="px-6 mb-6 w-100 grid grid-rows-12">
                <div className="mb-2">
                    <img data-testid="settings-image" className="h-[8em] w-[8em] object-cover rounded-full" src={selectedImageSrc ? selectedImageSrc : USERS_URL_WITHOUT_SLASH + currentUserData.image} />
                    <label id="change-picture" htmlFor="picture" type="button" className="w-[2em] h-[2em] absolute mt-[-2.3em] ml-[1.3em] bg-white text-sm border border-gray-400 rounded-md px-1 py-1 hover:bg-gray-200">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                        </svg>
                        <input data-testid="settings-image-input" onChange={onImageChange} hidden={true} style={{zIndex: -1}} id="picture" type="file" className="absolute w-[0.1px] h-[0.1px]" />
                    </label>
                </div>
                <div className="grid grid-cols-2 gap-2">
                    <input data-testid="settings-first-name-input" ref={firstNameRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="??????" defaultValue={currentUserData.user.first_name} required />
                    <input data-testid="settings-last-name-input" ref={lastNameRef} className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="??????????????" defaultValue={currentUserData.user.last_name} required />
                </div>
                <input data-testid="settings-job-title-input" ref={jobTitleRef} className="border pl-[14px] border-gray-400 w-[100%] py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="??????????????????:" defaultValue={currentUserData.job_title} required />
                <textarea data-testid="settings-description-input" ref={descriptionRef} style={{resize: "none"}} className="h-[10em] w-[100%] border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="????????????????" defaultValue={currentUserData.description}></textarea>
                <div className="flex justify-center mt-2">
                    <button data-testid="change-button" type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">????????????????</button>
                </div>
            </form>)}
            <div className="flex justify-center gap-5 mt-2">
                <button onClick={changePassword} className="bg-red-700 py-1 px-2 w-[15em] text-white rounded-md h-[2.5em] hover:bg-red-600" type="button">?????????????? ????????????</button>
                <button onClick={changeUsername} className="bg-red-700 py-1 px-2 w-[15em] text-white rounded-md h-[2.5em] hover:bg-red-600" type="button">?????????????? ?????? ????????????????????????</button>
            </div>
            {successChanged && <span data-testid="changed-successfully" className="h-[20px] py-1 text-sm text-green-500">?????????????????? ???????? ?????????????? ????????????????!</span>}
        </div>
    );
};