import React from 'react';

export default function About() {
    return (
        <div className="bg-white rounded-md inline py-2 px-2 grid">
            <div className="text-center my-2">
                <h1 className="text-2xl">О приложении:</h1>
            </div>
            <div className="px-3">
                <p>Github:</p><a href="https://github.com/izveigor/tasks">https://github.com/izveigor/tasks</a>
                <p>Author: Igor Izvekov</p>
                <p>Email: izveigor@gmail.com</p>
                <p>License: MIT</p>
            </div>
        </div>
    );
};