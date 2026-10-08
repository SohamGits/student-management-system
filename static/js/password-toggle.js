document.querySelectorAll(".password-toggle").forEach(function (button) {
    button.addEventListener("click", function () {
        const input = document.getElementById(button.dataset.target);
        const isHidden = input.type === "password";

        input.type = isHidden ? "text" : "password";

        button.querySelector(".icon-show").classList.toggle("d-none", isHidden);
        button.querySelector(".icon-hide").classList.toggle("d-none", !isHidden);

        button.setAttribute(
            "aria-label",
            isHidden ? "Hide password" : "Show password"
        );
    });
});