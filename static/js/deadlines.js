$(function () {

    function refreshDeadlines() {
        const now = new Date();

        $(".deadline-badge").each(function () {
            const $badge = $(this);
            const deadline = new Date($badge.attr("data-deadline"));
            const label = $badge.attr("data-label");

            if (now > deadline) {
                $badge
                    .removeClass("text-bg-warning")
                    .addClass("text-bg-danger")
                    .text("Overdue · " + label);
            } else {
                $badge
                    .removeClass("text-bg-danger")
                    .addClass("text-bg-warning")
                    .text("Due " + label);
            }
        });
    }

    refreshDeadlines();
    setInterval(refreshDeadlines, 30000);

});