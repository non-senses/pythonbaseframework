const Math2 = require('./libs/math'); // Overwrites the standard Math module
console.log(Math.random())


const addNameToList = (nameToAdd, list=[]) => {
    list.push(nameToAdd);
    return list;
}

console.log(addNameToList('First Name'))
console.log(addNameToList('Second Name'))

/**
 * Function parameters are evaluated at every single function invocation
 */