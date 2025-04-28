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

const highestCount = (arr) => {
    if (arr.length === 0) {
        return "Array is empty"
    }
    const highest = Math.max(...arr)
    const count = arr.filter(num => num === highest).length

    return {
        highestNumber: highest,
        frequency: count
    }
}

const catAndMouse = (cat1, cat2, mouse) => {
  // let positionCat1 = Math.abs(cat1 - mouse);
  // let positionCat2 = Math.abs(cat2 - mouse);

  // if (positionCat1 < positionCat2) {
  //   return 'cat1';
  // }

  // if (positionCat2 < positionCat1) {
  //   return 'cat2';
  // }
  // return 'os gatos trombam e o rato foge.';
  cat1 -= mouse;
  cat2 -= mouse;
  if (Math.abs(cat1) === Math.abs(cat2)) {
    return 'Os gatos trombam e o rato foge';
  }

  return Math.abs(cat1) < Math.abs(cat2) ? 'cat1' : 'cat2';
}


    