document.addEventListener("DOMContentLoaded", function () {
    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;
    const duration = (seconds) => (reduceMotion ? 0 : seconds);

    document.querySelectorAll("[data-dropdown]").forEach((dropdown) => {
        const toggle = dropdown.querySelector("[data-dropdown-toggle]");
        const body = dropdown.querySelector("[data-dropdown-body]");
        const chevron = dropdown.querySelector(".dd-chevron");

        if (!toggle || !body) return;

        const items = body.querySelectorAll(".list-group-item");
        const gsap = window.gsap;
        let isOpen = false;
        let timeline = null;

        if (gsap) {
            gsap.set(body, { height: 0, autoAlpha: 0 });
        } else {
            body.style.height = "0";
            body.style.visibility = "hidden";
        }

        function openDropdown() {
            isOpen = true;
            toggle.setAttribute("aria-expanded", "true");

            if (!gsap) {
                body.style.height = "auto";
                body.style.visibility = "visible";
                return;
            }

            if (timeline) timeline.kill();
            timeline = gsap.timeline();
            if (chevron) {
                timeline.to(chevron, {
                    rotation: 180,
                    duration: duration(0.35),
                    ease: "power2.out",
                }, 0);
            }
            timeline.to(body, {
                height: "auto",
                autoAlpha: 1,
                duration: duration(0.45),
                ease: "power2.out",
            }, 0);
            if (items.length) {
                timeline.fromTo(items,
                    { y: -12, autoAlpha: 0 },
                    {
                        y: 0,
                        autoAlpha: 1,
                        duration: duration(0.35),
                        stagger: duration(0.06),
                        ease: "power2.out",
                        clearProps: "transform",
                    },
                    duration(0.1)
                );
            }
        }

        function closeDropdown() {
            isOpen = false;
            toggle.setAttribute("aria-expanded", "false");

            if (!gsap) {
                body.style.height = "0";
                body.style.visibility = "hidden";
                return;
            }

            if (timeline) timeline.kill();
            timeline = gsap.timeline();
            if (items.length) {
                timeline.to(items, {
                    autoAlpha: 0,
                    y: -8,
                    duration: duration(0.15),
                    stagger: { each: duration(0.03), from: "end" },
                    ease: "power1.in",
                }, 0);
            }
            if (chevron) {
                timeline.to(chevron, {
                    rotation: 0,
                    duration: duration(0.35),
                    ease: "power2.out",
                }, 0);
            }
            timeline.to(body, {
                height: 0,
                autoAlpha: 0,
                duration: duration(0.35),
                ease: "power2.inOut",
            }, duration(0.1));
        }

        toggle.addEventListener("click", function () {
            if (isOpen) {
                closeDropdown();
            } else {
                openDropdown();
            }
        });

        dropdown.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && isOpen) {
                closeDropdown();
                toggle.focus();
            }
        });
    });
});