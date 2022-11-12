import React from 'react';
import NotificationMenuItem from "./NotificationMenuItem";


export default function NotificationMenu(props) {
    return (
        <div data-testid="notification-menu-test">
            <div className="absolute z-10 w-0 h-0 border-[5px] ml-[0.4em] mt-[1.9em]" style={{borderColor: "transparent transparent white transparent"}}></div>
            <div className="absolute w-[16em] z-10 mt-[2.5em] ml-[-14.5em] rounded-md bg-white py-1 px-2 shadow-lg">
                {props.notifications !== undefined && props.notifications.map((notification, number) => (<div data-testid={"notification-" + number.toString()} key={number.toString()}><NotificationMenuItem text={notification.text} image={notification.image} time={notification.time} /></div>))}
            </div>
        </div>
    );
};