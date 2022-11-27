import React from 'react';


export default function(props) {
    return (
        <div className="mb-3">
            <h1 data-testid="form-name" className="text-2xl">{props.name}</h1>
        </div>
    );
};
