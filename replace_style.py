import re

# Read file
with open('index.html', encoding='utf-8') as f:
    content = f.read()

NEW_CSS = """  <style>
    /* =============================================
       REFINED DESIGN SYSTEM — Editorial Luxury
       Palette: Warm Ivory · Burgundy · Deep Maroon · Near-Black
       Aesthetic: Understated, Sophisticated, Authoritative
       ============================================= */
    :root {
      /* Core Palette */
      --ivory:          #EDE7C7;
      --ivory-soft:     #F4F0E0;
      --ivory-muted:    #E3DBB8;
      --burgundy:       #8B0000;
      --burgundy-dark:  #5B0202;
      --near-black:     #200E01;

      /* Refined UI Surface Colors */
      --surface:        #FAFAF7;
      --surface-card:   #FFFFFF;
      --surface-warm:   #F8F5EC;
      --rule:           #E8E4D8;
      --rule-dark:      #C8C0A0;

      /* Text Hierarchy */
      --text-ink:       #1A0A00;
      --text-dim:       #6B5744;
      --text-hint:      #A0907A;

      /* Muted Antique Gold Accent */
      --gold:           #A8892E;
      --gold-subtle:    rgba(168,137,46,0.15);

      /* Aliases for backward-compatibility with JS */
      --royal-blue:      #8B0000;
      --deep-maroon:     #5B0202;
      --midnight-maroon: #200E01;
      --amber-gold:      #A8892E;
      --amber-hover:     #8A7025;
      --amber-light:     #C9A84C;
      --deep-navy:       #8B0000;
      --midnight-navy:   #5B0202;
      --secondary-navy:  #8B0000;
      --secondary-maroon:#8B0000;
      --antique-gold:    #A8892E;
      --light-gold:      #C9A84C;
      --warm-ivory:      #EDE7C7;
      --white:           #FFFFFF;
      --text-primary:    #1A0A00;
      --text-secondary:  #6B5744;
      --border:          #E8E4D8;
      --shadow-sm:       0 1px 3px rgba(26,10,0,0.07), 0 4px 16px rgba(26,10,0,0.05);
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      font-family: 'Inter', system-ui, Arial, sans-serif;
      font-size: 15px;
      line-height: 1.65;
      color: var(--text-ink);
      background: var(--surface);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    a { text-decoration: none; color: inherit; }
    img { max-width: 100%; height: auto; }

    /* ═══════════════════════════════
       HEADER — Deep, quiet, sticky
       ═══════════════════════════════ */
    header {
      background: var(--near-black);
      color: var(--ivory-soft);
      padding: 0 6%;
      height: 66px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 32px;
      position: sticky;
      top: 0;
      z-index: 100;
      border-bottom: 1px solid rgba(237,231,199,0.07);
    }

    .brand { display: flex; flex-direction: column; gap: 2px; }

    .brand b {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 19px;
      font-weight: 600;
      letter-spacing: 0.25px;
      color: var(--ivory-soft);
      line-height: 1.2;
    }

    .brand small {
      display: block;
      font-size: 9px;
      letter-spacing: 2.8px;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 400;
      opacity: 0.75;
    }

    nav {
      display: flex;
      gap: 30px;
      align-items: center;
    }

    nav a {
      color: rgba(237,231,199,0.55);
      font-weight: 400;
      transition: color 0.2s;
      text-transform: uppercase;
      letter-spacing: 0.9px;
      font-size: 11px;
    }

    nav a:hover { color: var(--ivory-soft); }

    .cta-btn {
      background: transparent;
      color: rgba(237,231,199,0.80);
      border: 1px solid rgba(237,231,199,0.22);
      padding: 8px 20px;
      border-radius: 2px;
      font-weight: 400;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.22s;
      letter-spacing: 0.7px;
      text-transform: uppercase;
    }

    .cta-btn:hover {
      border-color: var(--gold);
      color: var(--gold);
    }

    /* ═══════════════════════════════
       HERO — Rich dark, restrained
       ═══════════════════════════════ */
    .hero {
      background: var(--burgundy-dark);
      color: var(--ivory-soft);
      text-align: center;
      padding: 90px 6% 72px;
      position: relative;
      overflow: hidden;
    }

    /* Subtle vignette — no cartoon glow */
    .hero::after {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 85% 70% at 50% 50%, transparent 35%, rgba(32,14,1,0.50) 100%);
      pointer-events: none;
    }

    .hero-inner { position: relative; z-index: 1; }

    /* Thin ornamental rule */
    .hero-ornament {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 14px;
      margin-bottom: 26px;
    }

    .hero-ornament span {
      display: block;
      width: 44px;
      height: 1px;
      background: var(--gold);
      opacity: 0.50;
    }

    .hero-ornament em {
      font-family: 'Cormorant Garamond', serif;
      font-style: italic;
      font-size: 11px;
      color: var(--gold);
      letter-spacing: 2.5px;
      text-transform: uppercase;
      opacity: 0.80;
    }

    .hero h1 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 50px;
      font-weight: 600;
      margin: 0 0 18px;
      color: var(--ivory-soft);
      line-height: 1.18;
      letter-spacing: -0.3px;
    }

    .hero p {
      max-width: 520px;
      margin: 0 auto 46px;
      font-size: 14.5px;
      color: rgba(237,231,199,0.52);
      line-height: 1.80;
      font-weight: 300;
    }

    /* Search box — understated glass */
    .searchbox {
      max-width: 820px;
      margin: 0 auto;
      background: rgba(255,255,255,0.05);
      padding: 10px;
      border-radius: 3px;
      display: grid;
      grid-template-columns: 1.6fr 1fr 1fr auto;
      gap: 8px;
      border: 1px solid rgba(237,231,199,0.12);
    }

    .searchbox input,
    .searchbox select {
      border: 1px solid rgba(237,231,199,0.15);
      border-radius: 2px;
      padding: 11px 14px;
      font: inherit;
      font-size: 13.5px;
      color: var(--ivory-soft);
      background: rgba(255,255,255,0.06);
      transition: border-color 0.2s;
      -webkit-appearance: none;
    }

    .searchbox input::placeholder  { color: rgba(237,231,199,0.35); }
    .searchbox select option        { background: var(--near-black); color: var(--ivory-soft); }

    .searchbox input:focus,
    .searchbox select:focus {
      outline: none;
      border-color: rgba(168,137,46,0.55);
    }

    .searchbox .btn {
      background: var(--burgundy);
      color: var(--ivory-soft);
      border: none;
      border-radius: 2px;
      padding: 11px 22px;
      font-weight: 500;
      font-size: 13px;
      cursor: pointer;
      transition: background 0.2s;
      white-space: nowrap;
    }

    .searchbox .btn:hover { background: #6E0000; }

    /* ═══════════════════════════════
       DIRECTORY SECTION HEADING
       ═══════════════════════════════ */
    .section {
      padding: 52px 6%;
      max-width: 1280px;
      margin: auto;
    }

    .sectionhead {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--rule);
    }

    .section h2 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      color: var(--text-ink);
      font-size: 30px;
      font-weight: 600;
      margin: 0;
      letter-spacing: -0.3px;
    }

    .sectionhead p {
      color: var(--text-hint);
      font-size: 12.5px;
      margin-top: 5px;
    }

    .add {
      border: 1px solid var(--rule-dark);
      background: transparent;
      color: var(--text-dim);
      padding: 9px 18px;
      border-radius: 2px;
      font-weight: 500;
      font-size: 12.5px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .add:hover {
      border-color: var(--burgundy);
      color: var(--burgundy);
      background: rgba(139,0,0,0.03);
    }

    /* ═══════════════════════════════
       CHURCH CARDS
       ═══════════════════════════════ */
    .directory {
      background: var(--surface-warm);
      padding: 40px 6%;
      border-top: 1px solid var(--rule);
      border-bottom: 1px solid var(--rule);
    }

    .grid {
      display: grid;
      gap: 22px;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      max-width: 1280px;
      margin: auto;
    }

    .card {
      background: var(--surface-card);
      border: 1px solid var(--rule);
      border-radius: 2px;
      padding: 26px 28px;
      box-shadow: var(--shadow-sm);
      transition: box-shadow 0.28s, border-color 0.28s, transform 0.28s;
      position: relative;
    }

    /* Slim left accent bar on hover */
    .card::before {
      content: '';
      position: absolute;
      left: 0; top: 22%; bottom: 22%;
      width: 2px;
      background: var(--burgundy);
      opacity: 0;
      transition: opacity 0.28s;
      border-radius: 0 1px 1px 0;
    }

    .card:hover {
      transform: translateY(-2px);
      border-color: rgba(139,0,0,0.18);
      box-shadow: 0 6px 20px rgba(26,10,0,0.09), 0 1px 4px rgba(26,10,0,0.05);
    }

    .card:hover::before { opacity: 1; }

    .country {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--text-hint);
      font-weight: 500;
    }

    .card h3 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      color: var(--text-ink);
      font-size: 21px;
      font-weight: 600;
      margin: 8px 0 10px;
      line-height: 1.28;
      letter-spacing: -0.2px;
    }

    .meta {
      font-size: 13px;
      color: var(--text-dim);
      line-height: 1.7;
    }

    .card .line {
      border: none;
      border-top: 1px solid var(--rule);
      margin: 16px 0;
    }

    .card a.more {
      color: var(--burgundy);
      font-size: 12.5px;
      font-weight: 500;
      transition: color 0.2s;
      letter-spacing: 0.2px;
    }

    .card a.more:hover { color: var(--gold); }

    /* ═══════════════════════════════
       FOOTER
       ═══════════════════════════════ */
    .footer {
      background: var(--near-black);
      color: rgba(237,231,199,0.65);
      padding: 64px 6% 48px;
      text-align: center;
      position: relative;
    }

    .footer::before {
      content: '';
      position: absolute;
      top: 0; left: 8%; right: 8%;
      height: 1px;
      background: rgba(168,137,46,0.28);
    }

    .footer-inner {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      max-width: 640px;
      margin: 0 auto;
    }

    .footer-copy {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 18px;
      color: var(--ivory-soft);
      font-weight: 600;
      letter-spacing: 0.2px;
    }

    .footer-note {
      font-size: 13px;
      color: rgba(237,231,199,0.38);
      line-height: 1.8;
      max-width: 480px;
    }

    .footer-credit {
      font-size: 13px;
      color: rgba(237,231,199,0.52);
      margin-top: 8px;
    }

    .footer-credit strong { color: rgba(237,231,199,0.78); font-weight: 500; }

    .footer-credit a {
      color: var(--gold);
      font-weight: 500;
      text-decoration: none;
      border-bottom: 1px solid rgba(168,137,46,0.28);
      padding-bottom: 1px;
      transition: all 0.2s;
    }

    .footer-credit a:hover { color: var(--amber-light); border-color: var(--amber-light); }

    .footer-legal-links {
      display: flex;
      gap: 16px;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      font-size: 11px;
      color: rgba(237,231,199,0.28);
      margin-top: 20px;
    }

    .footer-legal-links a {
      color: rgba(237,231,199,0.35);
      text-decoration: none;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      transition: color 0.2s;
    }

    .footer-legal-links a:hover { color: rgba(237,231,199,0.72); }

    /* ═══════════════════════════════
       MODALS
       ═══════════════════════════════ */
    .modal {
      position: fixed;
      inset: 0;
      background: rgba(26,10,0,0.65);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 200;
    }

    .modal.show { display: flex; }

    .modalbox {
      background: var(--surface-card);
      width: min(540px, 100%);
      border-radius: 3px;
      padding: 36px;
      border: 1px solid var(--rule);
      box-shadow: 0 24px 64px rgba(26,10,0,0.22), 0 4px 16px rgba(26,10,0,0.10);
    }

    .modalbox h2 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      color: var(--text-ink);
      margin: 0 0 4px;
      font-size: 24px;
      font-weight: 600;
      letter-spacing: -0.3px;
    }

    .formgrid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 16px;
    }

    .formgrid input,
    .formgrid select,
    .formgrid textarea {
      width: 100%;
      border: 1px solid var(--rule);
      border-radius: 2px;
      padding: 10px 13px;
      font: inherit;
      font-size: 13.5px;
      background: var(--surface);
      color: var(--text-ink);
      transition: border-color 0.2s;
    }

    .formgrid input:focus,
    .formgrid select:focus,
    .formgrid textarea:focus {
      outline: none;
      border-color: var(--burgundy);
      box-shadow: 0 0 0 2px rgba(139,0,0,0.08);
    }

    .formgrid input::placeholder,
    .formgrid textarea::placeholder { color: var(--text-hint); font-size: 13px; }

    .full { grid-column: 1 / -1; }

    .modalactions {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 20px;
    }

    .modalactions .add {
      background: var(--burgundy);
      color: var(--ivory-soft);
      border: none;
      padding: 10px 20px;
      border-radius: 2px;
      cursor: pointer;
      font-weight: 500;
      font-size: 13px;
      transition: background 0.2s;
    }

    .modalactions .add:hover { background: var(--burgundy-dark); }

    /* ═══════════════════════════════
       STATUS BADGES
       ═══════════════════════════════ */
    .card-top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }

    .status-badge {
      font-size: 9.5px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 2px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      letter-spacing: 0.7px;
      text-transform: uppercase;
    }

    .badge-approved { background: rgba(4,120,87,0.07);  color: #065F46; border: 1px solid rgba(4,120,87,0.16); }
    .badge-pending  { background: rgba(120,80,4,0.07);  color: #78500A; border: 1px solid rgba(120,80,4,0.16); }
    .badge-rejected { background: rgba(139,0,0,0.07);   color: #8B0000; border: 1px solid rgba(139,0,0,0.16); }

    .admin-actions {
      display: flex;
      gap: 6px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--rule);
    }

    .btn-approve, .btn-reject, .btn-delete {
      border: none;
      padding: 5px 11px;
      border-radius: 2px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      letter-spacing: 0.3px;
      transition: background 0.18s;
    }

    .btn-approve { background: rgba(4,120,87,0.10);  color: #065F46; }
    .btn-approve:hover { background: rgba(4,120,87,0.20); }
    .btn-reject  { background: rgba(139,0,0,0.10);   color: #8B0000; }
    .btn-reject:hover  { background: rgba(139,0,0,0.20); }
    .btn-delete  { background: rgba(100,90,80,0.10); color: #4B4030; }
    .btn-delete:hover  { background: rgba(100,90,80,0.20); }

    /* ═══════════════════════════════
       CHURCH DETAIL MODAL
       ═══════════════════════════════ */
    #details-modal .modalbox {
      width: min(640px, 100%);
      max-height: 90vh;
      overflow-y: auto;
    }

    .details-header {
      border-bottom: 1px solid var(--rule);
      padding-bottom: 18px;
      margin-bottom: 22px;
    }

    .details-header .country-badge {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--text-hint);
      font-weight: 500;
      margin-bottom: 8px;
    }

    .details-header h2 {
      margin: 0 0 5px;
      font-size: 26px;
      color: var(--text-ink);
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-weight: 600;
      letter-spacing: -0.3px;
    }

    .inline-tagline {
      font-size: 12px;
      font-style: italic;
      font-family: 'Cormorant Garamond', Georgia, serif;
      color: var(--text-hint);
    }

    .details-pastor {
      font-size: 13px;
      font-weight: 500;
      color: var(--text-dim);
      margin-top: 4px;
    }

    .details-fields {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }

    .details-fields .field { display: flex; flex-direction: column; gap: 4px; }
    .details-fields .field.full { grid-column: 1 / -1; }

    .details-fields .field label {
      font-size: 9.5px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      font-weight: 600;
      color: var(--text-hint);
    }

    .details-fields .field span {
      font-size: 14px;
      color: var(--text-ink);
      font-weight: 400;
    }

    .details-fields .field span.empty {
      color: var(--rule-dark);
      font-style: italic;
      font-size: 13px;
    }

    .details-divider {
      border: none;
      border-top: 1px solid var(--rule);
      margin: 22px 0;
    }

    /* ═══════════════════════════════
       RESPONSIVE
       ═══════════════════════════════ */
    @media (max-width: 860px) {
      nav { display: none; }
      .searchbox { grid-template-columns: 1fr 1fr; }
      .grid { grid-template-columns: 1fr 1fr; }
      .hero h1 { font-size: 36px; }
      .hero { padding: 68px 5% 56px; }
    }

    @media (max-width: 560px) {
      .searchbox, .grid, .formgrid { grid-template-columns: 1fr; }
      .sectionhead { flex-direction: column; align-items: flex-start; gap: 14px; }
      .hero { padding: 60px 5% 50px; }
      .hero h1 { font-size: 28px; }
      .details-fields { grid-template-columns: 1fr; }
      .details-fields .field.full { grid-column: 1; }
      .modalbox { padding: 24px; }
    }
  </style>"""

# Replace the style block
new_content = re.sub(r'  <style>.*?  </style>', NEW_CSS, content, flags=re.DOTALL, count=1)

if new_content == content:
    print("ERROR: Pattern not matched!")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Style block replaced.")
    print(f"Old length: {len(content)}, New length: {len(new_content)}")
