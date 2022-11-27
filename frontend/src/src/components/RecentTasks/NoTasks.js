import React from 'react';


export default function NoTasks() {
    return (
        <div className="text-center my-[10em]">
            <h1 data-testid="empty-tasks" className="text-xl text-gray-600">Задания отсутствуют!</h1>
        </div>
    );
};