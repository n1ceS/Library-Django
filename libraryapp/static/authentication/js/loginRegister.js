const inputs = document.querySelectorAll(".input");
window.onload = checkFields()
function focusFunc() {
    let parent = this.parentNode.parentNode;
    parent.classList.add('focus');
}

function unFocusFunc(){
    let parent = this.parentNode.parentNode;
    if(this.value == ""){
    parent.classList.remove('focus');
    }
}

inputs.forEach(input => {
    input.addEventListener('focus', focusFunc);
    input.addEventListener('blur', unFocusFunc)
})
function checkFields(){
    inputs.forEach(element => {
        let parent = element.parentNode.parentNode;
        console.log(element.value)
        if(element.value !=="" ) {
            parent.classList.add('focus');
        }else {
            parent.classList.remove('focus')
        }
    });
}