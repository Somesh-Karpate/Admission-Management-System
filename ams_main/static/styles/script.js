const form = document.querySelector("form"),
    nxtbtn = form.querySelector(".nxtbtn"),
    backbtn = form.querySelector(".backbtn"),
    allInput = form.querySelectorAll(".first input");

nxtbtn.addEventListener("click", () => {
    allInput.forEach(input => {
        if (input.value != "") {
            form.classList.add('secActive');
        } else {
            form.classList.remove('secActive');
        }

    })
})
backbtn.addEventListener("click", () => form.classList.remove('secActive'));