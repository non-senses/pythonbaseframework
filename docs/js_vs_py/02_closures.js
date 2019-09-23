"use strict";

class MyClass {
    constructor(){
        this.myAttribute = 'Can not be changed';
    }
    
    expose() {
        console.log(this.myAttribute)
    }
    
}


const instance = new MyClass();
instance.expose()
instance.myAttribute = 'But it was changed'
instance.expose()


const closure = () => {
    let myPrivateVariable = 'It can not be changed'

    const expose = () => {
        console.log(myPrivateVariable);
    }

    return expose;
}

const closureResult = closure()
closureResult()
closureResult.myPrivateVariable = 'But I changed it'
closureResult()

