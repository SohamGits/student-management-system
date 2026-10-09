
(function () {
    function initRoleToggles() {
        const reduceMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        document.querySelectorAll(".role-toggle").forEach((toggle) => {
            const thumb = toggle.querySelector(".role-toggle-thumb");
            const inputs = toggle.querySelectorAll(
                ".role-toggle-input"
            );

            if (!thumb || !inputs.length) return;

            function moveThumb(role, animate = true) {
                const teacherSelected = role === "teacher";
                const xPercent = teacherSelected ? 100 : 0;
                const color = teacherSelected ? "#212529" : "#0d6efd";

                if (window.gsap) {
                    gsap.to(thumb, {
                        xPercent,
                        backgroundColor: color,
                        duration: animate && !reduceMotion ? 0.4 : 0,
                        ease: "power3.out",
                        overwrite: true
                    });
                } else {
                    thumb.style.transform =
                        `translateX(${xPercent}%)`;
                    thumb.style.backgroundColor = color;
                }
            }

            function sync() {
                const selected = toggle.querySelector(
                    ".role-toggle-input:checked"
                );

                moveThumb(selected ? selected.value : "student", false);
            }

            inputs.forEach((input) => {
                input.addEventListener("change", () => {
                    moveThumb(input.value, true);
                });
            });

            sync();

            window.addEventListener("pageshow", sync);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initRoleToggles
        );
    } else {
        initRoleToggles();
    }
})();
