import React from 'react';
import ProfileMenu from "./ProfileMenu";
import { useState } from 'react';
import { USERS_URL_WITHOUT_SLASH } from '../../features/constants';


export default function Avatar(props) {
    const [profileMenuState, changeProfileMenuState] = useState(false);

    return (
        <div>
            <div>
                <button onClick={() => {
                    changeProfileMenuState(previousMenuState => !previousMenuState);
                    if(props.onChange) { props.onChange(!profileMenuState); }
                    }} className="align-middle" type="button">
                    <img className="h-8 w-8 rounded-full" src={USERS_URL_WITHOUT_SLASH + props.avatar.image} />
                </button>
            </div>

            {profileMenuState && <ProfileMenu isTeammate={props.isTeammate} isAdmin={props.isAdmin} />}
        </div>
    );
};