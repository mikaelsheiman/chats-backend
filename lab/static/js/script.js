function openForm() {
    form = document.querySelector('.newchat-form').classList.toggle('hidden')
}

ofbtn = document.getElementById('open-form-button')

ofbtn.addEventListener("click", openForm)