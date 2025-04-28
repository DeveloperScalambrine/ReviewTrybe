const compareTrue = (valueOne, valueTwo) => {
    if (valueOne && valueTwo == true) {
        return true
    } if (valueOne && valueTwo == false) {
        return false
    } if (valueOne || valueTwo == false) {
        return false
    }
}

console.log(compareTrue(false, false));
