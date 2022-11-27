export default function isRightPassword(password) {
    const numberRegex = new RegExp("[0-9]");
    const lowerRegex = new RegExp("[a-z]");
    const upperRegex = new RegExp("[A-Z]");

    let isUpper = false,
        isLower = false,
        isDigit = false;

    if(password.length < 10) {
        return false;
    }

    for(let i = 0; i < password.length; i ++) {
        if(password[i].match(numberRegex) !== null) {
            isDigit = true;
            continue;
        }

        if(password[i].match(lowerRegex) !== null) {
            isUpper = true;
            continue;
        }

        if(password[i].match(upperRegex) !== null) {
            isLower = true;
            continue;
        }
    }

    if(isUpper && isLower && isDigit) {
        return true;
    } return false;
};