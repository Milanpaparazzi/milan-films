#!/usr/bin/env python3
"""
Generates root index.html and per-wedding <slug>/index.html pages
with static Open Graph (og:title, og:description, og:image, og:url) tags
so Instagram, Telegram, WhatsApp, and Viber show the exact cover photo
and details for each specific wedding link.
"""

import html
import json
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent
BASE_URL = "https://milanpaparazzi.github.io/milan-films"

TEMPLATE = """<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>{page_title}</title>
  <meta name="description" content="{og_description}" />
  <meta name="theme-color" content="#FFFFFF" />

  <!-- Open Graph / Instagram / Telegram / WhatsApp Preview -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{brand_name}" />
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{og_description}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:image:width" content="1920" />
  <meta property="og:image:height" content="1080" />
  <meta property="og:url" content="{og_url}" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{og_description}" />
  <meta name="twitter:image" content="{og_image}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{prefix}styles.css" />
</head>
<body>
  <!-- Minimalist Tesla-inspired sticky header -->
  <header class="top-nav">
    <a href="#" class="brand-wordmark" id="brand-wordmark">{brand_name}</a>
    <nav class="nav-actions" aria-label="Навігація">
      <a href="#cinema" class="nav-link">Фільм</a>
      <a href="#download" class="nav-link">Оригінал</a>
      <button type="button" class="nav-pill" id="nav-share-btn">Поділитись</button>
    </nav>
  </header>

  <main>
    <!-- Hero Section -->
    <section class="hero" id="hero">
      <div class="hero-media">
        <img id="hero-cover" src="{prefix}{cover_image}" alt="Обкладинка весільного фільму" />
        <div class="hero-gradient"></div>
      </div>

      <div class="hero-content">
        <p class="hero-eyebrow" id="hero-subtitle">{subtitle}</p>
        <h1 class="hero-title" id="hero-title">{couple}</h1>
        <div class="hero-cta-group">
          <a href="#cinema" class="btn btn-primary">Дивитись кліп</a>
          <a href="#download" class="btn btn-secondary">Завантажити оригінал</a>
        </div>
      </div>
    </section>

    <!-- Cinema Player Section -->
    <section class="section cinema-section" id="cinema">
      <div class="container">
        <div class="section-header">
          <div>
            <p class="section-kicker">Онлайн-кінотеатр</p>
            <h2 class="section-title">Перегляд на будь-якому екрані</h2>
          </div>
          <div class="player-tabs" id="player-tabs" role="tablist" aria-label="Вибір відео">
            <button type="button" class="tab-btn active" data-video="clip" role="tab" aria-selected="true">
              Кліп
            </button>
            <button type="button" class="tab-btn" data-video="full" role="tab" aria-selected="false">
              Повний фільм
            </button>
          </div>
        </div>

        <div class="player-frame" id="player-frame">
          <!-- YouTube iframe or clean placeholder injected by app.js -->
        </div>

        <div style="margin-top:18px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;">
          <p class="player-hint" id="wedding-note" style="margin:0;"></p>
          <button type="button" class="btn btn-outline" id="switch-to-full-btn">
            Перейти до повного фільму →
          </button>
        </div>
      </div>
    </section>

    <!-- Download Section -->
    <section class="section specs-section" id="download">
      <div class="container">
        <div class="cards-single">
          <article class="studio-card">
            <p class="card-kicker">Архів</p>
            <h3 class="card-title">Оригінал без стиснення</h3>
            <p class="card-desc">
              Повний майстер-файл у максимальній якості для збереження на комп'ютер або флешку.
            </p>
            <div class="spec-row">
              <span class="spec-label">Формат та обсяг</span>
              <span class="spec-value" id="drive-size">{drive_size}</span>
            </div>
            <div class="spec-row">
              <span class="spec-label">Дата</span>
              <span class="spec-value" id="wedding-date">{date}</span>
            </div>
            <p class="backup-notice">
              <strong>Рекомендація щодо зберігання:</strong> будь ласка, завантажте оригінальні файли та збережіть резервну копію на власному комп'ютері чи зовнішньому носії. Онлайн-галерея та хмарні посилання мають обмежений термін зберігання.
            </p>
            <div class="download-actions" style="display:flex;flex-direction:column;gap:10px;">
              <a id="drive-download-btn" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-full">
                Завантажити Фільм (Google Диск)
              </a>
              <a id="drive-clip-btn" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-full" hidden>
                Завантажити Кліп (Google Диск)
              </a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Filmmaker Brand Section -->
    <section class="section brand-section" id="filmmaker">
      <div class="container">
        <div class="brand-card">
          <div class="brand-info">
            <p class="section-kicker" id="brand-tagline">Wedding Cinematography</p>
            <h2 class="brand-name" id="brand-name">{brand_name}</h2>
            <p class="brand-bio" id="brand-bio"></p>
          </div>
          <div class="brand-links">
            <a id="brand-instagram" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-outline">Instagram</a>
            <a id="brand-telegram" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-outline">Telegram</a>
            <a id="brand-whatsapp" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-primary">WhatsApp</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <span id="footer-brand">{brand_name}</span>
      <span>Персональна галерея для перегляду та завантаження</span>
    </div>
  </footer>

  <div class="toast" id="toast" role="status" aria-live="polite">Посилання скопійовано</div>

  <script>
    window.__WEDDING_SLUG__ = {slug_js};
    window.__BASE_PREFIX__ = {prefix_js};
  </script>
  <script src="{prefix}app.js"></script>
</body>
</html>
"""


def render_page(brand: dict, wedding: dict, is_root: bool) -> str:
    brand_name = brand.get("name", "MILAN NECHESANOV")
    slug = wedding["slug"]
    prefix = "" if is_root else "../"
    og_url = f"{BASE_URL}/" if is_root else f"{BASE_URL}/{slug}/"
    cover_image = wedding["coverImage"]
    og_image = f"{BASE_URL}/{cover_image}"
    page_title = f"{wedding['couple']} ({wedding['date']}) — {brand_name}"
    og_description = f"{wedding['subtitle']}. Онлайн-перегляд кліпу та повного фільму + завантаження оригіналу."

    return TEMPLATE.format(
        page_title=html.escape(page_title),
        og_description=html.escape(og_description),
        brand_name=html.escape(brand_name),
        og_image=html.escape(og_image),
        og_url=html.escape(og_url),
        prefix=prefix,
        cover_image=html.escape(cover_image),
        subtitle=html.escape(wedding["subtitle"]),
        couple=html.escape(wedding["couple"]),
        drive_size=html.escape(wedding.get("driveFileSize", "")),
        date=html.escape(wedding.get("date", "")),
        slug_js=json.dumps(slug),
        prefix_js=json.dumps(prefix),
    )


def main():
    data = json.loads((SITE_DIR / "weddings.json").read_text(encoding="utf-8"))
    brand = data.get("brand", {})
    weddings = data.get("weddings", [])
    if not weddings:
        return

    # Root index.html uses the first wedding
    (SITE_DIR / "index.html").write_text(
        render_page(brand, weddings[0], is_root=True), encoding="utf-8"
    )
    print(f"Generated index.html -> {weddings[0]['slug']}")

    # Per-wedding <slug>/index.html for clean URLs & accurate social previews
    for w in weddings:
        out_dir = SITE_DIR / w["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            render_page(brand, w, is_root=False), encoding="utf-8"
        )
        print(f"Generated {w['slug']}/index.html (og:image={w['coverImage']})")


if __name__ == "__main__":
    main()
