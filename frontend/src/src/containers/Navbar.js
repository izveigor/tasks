import React from 'react';
import Avatar from '../components/Navbar/Avatar';
import Bell from '../components/Navbar/Bell';
import Menu from '../components/Navbar/Menu';
import { useSelector } from 'react-redux';


export default function Navbar() {
    const isTeammate = useSelector((state) => state.user.isTeammate);
    const isAdmin = useSelector((state) => state.user.isAdmin);
    const image = useSelector((state) => state.user.image);

    return (
        <nav className="w-100 py-5 bg-gray-800 flex justify-between">
            <div>
                <Menu isTeammate={isTeammate} />
            </div>
            {image && (<div>
                <div className="flex justify-between gap-4">
                    <Bell isTeammate={isTeammate} />
                    <Avatar isAdmin={isAdmin} isTeammate={isTeammate} image={image} />
                </div>
            </div>)}
        </nav>
    );
};