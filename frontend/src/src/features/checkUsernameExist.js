import { USERS_URL } from "./constants"


export default async function checkUsernameExist(username) {
    const response = await fetch(USERS_URL + "check_username/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
        })
    })
    const usernameData = await response.json()

    return usernameData;
};