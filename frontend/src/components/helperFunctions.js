import { Store } from "react-notifications-component";

export function DisplayNameSetup(name, readLength){   
    if(name.length > readLength){
        return `${name.substring(0,readLength)}...`
    }else{
        return name;
    }
}

export function upperCaseValidation(checkString, printNoti=true, messageConcat=" NAME DID NOT SAVE"){
    const upperRegex = /^(?!UC_)(?!.*__)(?!.*[^A-Za-z'_0-9])(?!.*_$)[A-Z][A-Za-z'_0-9]*/
    // ^(?!UC_) Does not start with UC_
    // (?!.*__) does not have a double __
    // (?!.*[^A-Za-z'_0-9]) does not allow non-alphanumeric characters except ' and _
    // (?!.*_$) does not end with a _
    // [A-Z] First character is a Capital and must be there
    // [A-Za-z'_0-9]* Usable characters in the string can have 0 to many
    if(checkString === "" || checkString === null){
        return true
    }
    let notiTitle = checkString.concat(" Name Check Failure")
    let notiMessage = "Message: "
    let notiType = 'danger'
    let theCheck = upperRegex.test(checkString)
    if(reservedWordCheck(checkString)){
        theCheck = false
    }
    if(theCheck){
        return theCheck
        
    }  else {
        if(printNoti){
            notiMessage = upperCaseInvalidMessage(checkString)
            notiMessage = notiMessage.concat(messageConcat)
            
            let notification = {
                title:   notiTitle,
                message: notiMessage,
                type:    notiType,
                insert:  "top",
                container: "top-right",
                animationIn: ["animate__animated", "animate__fadeIn"],
                animationOut: ["animate__animated", "animate__fadeOut"],
                dismiss: {
                    duration: 10000,
                    onScreen: true
                }
            }
            Store.addNotification(notification)
        }
       return theCheck
    }
    

}

export function lowerCaseValidation(checkString, printNoti=true){
    const lowerRegex = /^(?!uc_)(?!.*__)(?!.*[^A-Za-z'_0-9])(?!.*_$)[a-z][A-Za-z'_0-9]*/
    // ^(?!uc_) Does not start with uc_
    // (?!.*__) does not have a double __
    // (?!.*[^A-Za-z'_0-9]) does not allow non-alphanumeric characters except ' and _
    // (?!.*_$) does not end with a _
    // [a-z] First character is a lowercase letter
    // [A-Za-z'_0-9]* Usable characters in the string can have 0 to many
    if(checkString === "" || checkString === null){
        return true
    }
    let notiTitle = checkString.concat(" Name Check Failure")
    let notiMessage = "Message: "
    let notiType = 'danger'
    let theCheck = lowerRegex.test(checkString)
    if(reservedWordCheck(checkString)){
        theCheck = false
    }
    if(theCheck){
        return theCheck
        
    }  else {
        if(printNoti){
            notiMessage = lowerCaseInvalidMessage(checkString)
            notiMessage = notiMessage + " Name did not Save"
            let notification = {
                title:   notiTitle,
                message: notiMessage,
                type:    notiType,
                insert:  "top",
                container: "top-right",
                animationIn: ["animate__animated", "animate__fadeIn"],
                animationOut: ["animate__animated", "animate__fadeOut"],
                dismiss: {
                    duration: 10000,
                    onScreen: true
                }
            }
            Store.addNotification(notification)
        }
        
       return theCheck
    }
}
export function commentValidation(checkString, printNoti=true, messageConcat=" COMMENT DID NOT SAVE"){
    if(checkString === "" || checkString === null){
        return true
    }
    let notiTitle = checkString.concat(" Comment Check Failure")
    let notiMessage = "Message: "
    let notiType = 'danger'
    let theCheck = false
    if (!checkString.includes('*)') && !checkString.includes('(*')){theCheck = true}
    if(theCheck){
        return theCheck
        
    }  else {
        if(printNoti){
            notiMessage += "Comment cannot have (* or *) with no white space between the characters."
            notiMessage = notiMessage.concat(messageConcat)
            
            let notification = {
                title:   notiTitle,
                message: notiMessage,
                type:    notiType,
                insert:  "top",
                container: "top-right",
                animationIn: ["animate__animated", "animate__fadeIn"],
                animationOut: ["animate__animated", "animate__fadeOut"],
                dismiss: {
                    duration: 10000,
                    onScreen: true
                }
            }
            Store.addNotification(notification)
        }
       return theCheck
    }
    

}
export function upperCaseInvalidMessage(checkString){
    let notiMessage = "Message: "
    const regexCheckUCLead = /^(?!UC_)/
        if(!regexCheckUCLead.test(checkString)){
            notiMessage = notiMessage.concat(" Cannot start the name of this entity with UC_\n")
        }
        const regexCheckUpperLead = /^[A-Z]/
        if(!regexCheckUpperLead.test(checkString)){
            notiMessage = notiMessage.concat(
                " Name of this entity must start with an uppercase letter\n")
        }
        const regexDoubleUnderScore = /__/
        if(regexDoubleUnderScore.test(checkString)){
            notiMessage = notiMessage.concat(" Name cannot contain 2 consecutive underscores '__'\n")
        }
        const regexContains = /[^A-Za-z'_0-9]/
        if(regexContains.test(checkString)){
            notiMessage = notiMessage.concat(
                " Name cannot contain non-alpha numeric characters except for ' and _\n")
        }
        const regexUnderScoreEnd = /_$/
        if(regexUnderScoreEnd.test(checkString)){
            notiMessage = notiMessage.concat(" Name cannot end in an _\n")
        }
        if(reservedWordCheck(checkString)){
            notiMessage = notiMessage.concat(" Name cannot be a reserved word")
        }
        return notiMessage
}
export function lowerCaseInvalidMessage(checkString){
    let notiMessage = "Message: "
    const regexCheckUCLead = /^(?!uc_)/
    if(!regexCheckUCLead.test(checkString)){
        notiMessage = notiMessage.concat(" Cannot start the name of this entity with uc_\n")
    }
    const regexCheckLowerLead = /^[a-z]/
    if(!regexCheckLowerLead.test(checkString)){
        notiMessage = notiMessage.concat(
            " Name of this entity must start with an lowercase letter\n")
    }
    const regexDoubleUnderScore = /__/
    if(regexDoubleUnderScore.test(checkString)){
        notiMessage = notiMessage.concat(" Name cannot contain 2 consecutive underscores '__'\n")
    }
    const regexContains = /[^A-Za-z'_0-9]/
    if(regexContains.test(checkString)){
        notiMessage = notiMessage.concat(
            " Name cannot contain non-alpha numeric characters except for ' and _\n")
    }
    const regexUnderScoreEnd = /_$/
    if(regexUnderScoreEnd.test(checkString)){
        notiMessage = notiMessage.concat(" Name cannot end in an _\n")
    }
    if(reservedWordCheck(checkString)){
        notiMessage = notiMessage.concat(" Name cannot be a reserved word")
    }
    return notiMessage
}

const reservedWordList = ['adversarial', 'and', 'direct', 'ec_requires', 'elif', 
    'else', 'end', 'envport', 'fail', 'functionality', 'if', 'implements', 'in', 'initial',
    'intport', 'match', 'message', 'out', 'party', 'send', 'serves', 'simulates', 'simulator',
    'state', 'subfun', 'transition', 'uc_requires', 'uses', 'var', 'with', // End of EasyUC list
    'Pr', 'Top', 'abbrev', 'abstract', 'admit', 'algebra', 'alias', 'apply', 'as', 'assert', 
    'assumption', 'auto', 'axiom', 'axiomatized', 'beta', 'by', 'byequiv', 'byphoare', 
    'bypr', 'call', 'case', 'cbv', 'cfold', 'change', 'class', 'clear', 'clone', 'congr',
    'conseq', 'const', 'cut', 'debug', 'declare', 'delta', 'do', 'done', 'eager', 'elim',
    'equiv', 'eta', 'exact', 'exfalso', 'exists', 'export', 'fel', 'fission', 'for', 'forall',
    'fun', 'fusion', 'glob', 'goal', 'have', 'hint', 'hoare', 'idtac', 'import', 'include', 
    'inductive', 'inline', 'instance', 'iota', 'is', 'islossless', 'kill', 'lemma', 'let', 
    'local', 'logic', 'modpath', 'module', 'move', 'nosmt', 'notation', 'of', 'op', 'phoare', 
    'pose', 'pr', 'pragma', 'pred', 'print', 'proc', 'progress', 'proof', 'prover', 'qed', 'rcondf', 
    'rcondt', 'realize', 'reflexivity', 'remove', 'rename', 'replace', 'require', 'res', 'return', 
    'rewrite', 'rnd', 'rwnormal', 'search', 'section', 'seq', 'sim', 'simplify', 'skip', 'smt', 
    'sp', 'split', 'splitwhile', 'subst', 'suff', 'swap', 'symmetry', 'then', 'theory', 'time', 
    'timeout', 'transitivity', 'trivial', 'try', 'type', 'undo', 'unroll', 'while', 'why3', 'wp', 'zeta']

// Returns whether a reserved word is being used
export function reservedWordCheck(checkString){
    let isInvalid = false
    for (let resWord of reservedWordList){
        if (checkString === resWord){
            isInvalid = true
        }
    }
    return isInvalid
}
/*
* splits input string into multiline string, with each line other than 1st starting with *. breaks will be inbetween words
* input=string, limit=int(max length of each line), type=bool(whether its inside or outside a interface)
*/
export function commentBreaker(input, limit, type){
    const maxLength = limit;
    const words = input.split(/\s+/);
    const result = [];

    let currentLine = '';
    if(type === 0){
        for (const word of words) {
        if ((currentLine + ' ' + word).trim().length <= maxLength) {
            currentLine += (currentLine ? ' ' : '') + word;
        } else {
            result.push(currentLine);
            currentLine = word;
        }
    }

    if (currentLine) {
        result.push(currentLine);
    }

    return result.map((line, index) => index === 0 ? line : ` * ${line}`).join('\n');
    }else if(type ===1){ //extra tabs for when comment is inside of interface(ie. basic instances or message comments)
        for (const word of words) {
        if ((currentLine + ' ' + word).trim().length <= maxLength) {
            currentLine += (currentLine ? ' ' : '') + word;
        } else {
            result.push(currentLine);
            currentLine = word;
        }
    }

    if (currentLine) {
        result.push(currentLine);
    }

    return result.map((line, index) => index === 0 ? line :`    * ${line}`).join('\n');
    }else if(type ===2){//different formatting for party comments, also for ideal functionality states
        for (const word of words) {
        if ((currentLine + ' ' + word).trim().length <= maxLength) {
            currentLine += (currentLine ? ' ' : '') + word;
        } else {
            result.push(currentLine);
            currentLine = word;
        }
    }
    if (currentLine) {
        result.push(currentLine);
    }
    return result.map((line, index) => index === 0 ? line :`   * ${line}`).join('\n');
    }else if(type ===3){//different formatting for state comments
        for (const word of words) {
        if ((currentLine + ' ' + word).trim().length <= maxLength) {
            currentLine += (currentLine ? ' ' : '') + word;
        } else {
            result.push(currentLine);
            currentLine = word;
        }
    }
    if (currentLine) {
        result.push(currentLine);
    }
    return result.map((line, index) => index === 0 ? line :`     * ${line}`).join('\n');
    }
}
