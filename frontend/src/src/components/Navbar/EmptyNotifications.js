import React from 'react';


export default function EmptyNotifications() {
    return (
        <span data-testid="empty-notifications-test" className="text-center hover:text-gray-400 text-md text-gray-500 py-[2em] px-[2em]">
            Уведомления отсутствуют!
        </span>
    );
};