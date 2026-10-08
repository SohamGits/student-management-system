$(function () {

    const csrfToken = $("input[name='csrfmiddlewaretoken']").first().val();
    const MAX_BYTES = 10 * 1024 * 1024;

    function renderStatus($status, data) {
        $status.empty();

        $("<span>")
            .addClass("badge text-bg-success me-1")
            .text("Submitted")
            .appendTo($status);

        if (data.late) {
            $("<span>")
                .addClass("badge text-bg-danger me-1")
                .text("Late")
                .appendTo($status);
        }

        $("<a>")
            .attr("href", data.download_url)
            .text(data.file_name)
            .appendTo($status);

        $("<div>")
            .addClass("text-muted")
            .text(data.submitted_at)
            .appendTo($status);
    }

    $(".btn-submit").on("click", function () {
        $(this)
            .closest(".submission-area")
            .find(".submission-input")
            .trigger("click");
    });

    $(".submission-input").on("change", function () {
        const $input = $(this);
        const $area = $input.closest(".submission-area");
        const $button = $area.find(".btn-submit");
        const $status = $area.find(".submission-status");
        const $error = $area.find(".submission-error");
        const file = this.files[0];

        $error.addClass("d-none").text("");

        if (!file) {
            return;
        }

        if (file.size > MAX_BYTES) {
            $error.text("File must be 10 MB or smaller.").removeClass("d-none");
            $input.val("");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("csrfmiddlewaretoken", csrfToken);

        const originalText = $button.text();
        $button.prop("disabled", true).text("Uploading...");

        $.ajax({
            url: $area.attr("data-url"),
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            dataType: "json"
        })
        .done(function (data) {
            renderStatus($status, data);
            $button.text("Resubmit");
        })
        .fail(function (xhr) {
            const message = xhr.responseJSON && xhr.responseJSON.error
                ? xhr.responseJSON.error
                : "Upload failed. Please try again.";
            $error.text(message).removeClass("d-none");
            $button.text(originalText);
        })
        .always(function () {
            $button.prop("disabled", false);
            $input.val("");
        });
    });

});