$(function () {

    const $form = $("#forgot-form");
    const $error = $("#reset-error");
    const $button = $("#reset-button");

    function showError(message) {
        $error.text(message).removeClass("d-none");
    }

    $form.on("submit", function (event) {
        event.preventDefault();
        $error.addClass("d-none").text("");

        if ($("#new_password").val() !== $("#confirm_password").val()) {
            showError("Passwords do not match.");
            return;
        }

        $button.prop("disabled", true).text("Resetting...");

        $.ajax({
            url: $form.attr("action"),
            method: "POST",
            data: $form.serialize(),
            dataType: "json"
        })
        .done(function (response) {
            window.location.href = response.redirect;
        })
        .fail(function (xhr) {
            const message = xhr.responseJSON && xhr.responseJSON.error
                ? xhr.responseJSON.error
                : "Something went wrong. Please try again.";
            showError(message);
            $button.prop("disabled", false).text("Reset password");
        });
    });

});