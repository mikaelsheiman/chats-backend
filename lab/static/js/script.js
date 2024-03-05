function openForm() {
    form = document.getElementById('newchat-form').classList.toggle('hidden')
}

ofbtn = document.getElementById('open-form-button')

ofbtn.addEventListener("click", openForm)


function openMessageForm() {
    form = document.getElementById('newmessage-form').classList.toggle('hidden')

    // const choices = document.querySelectorAll(.message_choices)

    ofmbtn.innerHTML = "+message (" + Array.from(document.querySelectorAll(".message_choices")).filter(x => x.checked).length + ")"

}

ofmbtn = document.getElementById('open-form-message-button')

ofmbtn.addEventListener("click", openMessageForm)

