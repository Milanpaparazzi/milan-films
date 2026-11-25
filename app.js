(function () {
  const qs = new URLSearchParams(window.location.search);
  const requestedSlug = qs.get("w") || window.location.hash.replace(/^#/, "");

  const el = (id) => document.getElementById(id);

  function showToast(msg) {
    const toast = el("toast");
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(window.__toastTimer);
    window.__toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
  }

  async function sharePage(title) {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title, url });
        return;
      } catch (e) {
        if (e.name === "AbortError") return;
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      showToast("Посилання скопійовано");
    } catch {
      showToast("Скопіюйте посилання з адресного рядка");
    }
  }

  function renderPlayer(videoId) {
    const frame = el("player-frame");
    if (!videoId) {
      frame.innerHTML = `
        <div class="player-placeholder">
          <strong>Відео обробляється на YouTube</strong>
          <span>Одразу після завершення завантаження плеєр з'явиться тут автоматично.</span>
        </div>
      `;
      return;
    }
    frame.innerHTML = `
      <iframe
        src="https://www.youtube.com/embed/${encodeURIComponent(videoId)}?rel=0&modestbranding=1&playsinline=1"
        title="Весільний фільм"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
      ></iframe>
    `;
  }

  fetch("weddings.json")
    .then((r) => r.json())
    .then((data) => {
      const brand = data.brand || {};
      const weddings = data.weddings || [];
      const wedding =
        weddings.find((w) => w.slug === requestedSlug) || weddings[0];

      if (!wedding) return;

      document.title = `${wedding.couple} — ${brand.name || "Wedding Film"}`;

      el("hero-title").textContent = wedding.couple;
      el("hero-subtitle").textContent = wedding.subtitle;
      if (wedding.coverImage) {
        el("hero-cover").src = wedding.coverImage;
      }
      el("wedding-note").textContent = wedding.note || "";
      el("drive-size").textContent = wedding.driveFileSize || "MP4 4K";
      el("wedding-date").textContent = wedding.date || "";
      el("wedding-location").textContent = wedding.location || "4K Ultra HD";
      el("drive-download-btn").href = wedding.driveDownloadUrl || "#";
      const driveClipBtn = el("drive-clip-btn");
      if (driveClipBtn) {
        if (wedding.driveClipUrl) {
          driveClipBtn.href = wedding.driveClipUrl;
          driveClipBtn.hidden = false;
        } else {
          driveClipBtn.hidden = true;
        }
      }

      // Brand block
      el("brand-wordmark").textContent = brand.name || "MILAN NECHESANOV";
      el("brand-name").textContent = brand.name || "MILAN NECHESANOV";
      el("brand-tagline").textContent = brand.tagline || "Wedding Cinematography";
      el("brand-bio").textContent = brand.bio || "";
      el("footer-brand").textContent = brand.name || "MILAN NECHESANOV";
      el("brand-instagram").href = brand.instagram || "#";
      el("brand-telegram").href = brand.telegram || "#";
      const waBtn = el("brand-whatsapp");
      if (waBtn) {
        if (brand.whatsapp) {
          waBtn.href = brand.whatsapp;
        } else {
          waBtn.hidden = true;
        }
      }

      // Player tabs (Clip first by default, then Full Film)
      const tabs = document.querySelectorAll(".tab-btn");
      const switchToFullBtn = el("switch-to-full-btn");

      function selectVideoTab(mode) {
        tabs.forEach((b) => {
          const isMatch = b.getAttribute("data-video") === mode;
          b.classList.toggle("active", isMatch);
          b.setAttribute("aria-selected", isMatch ? "true" : "false");
        });
        if (switchToFullBtn) {
          switchToFullBtn.hidden = mode === "full";
        }
        renderPlayer(
          mode === "clip" ? wedding.youtubeClipId : wedding.youtubeFullId
        );
      }

      const initialMode = wedding.youtubeClipId || !wedding.youtubeFullId ? "clip" : "full";
      selectVideoTab(initialMode);

      tabs.forEach((btn) => {
        btn.addEventListener("click", () => {
          selectVideoTab(btn.getAttribute("data-video"));
        });
      });

      if (switchToFullBtn) {
        switchToFullBtn.addEventListener("click", () => {
          selectVideoTab("full");
        });
      }

      // Share buttons
      el("nav-share-btn").addEventListener("click", () =>
        sharePage(wedding.couple)
      );
      el("card-share-btn").addEventListener("click", () =>
        sharePage(wedding.couple)
      );
    })
    .catch(() => {
      renderPlayer("");
    });
})();
