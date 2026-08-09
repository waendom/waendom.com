// Waendom.com — main script
// 1) overlay menu
// 2) scroll state: wordmark bar collapses, shadows drift, back-to-top appears
// 3) the two gentlemen glide apart, shrink and fade
// 4) lightbox: any piece opens at full size, in its own album
// 5) right-click and image dragging are blocked

document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;

  /* ---------------------------------------------------- overlay menu ---- */
  const toggle = document.querySelector(".menu-toggle");
  const overlay = document.querySelector(".menu-overlay");

  const closeMenu = () => {
    document.body.classList.remove("menu-open");
    toggle && toggle.setAttribute("aria-expanded", "false");
  };

  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }
  if (overlay) {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) closeMenu();
    });
    overlay.querySelectorAll("a").forEach((l) => l.addEventListener("click", closeMenu));
  }

  /* --------------------------------------------- wordmark / back button --
     At rest the bar reads "waendom.com" and links to the start page. Once
     the page is scrolled it collapses to an arrow. Where that arrow leads is
     fixed per page (an album goes up to the gallery, the gallery goes up to
     home) via the data-up attribute set at build time — never browser
     history, so it behaves the same whether you arrived from a link, a
     bookmark, or from outside the site entirely. */
  const bar = document.querySelector(".wordmark-bar");

  if (bar) {
    const homeHref = bar.getAttribute("href");
    const upHref = bar.dataset.up || null;

    bar.addEventListener("click", (e) => {
      if (!document.body.classList.contains("is-scrolled")) return; // plain link home
      e.preventDefault();
      if (upHref) {
        window.location.href = upHref;
      } else {
        // already at the top of the hierarchy (home) — just scroll up
        window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
      }
    });
  }

  /* ------------------------------------------ discourage image grabbing --
     A deterrent, not protection — anything on screen can still be captured. */
  document.addEventListener("contextmenu", (e) => e.preventDefault());
  document.addEventListener("dragstart", (e) => {
    if (e.target.tagName === "IMG") e.preventDefault();
  });

  /* ---------------------------------------------------- scroll effects ---
     The figures drift outwards and shrink at the same time. Their
     transform-origin sits at the bottom centre, so the inward shrink cancels
     the outward drift at the edges — neither man is ever clipped. */
  const hero = document.querySelector(".hero");
  const heroMedia = document.querySelector(".hero-media");
  const figLeft = document.querySelector(".figure-left");
  const figRight = document.querySelector(".figure-right");
  const toTop = document.querySelector(".to-top");

  /* The back-to-top button only makes sense near the foot of the page, so it
     appears once the remaining scroll distance drops below roughly three
     quarters of a screen — and never on pages too short to scroll properly. */
  const nearPageEnd = () => {
    const docHeight = Math.max(
      document.body.scrollHeight,
      document.documentElement.scrollHeight
    );
    const scrollable = docHeight - window.innerHeight;
    if (scrollable < window.innerHeight * 0.6) return false; // barely scrolls
    const remaining = scrollable - window.scrollY;
    return remaining < window.innerHeight * 0.75;
  };

  const DRIFT = 18;    // % of each figure's own width
  const SHRINK = 0.38; // scale runs from 1 down to 1 - SHRINK

  let ticking = false;

  const onScroll = () => {
    ticking = false;
    const y = window.scrollY;

    // wordmark bar collapses into a back arrow
    const scrolled = y > 40;
    document.body.classList.toggle("is-scrolled", scrolled);
    if (bar) bar.setAttribute("aria-label", scrolled ? "Zurück" : "Zur Startseite");

    // back-to-top fades in as the foot of the page comes within reach
    if (toTop) toTop.classList.toggle("is-visible", nearPageEnd());

    // the drop shadow swings a little as the page moves
    const doc = Math.max(document.body.scrollHeight - window.innerHeight, 1);
    const q = Math.min(Math.max(y / doc, 0), 1);
    root.style.setProperty("--sx", (-9 + 18 * q).toFixed(1) + "px");
    root.style.setProperty("--sy", (9 + 13 * q).toFixed(1) + "px");
    root.style.setProperty("--sblur", (22 + 14 * q).toFixed(1) + "px");

    // the banner
    if (hero && heroMedia && !reduceMotion) {
      const p = Math.min(Math.max(y / hero.offsetHeight, 0), 1);
      heroMedia.style.opacity = String(1 - p);
      const scale = 1 - SHRINK * p;
      if (figLeft)
        figLeft.style.transform = "translateX(" + -DRIFT * p + "%) scale(" + scale + ")";
      if (figRight)
        figRight.style.transform = "translateX(" + DRIFT * p + "%) scale(" + scale + ")";
    }
  };

  window.addEventListener("scroll", () => {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* --------------------------------------------------------- lightbox ----
     Each grid is its own set, so the arrows stay inside the album you opened. */
  const groups = Array.from(document.querySelectorAll(".gallery, .highlights-grid"))
    .map((grid) => Array.from(grid.querySelectorAll(".art-piece")))
    .filter((g) => g.length);

  if (groups.length) {
    const box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Bildansicht");
    box.innerHTML = `
      <button class="lightbox-close" aria-label="Schließen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
      <button class="lightbox-prev" aria-label="Vorheriges Bild">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M15 5l-7 7 7 7"/></svg>
      </button>
      <button class="lightbox-next" aria-label="Nächstes Bild">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M9 5l7 7-7 7"/></svg>
      </button>
      <img alt="">
      <span class="lightbox-counter"></span>`;
    document.body.appendChild(box);

    const lbImg = box.querySelector("img");
    const lbCounter = box.querySelector(".lightbox-counter");
    const btnPrev = box.querySelector(".lightbox-prev");
    const btnNext = box.querySelector(".lightbox-next");
    const btnClose = box.querySelector(".lightbox-close");

    let group = groups[0];
    let index = 0;
    let lastFocus = null;

    const show = (i) => {
      index = (i + group.length) % group.length;
      const img = group[index].querySelector("img");

      // Show the grid image straight away so there is never an empty frame,
      // then swap in the high-resolution file once it has finished loading.
      const thumb = img.currentSrc || img.src;
      const full = img.dataset.full;
      lbImg.src = thumb;
      lbImg.alt = img.alt || "";
      box.classList.add("is-loading");

      if (full) {
        const hi = new Image();
        const wanted = index;
        hi.onload = () => {
          if (wanted === index) {          // still the same picture?
            lbImg.src = full;
            box.classList.remove("is-loading");
          }
        };
        hi.onerror = () => box.classList.remove("is-loading");
        hi.src = full;
      } else {
        box.classList.remove("is-loading");
      }
      const single = group.length < 2;
      lbCounter.textContent = single ? "" : index + 1 + " / " + group.length;
      btnPrev.hidden = single;
      btnNext.hidden = single;
    };

    const open = (g, i) => {
      lastFocus = document.activeElement;
      group = g;
      show(i);
      box.classList.add("is-open");
      document.body.classList.add("lightbox-open");
      btnClose.focus();
    };

    const close = () => {
      box.classList.remove("is-open");
      document.body.classList.remove("lightbox-open");
      lastFocus && lastFocus.focus();
    };

    groups.forEach((g) => {
      g.forEach((fig, i) => {
        fig.setAttribute("tabindex", "0");
        fig.setAttribute("role", "button");
        fig.addEventListener("click", () => open(g, i));
        fig.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(g, i); }
        });
      });
    });

    btnClose.addEventListener("click", close);
    btnPrev.addEventListener("click", () => show(index - 1));
    btnNext.addEventListener("click", () => show(index + 1));
    box.addEventListener("click", (e) => { if (e.target === box) close(); });

    document.addEventListener("keydown", (e) => {
      if (document.body.classList.contains("menu-open") && e.key === "Escape") {
        closeMenu();
        return;
      }
      if (!box.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });

    let startX = null;
    box.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener("touchend", (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
      startX = null;
    }, { passive: true });
  } else {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ------------------------------------------- fade pieces in on scroll -- */
  const pieces = document.querySelectorAll(".art-piece");
  if ("IntersectionObserver" in window && pieces.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("in-view"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    pieces.forEach((p) => io.observe(p));
  } else {
    pieces.forEach((p) => p.classList.add("in-view"));
  }
});
