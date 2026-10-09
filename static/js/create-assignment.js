(function () {
  const btn = document.getElementById("create-toggle");
  const panel = document.getElementById("create-panel");
  if (!btn || !panel) return;

  const icon = btn.querySelector(".create-toggle-icon");
  let open = false;

  // Fallback: if GSAP failed to load, show/hide without animation
  if (!window.gsap) {
    btn.addEventListener("click", () => {
      open = !open;
      panel.style.cssText = open
        ? "height:auto;opacity:1;visibility:visible;overflow:visible"
        : "";
      btn.setAttribute("aria-expanded", open);
    });
    return;
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items = panel.querySelectorAll("h2, form > :not(input)");

  // One timeline: play() opens, reverse() closes (handles fast double-clicks too)
  const tl = gsap.timeline({
    paused: true,
    defaults: { ease: "power3.out" },
    onComplete: () => {
      panel.style.overflow = "visible";   // so focus rings/shadows aren't clipped
      const first = panel.querySelector("input:not([type=hidden]), textarea");
      if (first) first.focus({ preventScroll: true });
    },
  });

  tl.to(panel, { height: "auto", autoAlpha: 1, duration: 0.5 })
    .from(items, { y: 16, autoAlpha: 0, duration: 0.35, stagger: 0.06 }, "-=0.25");

  if (reduce) tl.timeScale(50);

  btn.addEventListener("click", () => {
    open = !open;
    btn.setAttribute("aria-expanded", open);
    gsap.to(icon, { rotation: open ? 45 : 0, duration: 0.3, ease: "back.out(2)" });
    panel.style.overflow = "hidden";      // needed while the height is animating
    open ? tl.play() : tl.reverse();
  });
})();