import React, { useEffect, useState } from 'react';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../../features/constants';
import { Link } from 'react-router-dom';


export default function NotificationMenuItem(props) {
    const token = localStorage.getItem("token");
    const [acceptLink, changeAcceptLink] = useState(false);

    useEffect(() => {
        if (props.text.search("присоединиться") !== -1) {
            changeAcceptLink(true);
        }
    }, [])

    async function Accept() {
        await fetch(USERS_URL + "accept/", {
            method: "PUT",
            headers: {
                'Authorization': "Token " + token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: props.text.replace('Пользователь "', '').replace('" хочет присоединиться к вашей команде!', '')
            }),
        })
        .then((response) => {
            if(response.ok) {
                changeAcceptLink(false);
            }
        })
    }

    return (
        <div>
            <span href="" className="hover:text-gray-500">
                <div className="float-left mr-2 mt-1">
                    <img data-testid="notification-image" className="h-8 w-8 rounded-full" src={USERS_URL_WITHOUT_SLASH + props.image} alt="" />
                </div>
                <div className="grid ml-2">
                    <span className="text-sm" data-testid="notification-text">{props.text} {acceptLink && (<Link className="text-red-500" onClick={async() => await Accept()}>Принять</Link>)}</span>
                    <span className="text-sm text-gray-500" data-testid="notification-time">{props.time}</span>
                </div>
            </span>
            <hr/>
        </div>
    );
};