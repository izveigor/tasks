import React from 'react';


export default function ChangeLoginRegisterButton(props) {
    return (
        <div>
            <button onClick={() => {props.changeForm()}} type="button" className="border-0 text-gray-700 mt-1 hover:text-gray-500">
                {props.name}
            </button>
        </div>
    );
};