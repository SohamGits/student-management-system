(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const COLORS = { student: "#0d6efd", teacher: "#212529" };

  document.querySelectorAll(".role-toggle").forEach((toggle) => {
    const thumb = toggle.querySelector(".role-toggle-thumb");
    const inputs = toggle.querySelectorAll(".role-toggle-input");

    // Move the pill to the given role (animate=false snaps instantly)
    const moveThumb = (role, animate) => {
      const x = role === "teacher" ? 100 : 0;
      if (!window.gsap) {            // fallback if GSAP failed to load
        thumb.style.transform = `translateX(${x}%)`;
        thumb.style.backgroundColor = COLORS[role];
        return;
      }
      gsap.to(thumb, {
        xPercent: x,
        backgroundColor: COLORS[role],
        duration: animate && !reduce ? 0.45 : 0,
        ease: "back.out(1.5)",
        overwrite: true,
      });
    };

    const sync = () => {
      const checked = toggle.querySelector(".role-toggle-input:checked");
      moveThumb(checked ? checked.value : "student", false);
    };

    inputs.forEach((input) => {
      input.addEventListener("change", () => {
        moveThumb(input.value, true);
        const label = toggle.querySelector(`label[for="${input.id}"]`);
        if (window.gsap && label && !reduce) {
          gsap.fromTo(label, { scale: 0.92 },
            { scale: 1, duration: 0.4, ease: "back.out(3)" });
        }
      });
    });

    sync();                                   // initial position
    window.addEventListener("pageshow", sync); // browser back/forward restores form state
  });
})();