$(function () {

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;
    const t = (seconds) => (reduceMotion ? 0 : seconds);

    $("[data-dropdown]").each(function () {
        const $dropdown = $(this);
        const $toggle = $dropdown.find("[data-dropdown-toggle]");
        const $body = $dropdown.find("[data-dropdown-body]");
        const body = $body[0];
        const chevron = $dropdown.find(".dd-chevron")[0];
        const items = $body.find(".list-group-item").toArray();

        let isOpen = false;
        let timeline = null;

        // If GSAP didn't load, fall back to a plain jQuery slide
        if (!window.gsap) {
            $body.css({ height: "auto", visibility: "visible" }).hide();
            $toggle.on("click", function () {
                isOpen = !isOpen;
                $toggle.attr("aria-expanded", String(isOpen));
                $body.slideToggle(200);
            });
            return;
        }

        gsap.set(body, { height: 0, autoAlpha: 0 });

        function openDropdown() {
            isOpen = true;
            $toggle.attr("aria-expanded", "true");
            if (timeline) timeline.kill();

            timeline = gsap.timeline();
            timeline
                .to(chevron, {
                    rotation: 180, duration: t(0.35), ease: "power2.out"
                }, 0)
                .to(body, {
                    height: "auto", autoAlpha: 1,
                    duration: t(0.45), ease: "power2.out"
                }, 0)
                .fromTo(items,
                    { y: -12, autoAlpha: 0 },
                    {
                        y: 0, autoAlpha: 1, duration: t(0.35),
                        stagger: t(0.06), ease: "power2.out",
                        clearProps: "transform"
                    },
                    t(0.1)
                );
        }

        function closeDropdown() {
            isOpen = false;
            $toggle.attr("aria-expanded", "false");
            if (timeline) timeline.kill();

            timeline = gsap.timeline();
            timeline
                .to(items, {
                    autoAlpha: 0, y: -8, duration: t(0.15),
                    stagger: { each: t(0.03), from: "end" },
                    ease: "power1.in"
                }, 0)
                .to(chevron, {
                    rotation: 0, duration: t(0.35), ease: "power2.out"
                }, 0)
                .to(body, {
                    height: 0, autoAlpha: 0,
                    duration: t(0.35), ease: "power2.inOut"
                }, t(0.1));
        }

        $toggle.on("click", function () {
            if (isOpen) {
                closeDropdown();
            } else {
                openDropdown();
            }
        });

        $dropdown.on("keydown", function (event) {
            if (event.key === "Escape" && isOpen) {
                closeDropdown();
                $toggle.trigger("focus");
            }
        });
    });

});