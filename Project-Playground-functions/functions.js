const compareTrue = (valueOne, valueTwo) => {
    if (valueOne && valueTwo == true) {
        return true
    } if (valueOne && valueTwo == false) {
        return false
    } if (valueOne || valueTwo == false) {
        return false
    }
}

const calcArea = (base, height) => {
    const triangle = (base * height) / 2;
    return triangle;
}

const splitSentence = (phrase) => {
   const wordWithSplit = phrase.split(' ');
   return wordWithSplit;
}

const concatName = (arr) => {
    if (arr.length === 0) {
        return "Array is empty"
    }
    return {
        last: arr[arr.length - 1],
        first: arr[0]
    }
}

console.log(concatName(['Carlos', 'Henrique']));

    