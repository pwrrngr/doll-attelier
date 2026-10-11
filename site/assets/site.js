/* Atelier Alla Mode — interactions. No dependencies. */
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header: light over dark heroes, solid once scrolled */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu */
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("menu-open")) toggle.click();
    });
  }

  /* Scroll reveals */
  var targets = document.querySelectorAll(".reveal, .unveil");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Gentle hero parallax */
  var heroImg = document.querySelector(".hero-media");
  if (heroImg && !reduce) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, window.innerHeight);
        heroImg.style.transform = "translate3d(0," + (y * 0.18).toFixed(1) + "px,0)";
        ticking = false;
      });
    }, { passive: true });
  }

  /* Commission form: compose a prepared email (static site, no server) */
  var form = document.querySelector("[data-enquiry]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var get = function (n) { var f = form.elements[n]; return f ? f.value.trim() : ""; };
      var lines = [
        "Name: " + get("name"),
        "Email: " + get("email"),
        "Country: " + get("country"),
        "",
        "The doll",
        "Maker / mould mark: " + get("maker"),
        "Height: " + get("height"),
        "",
        "The garment",
        "Type: " + get("garment"),
        "Era or mood: " + get("era"),
        "Ideal timing: " + get("timing"),
        "",
        get("message"),
        "",
        "(Photographs attached: front, back and profile.)"
      ];
      var subject = "Commission enquiry" + (get("name") ? " — " + get("name") : "");
      window.location.href = "mailto:" + form.getAttribute("data-enquiry") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      var note = form.querySelector("[data-sent]");
      if (note) note.hidden = false;
    });
  }

  /* Lightbox for portfolio images */
  var zooms = document.querySelectorAll("[data-zoom]");
  if (zooms.length && "HTMLDialogElement" in window) {
    var box = document.createElement("dialog");
    box.className = "lightbox";
    box.innerHTML = '<img alt=""><p></p><button type="button" aria-label="Close">×</button>';
    document.body.appendChild(box);
    var bimg = box.querySelector("img"), bcap = box.querySelector("p");
    zooms.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        var img = a.querySelector("img");
        bimg.src = a.getAttribute("href");
        bimg.alt = img ? img.alt : "";
        bcap.textContent = img ? img.alt : "";
        box.showModal();
      });
    });
    box.addEventListener("click", function () { box.close(); });
  }

  /* Year */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
