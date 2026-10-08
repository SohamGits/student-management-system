(function () {
  const root = document.documentElement;
  const reveal = () => root.classList.remove("gsap-pending");

  // If GSAP failed to load, just show the page normally
  if (!window.gsap || !window.ScrollTrigger) {
    reveal();
    return;
  }
  gsap.registerPlugin(ScrollTrigger);

  // Reusable "no" shake: shake(".card") or shake(element)
  window.shake = (target) =>
    gsap.to(target, {
      keyframes: { x: [-8, 8, -5, 5, 0], easeEach: "power1.inOut" },
      duration: 0.4,
      clearProps: "transform",
    });

  // Skip all motion for users who've asked their OS to reduce it
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    const done = "transform,opacity,visibility";

    // 1. Navbar slides down (only exists when logged in)
    if (document.querySelector(".navbar")) {
      tl.from(".navbar", { y: -60, autoAlpha: 0, duration: 0.6, clearProps: done }, 0);
    }

    // 2. Dashboard header ("Student Dashboard" + welcome line)
    const h1 = document.querySelector("h1");
    if (h1 && !h1.closest(".card")) {
      tl.from(h1.parentElement.children, {
        y: 20, autoAlpha: 0, duration: 0.5, stagger: 0.1, clearProps: done,
      }, 0.15);
    }

    // 3. Cards rise in (login box, dashboard cards)
    if (document.querySelector(".card")) {
      tl.from(".card", {
        y: 40, autoAlpha: 0, duration: 0.7, stagger: 0.12, clearProps: done,
      }, 0.3);
    }

    // 4. Login/register/forgot-password: fields cascade in after the card
    const authItems = gsap.utils.toArray(
      ".auth-wrapper .card-body > .text-center, .auth-wrapper form > :not(input)"
    );
    if (authItems.length) {
      tl.from(authItems, {
        y: 15, autoAlpha: 0, duration: 0.45, stagger: 0.08, clearProps: done,
      }, 0.55);
    }

    // 5. Wrong password? Shake the login card
    if (document.querySelector(".auth-wrapper .alert-danger")) {
      tl.to(".auth-wrapper .card", {
        keyframes: { x: [-10, 10, -6, 6, 0], easeEach: "power1.inOut" },
        duration: 0.4,
        clearProps: "transform",
      }, 1.2);
    }

    // 6. Django flash messages drop in (slide only: Bootstrap's .fade owns opacity)
    if (document.querySelector(".alert-dismissible")) {
      gsap.from(".alert-dismissible", {
        y: -20, duration: 0.5, ease: "back.out(1.7)",
        stagger: 0.1, delay: 0.2, clearProps: "transform",
      });
    }

    // 7. List items (students, assignments) reveal as they scroll into view
    const items = gsap.utils.toArray(".list-group-item");
    if (items.length) {
      gsap.set(items, { autoAlpha: 0, y: 20 });
      ScrollTrigger.batch(items, {
        start: "top 95%",
        once: true,
        onEnter: (batch) =>
          gsap.to(batch, {
            autoAlpha: 1, y: 0, duration: 0.5, stagger: 0.07,
            ease: "power2.out", clearProps: done,
            delay: tl.isActive() ? 0.6 : 0,   // wait for the cards on first load
          }),
      });
    }

    // 8. Count-up for the numeric badges in card headers (e.g. assignment count)
    gsap.utils.toArray(".card-header .badge").forEach((badge) => {
      const text = badge.textContent.trim();
      if (!/^\d+$/.test(text) || text === "0") return;
      const target = parseInt(text, 10);
      const counter = { val: 0 };
      badge.textContent = "0";
      gsap.to(counter, {
        val: target, duration: 1, delay: 0.8, ease: "power1.out",
        onUpdate: () => (badge.textContent = Math.round(counter.val)),
        onComplete: () => (badge.textContent = target),
      });
    });

    // 9. Button hover lift / press (skips input-group buttons so they stay aligned)
    gsap.utils.toArray(".btn").forEach((btn) => {
      if (btn.closest(".input-group")) return;
      btn.addEventListener("pointerenter", () =>
        gsap.to(btn, { y: -2, duration: 0.2, ease: "power2.out" }));
      btn.addEventListener("pointerleave", () =>
        gsap.to(btn, { y: 0, scale: 1, duration: 0.2, ease: "power2.out" }));
      btn.addEventListener("pointerdown", () =>
        gsap.to(btn, { scale: 0.97, duration: 0.1 }));
      btn.addEventListener("pointerup", () =>
        gsap.to(btn, { scale: 1, duration: 0.1 }));
    });
  });

  // Starting states are now applied, so it's safe to un-hide the page
  reveal();
})();