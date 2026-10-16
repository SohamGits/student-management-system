// Fills the shared delete-confirmation modal with the assignment that was clicked.
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("delete-assignment-modal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
        const trigger = event.relatedTarget;
        if (!trigger) return;

        modal.querySelector("#delete-assignment-title").textContent =
            trigger.dataset.assignmentTitle;
        modal.querySelector("form").action = trigger.dataset.deleteUrl;
    });
});