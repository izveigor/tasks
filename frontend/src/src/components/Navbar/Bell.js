import React from 'react';
import NotificationMenu from './NotificationMenu';
import { useRef, useEffect, useState, useCallback } from 'react';
import EmptyNotifications from './EmptyNotifications';
import { NOTIFICATION_URL, WS_NOTIFICATION_URL } from '../../features/constants';


export default function Bell(props) {
    const token = localStorage.getItem("token");
    const [notificationState, changeNotificationState] = useState(false);
    const [notifications, changeNotifications] = useState({});
    const [areNotificationsExist, changeAreNotificationsExist] = useState(false);
    const [numberUnreadNotifications, changeNumberUnreadNotifications] = useState(0);
    const [status, setStatus] = useState("");

    const ws = useRef(null);

    async function getNotifications() {
        await fetch(NOTIFICATION_URL + "notifications/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => response.json())
        .then((data) => {
            changeAreNotificationsExist(true)
            changeNotifications(data)
        })
    }

    async function getUnreadNotifications() {
        await fetch(NOTIFICATION_URL + "get_number_unread_notifications/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => response.json())
        .then((data) => changeNumberUnreadNotifications(data))
    }

    async function ReadNotifications() {
        await fetch(NOTIFICATION_URL + "clear_unread_notifications/", {
            method: "GET",
            headers: {
                'Authorization': "Token " + token,
            }
        })
        .then((response) => {
            if(response.ok) {
                changeNumberUnreadNotifications(0);
            }
        })
    }

    const gettingData = useCallback(() => {
        if(!ws.current) return;

        ws.current.onmessage = e => {
            const notification = JSON.parse(e.data);
            changeNotifications([
                notification,
                ...notifications.slice(0, 2)
            ]);
            changeNumberUnreadNotifications(numberUnreadNotifications+1);
        }
    })

    useEffect(() => {
        getNotifications();
        getUnreadNotifications();

        ws.current = new WebSocket(WS_NOTIFICATION_URL + "ws/notify");
        ws.current.onopen = () => setStatus("Соединение открыто");
        ws.current.onclose = () => setStatus("Соединение закрыто");

        gettingData()

    }, []);

    return (
        <div>
            <button onClick={async() => {
                changeNotificationState(previousNotificationState => !previousNotificationState)
                await ReadNotifications()
                if(props.onChange) { props.onChange(!notificationState) }
                }} type="button" className="text-white">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                    </svg>
                {numberUnreadNotifications > 0 && (
                    <div data-testid="notification-badge-test" className="absolute z-10 bg-red-500 px-1.5 py-1.5 rounded-full ml-[0.7em] mt-[-1.5em]">
                        <span data-testid="notications-length-test" className="absolute text-white text-[10px] bottom-[-1px] left-[3px]">{numberUnreadNotifications}</span>
                    </div>
                    )
                }
                </div>
            </button>
            <div className="rounded-md bg-white py-1 shadom-lg absolute">
                {notificationState && areNotificationsExist && <NotificationMenu notifications={notifications} /> }
                {notificationState && !areNotificationsExist && <EmptyNotifications />}
            </div>
        </div>
    );
};