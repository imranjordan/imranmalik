from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.platypus import PageBreak
from reportlab.lib.colors import HexColor
from datetime import date

# ── Colour palette ──────────────────────────────────────────────────────────
NAVY    = HexColor("#1B2A4A")
GOLD    = HexColor("#C9A84C")
LIGHT   = HexColor("#F5F7FA")
MID     = HexColor("#E0E6EE")
DARK    = HexColor("#2C3E50")
GREEN   = HexColor("#27AE60")
RED     = HexColor("#C0392B")
ORANGE  = HexColor("#E67E22")
WHITE   = colors.white
BLACK   = colors.black

OUTPUT  = "/home/user/imranmalik/Kashif_Publications_Competitor_Social_Media_Analysis.pdf"

# ── Document setup ───────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Competitor Social Media Analysis — Kashif Publications",
    author="Prepared for Kashif Publications"
)

W = A4[0] - 4*cm   # usable width

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

S = {
    "cover_title": style("cover_title",
        fontSize=28, leading=34, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER),
    "cover_sub": style("cover_sub",
        fontSize=13, leading=18, textColor=GOLD,
        fontName="Helvetica-Bold", alignment=TA_CENTER),
    "cover_date": style("cover_date",
        fontSize=10, leading=14, textColor=MID,
        fontName="Helvetica", alignment=TA_CENTER),
    "cover_conf": style("cover_conf",
        fontSize=9, leading=12, textColor=GOLD,
        fontName="Helvetica-Oblique", alignment=TA_CENTER),

    "h1": style("h1", "Heading1",
        fontSize=16, leading=20, textColor=NAVY,
        fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=6),
    "h2": style("h2", "Heading2",
        fontSize=12, leading=16, textColor=NAVY,
        fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4),
    "h3": style("h3",
        fontSize=10, leading=14, textColor=DARK,
        fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3),

    "body": style("body",
        fontSize=9.5, leading=14, textColor=DARK,
        fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=4),
    "bullet": style("bullet",
        fontSize=9.5, leading=14, textColor=DARK,
        fontName="Helvetica", leftIndent=14,
        firstLineIndent=0, spaceAfter=3),
    "small": style("small",
        fontSize=8.5, leading=12, textColor=colors.grey,
        fontName="Helvetica-Oblique"),
    "callout": style("callout",
        fontSize=9.5, leading=14, textColor=NAVY,
        fontName="Helvetica-Bold", alignment=TA_CENTER),
    "label": style("label",
        fontSize=8, leading=11, textColor=DARK,
        fontName="Helvetica-Bold"),
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def hr(color=MID, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=2)

def section_rule():
    return HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=8, spaceBefore=4)

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet>  {text}", S["bullet"])

def body(text):
    return Paragraph(text, S["body"])

def h1(text):  return Paragraph(text, S["h1"])
def h2(text):  return Paragraph(text, S["h2"])
def h3(text):  return Paragraph(text, S["h3"])
def sp(n=6):   return Spacer(1, n)

def badge_table(label, value, label_color=NAVY, value_color=DARK):
    """Inline label+value chip."""
    data = [[Paragraph(f"<b>{label}</b>", style("bl", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold")),
             Paragraph(value, style("bv", fontSize=8, textColor=WHITE, fontName="Helvetica"))]]
    t = Table(data, colWidths=[3*cm, W-3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), label_color),
        ("BACKGROUND", (1,0), (1,0), value_color),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def colored_table(headers, rows, col_widths=None, header_bg=NAVY):
    col_widths = col_widths or [W/len(headers)]*len(headers)
    data = [[Paragraph(f"<b>{h}</b>", style("th", fontSize=8.5, textColor=WHITE,
             fontName="Helvetica-Bold", alignment=TA_CENTER)) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), style("td", fontSize=8.5, textColor=DARK,
                      fontName="Helvetica", leading=12)) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    row_count = len(data)
    ts = [
        ("BACKGROUND",    (0,0), (-1,0),  header_bg),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.4, MID),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ]
    t.setStyle(TableStyle(ts))
    return t

def info_box(text, bg=LIGHT, border=GOLD):
    data = [[Paragraph(text, style("ib", fontSize=9, textColor=DARK,
                fontName="Helvetica", leading=13, alignment=TA_JUSTIFY))]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LINEBEFORE",    (0,0), (0,-1),  3, border),
        ("BOX",           (0,0), (-1,-1), 0.5, MID),
    ]))
    return t

def cover_block(title, subtitle, date_str, prepared_for):
    data = [
        [Paragraph(title, S["cover_title"])],
        [Spacer(1, 10)],
        [Paragraph(subtitle, S["cover_sub"])],
        [Spacer(1, 6)],
        [Paragraph(date_str, S["cover_date"])],
        [Spacer(1, 4)],
        [Paragraph(prepared_for, S["cover_conf"])],
    ]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
        ("ROWPADDING",    (0,0), (-1,-1), 0),
    ]))
    return t

# ════════════════════════════════════════════════════════════════════════════
# BUILD CONTENT
# ════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 60))
story.append(cover_block(
    "Competitor Social Media\nAnalysis Report",
    "Publication Industry — Pakistan",
    f"Prepared: {date.today().strftime('%B %d, %Y')}",
    "Prepared for: Kashif Publications  |  kashifpublications.com  |  Confidential"
))
story.append(Spacer(1, 30))

# decorative gold bar
bar = Table([[""]], colWidths=[W], rowHeights=[6])
bar.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), GOLD)]))
story.append(bar)
story.append(Spacer(1, 20))

story.append(body(
    "This report analyses the social media strategies of five key competitors in Pakistan's "
    "publication industry. It identifies what each competitor is doing, what is working, "
    "where the gaps lie, and provides a clear action plan for Kashif Publications to run "
    "a superior campaign that drives more orders through kashifpublications.com."
))
story.append(sp(4))
story.append(body(
    "<b>Competitors Analysed:</b> Ferozson Publications · Sang-e-Meel Publications · "
    "Jehlum Book Corner · Mawara Publications · Qasim Ali Shah Publications"
))
story.append(PageBreak())

# ── SECTION 1: SNAPSHOT TABLE ────────────────────────────────────────────────
story.append(h1("1. Competitor Social Media Snapshot"))
story.append(section_rule())
story.append(body(
    "The table below summarises the current social media presence of each competitor "
    "across all major platforms."
))
story.append(sp(6))

headers = ["Competitor", "Facebook", "Instagram", "Twitter/X", "YouTube", "Key Strength"]
rows = [
    ["Sang-e-Meel\nPublications",      "Active\n@sangemeel",           "66K followers\n4,342 posts",   "@sangemeel",    "—",              "Volume &\nconsistency"],
    ["Book Corner\nJhelum",            "602K+ followers\n@bookcornershowroom", "16K followers\n1,125 posts", "@BookCornerJlm", "—",         "Facebook\ncommunity king"],
    ["Qasim Ali Shah\nPublications",   "Large page\n@Qasim.Ali.Shah",  "830K followers",               "—",             "Official\nchannel", "Personal\nbrand power"],
    ["Ferozson\nPublications",         "Active\n@FerozsonsBooks",       "@info.ferozsons",              "—",             "—",              "Legacy\nbrand (underused)"],
    ["Mawara\nPublications",           "Unclear",                       "Unclear",                      "—",             "—",              "Weak online\npresence"],
    ["Kashif\nPublications",           "Active\n(Lahore)",              "Not clearly\nestablished",     "—",             "—",              "Currently\nbehind rivals"],
]
col_w = [3.2*cm, 3.5*cm, 3.2*cm, 2.5*cm, 2.2*cm, 2.9*cm]
story.append(colored_table(headers, rows, col_w))
story.append(sp(4))
story.append(Paragraph(
    "Source: Direct social media platform search, May 2026.", S["small"]
))
story.append(PageBreak())

# ── SECTION 2: COMPETITOR DEEP DIVES ─────────────────────────────────────────
story.append(h1("2. What Each Competitor Is Doing — And What Is Working"))
story.append(section_rule())

# ── 2.1 Book Corner Jhelum ───────────────────────────────────────────────────
story.append(KeepTogether([
    h2("2.1  Book Corner Jhelum — Facebook Dominance"),
    hr(),
    sp(2),
]))

story.append(info_box(
    "Platforms: Facebook (602K+ followers) · Instagram (16K) · Twitter/X · Website: bookcorner.shop"
))
story.append(sp(6))
story.append(h3("What They Do"))
story.append(body(
    "Book Corner Jhelum has built the largest Facebook community of any competitor — over "
    "600,000 followers. Their content style is conversational and interactive. They ask "
    "questions like <i>\"Don't judge a book by its cover — but if you had to, which would you "
    "pick?\"</i> which drives large volumes of comments and shares. They post book arrivals, "
    "in-store moments, and customer visits. Their brand positioning — "
    "<b>\"Pakistan's Biggest Bookstore\"</b> — is consistent and memorable."
))
story.append(sp(4))
story.append(h3("What Is Working"))
for t in [
    "A 600K Facebook audience gives massive organic reach every time they post a book link.",
    "Interactive, question-based posts create high engagement without requiring a paid budget.",
    "Consistent brand tagline ('Pakistan's Biggest Bookstore') builds top-of-mind recall.",
]:
    story.append(bullet(f"<b>✓</b>  {t}"))
story.append(sp(4))
story.append(h3("What Is Missing"))
for t in [
    "Instagram is only 16K — Facebook strength has not been converted to multi-platform presence.",
    "No visible short-form video strategy (Reels or TikTok).",
    "No clear call-to-action funnel driving Facebook followers to website purchases.",
]:
    story.append(bullet(f"<b>✗</b>  {t}"))

story.append(sp(12))

# ── 2.2 Qasim Ali Shah ───────────────────────────────────────────────────────
story.append(KeepTogether([
    h2("2.2  Qasim Ali Shah Publications — Personal Brand Selling Books"),
    hr(),
    sp(2),
]))

story.append(info_box(
    "Platforms: Instagram (830K followers) · Facebook · YouTube (Official channel) · "
    "Foundation Instagram (@qasimalishahfoundation) · Website: qasimalishah.com"
))
story.append(sp(6))
story.append(h3("What They Do"))
story.append(body(
    "Qasim Ali Shah <b>is</b> the product. His 830K Instagram following, large YouTube channel, "
    "and Facebook page are not 'marketing for books' — they ARE his brand. Every motivational "
    "post, Urdu quote, and video naturally leads followers to buy his books. His foundation "
    "runs workshops and events that act as live sales channels. He has authored 13 bestselling "
    "books covering self-help, leadership, and personal development — all in Urdu."
))
story.append(sp(4))
story.append(h3("What Is Working"))
for t in [
    "Personal brand trust: people buy from personalities they know and follow.",
    "Urdu motivational content is highly shareable — every share is free marketing.",
    "YouTube gives long-form reach; Instagram and Facebook drive daily engagement.",
    "Foundation events create in-person touchpoints that convert to book sales.",
]:
    story.append(bullet(f"<b>✓</b>  {t}"))
story.append(sp(4))
story.append(h3("What Is Missing"))
for t in [
    "This model depends on pre-existing personal fame — not immediately replicable.",
    "No strong TikTok presence to capture younger audiences.",
    "Books are sold through multiple third-party platforms — less direct-website focus.",
]:
    story.append(bullet(f"<b>✗</b>  {t}"))

story.append(sp(12))

# ── 2.3 Sang-e-Meel ──────────────────────────────────────────────────────────
story.append(KeepTogether([
    h2("2.3  Sang-e-Meel Publications — Content Volume & Multi-Platform Consistency"),
    hr(),
    sp(2),
]))

story.append(info_box(
    "Platforms: Instagram (66K followers, 4,342 posts) · Facebook (@sangemeel) · "
    "Twitter/X (@sangemeel) · Website: sangemeel.shop"
))
story.append(sp(6))
story.append(h3("What They Do"))
story.append(body(
    "Sang-e-Meel have published an extraordinary 4,342 posts on Instagram alone. They are "
    "consistently branded as <b>@sangemeel</b> across Instagram, Facebook, and X/Twitter. "
    "Content includes Urdu and English book covers, literary quotes, and author spotlights. "
    "Their strategy is built on volume and consistency — posting regularly across all platforms "
    "to stay visible in the algorithm."
))
story.append(sp(4))
story.append(h3("What Is Working"))
for t in [
    "High posting volume = consistent algorithm visibility = steady follower growth.",
    "Uniform handle (@sangemeel everywhere) makes them easy to find and remember.",
    "Multi-platform presence ensures they reach different audience segments.",
]:
    story.append(bullet(f"<b>✓</b>  {t}"))
story.append(sp(4))
story.append(h3("What Is Missing"))
for t in [
    "High volume does not always equal high conversion — weak 'buy now' CTA strategy.",
    "No visible short-form video (Reels/TikTok) despite the algorithm favouring it.",
    "Social posts do not appear to drive traffic optimally to sangemeel.shop.",
]:
    story.append(bullet(f"<b>✗</b>  {t}"))

story.append(sp(12))

# ── 2.4 Ferozsons ────────────────────────────────────────────────────────────
story.append(KeepTogether([
    h2("2.4  Ferozson Publications — Legacy Brand, Weak Online Game"),
    hr(),
    sp(2),
]))

story.append(info_box(
    "Platforms: Facebook (@FerozsonsBooks) · Instagram (@info.ferozsons) · "
    "Website: ferozsons.com.pk  |  Also selling on Daraz.pk"
))
story.append(sp(6))
story.append(h3("What They Do"))
story.append(body(
    "Pakistan's oldest publisher, established in 1894, with a distribution network across "
    "200+ markets. Their offline reputation and Daraz presence do the heavy lifting. "
    "Social media activity exists but is thin relative to their brand authority."
))
story.append(sp(4))
story.append(h3("What Is Working"))
for t in [
    "130-year heritage provides unmatched brand trust — no social campaign needed to establish credibility.",
    "Daraz listing gives them marketplace reach beyond their own website.",
]:
    story.append(bullet(f"<b>✓</b>  {t}"))
story.append(sp(4))
story.append(h3("What Is Missing — And What Is YOUR Opportunity"))
for t in [
    "A 130-year brand story is being told nowhere on Instagram Reels or YouTube.",
    "Minimal engagement-driven content — no community building.",
    "This gap means a newer publisher with good content can capture the digital audience Ferozsons ignores.",
]:
    story.append(bullet(f"<b>✗</b>  {t}"))

story.append(sp(12))

# ── 2.5 Mawara ───────────────────────────────────────────────────────────────
story.append(KeepTogether([
    h2("2.5  Mawara Publications — Weak Online Presence"),
    hr(),
    sp(2),
]))
story.append(body(
    "No confirmed, verified social media accounts were found for Mawara Publications. "
    "They present the least competitive threat in the digital space and represent a baseline "
    "that Kashif Publications should aim to surpass immediately."
))
story.append(PageBreak())

# ── SECTION 3: GAPS IN THE MARKET ────────────────────────────────────────────
story.append(h1("3. The Gaps Nobody Is Filling — Your Competitive Opportunities"))
story.append(section_rule())
story.append(body(
    "The analysis reveals clear, uncontested opportunities that no competitor is currently "
    "exploiting. Kashif Publications should move quickly to own these spaces."
))
story.append(sp(8))

headers2 = ["Gap in the Market", "Why It Matters", "Priority"]
rows2 = [
    ["No competitor owns TikTok",
     "Pakistani Gen Z and millennials are heavily on TikTok. First-mover advantage is available right now.",
     "🔴 HIGH"],
    ["No Urdu short-form book\nsummary videos",
     '"Yeh kitaab kya kehti hai?" — 60-second Reels explaining a book in Urdu are highly shareable and drive purchase intent.',
     "🔴 HIGH"],
    ["No WhatsApp sales funnel",
     "Pakistan runs on WhatsApp. None of the competitors have a proper WhatsApp-to-order flow for direct book sales.",
     "🔴 HIGH"],
    ["No in-app Facebook /\nInstagram Shop",
     "Direct in-app shopping linked to the website reduces drop-offs and increases conversions significantly.",
     "🟠 MEDIUM"],
    ["No author storytelling content",
     "Who wrote this book? Why? Their personal story? This emotional content drives purchase decisions and is unused by all rivals.",
     "🟠 MEDIUM"],
    ["No email / SMS retargeting\nfor website visitors",
     "Retargeting website visitors who did not buy is completely underutilised by all competitors — very high ROI.",
     "🟠 MEDIUM"],
    ["No Facebook Reader\nCommunity Group",
     "Book Corner Jhelum built 600K followers over time. A dedicated reader community group accelerates this.",
     "🟡 BUILD OVER TIME"],
]
col_w2 = [4.5*cm, 8.5*cm, 2.5*cm]
story.append(colored_table(headers2, rows2, col_w2))
story.append(PageBreak())

# ── SECTION 4: STRATEGY ───────────────────────────────────────────────────────
story.append(h1("4. Recommended Social Media Strategy for Kashif Publications"))
story.append(section_rule())

# ── 4.1 ──────────────────────────────────────────────────────────────────────
story.append(h2("4.1  Phase 1 — Foundation Setup  (Month 1–2)"))
story.append(hr())
story.append(sp(2))
for item in [
    "<b>Unified branding:</b> Register the same handle (e.g. @kashifpublications) on Facebook, Instagram, and TikTok. Consistency makes the brand searchable and memorable.",
    "<b>Facebook + Instagram Shop:</b> Connect both platforms directly to kashifpublications.com so followers can browse and buy books without leaving the app.",
    "<b>WhatsApp Business account:</b> Set up a catalogue of books. Add the number to every social post and website page. Pakistani buyers expect to be able to WhatsApp before purchasing.",
    "<b>Link in bio:</b> Every profile bio must have a direct link to kashifpublications.com — this is the most basic driver of website traffic from social media.",
    "<b>Pixel / tracking:</b> Install the Facebook Pixel on kashifpublications.com so website visitors can be retargeted with ads later.",
]:
    story.append(bullet(item))
    story.append(sp(2))

story.append(sp(8))

# ── 4.2 Content Calendar ─────────────────────────────────────────────────────
story.append(h2("4.2  Phase 2 — Weekly Content Calendar  (Month 1 onwards, ongoing)"))
story.append(hr())
story.append(sp(4))

headers3 = ["Content Type", "Platform(s)", "Frequency", "Primary Goal"]
rows3 = [
    ["Urdu quote / book excerpt\n(calligraphy-style graphic)", "Facebook + Instagram", "3–4× per week", "Shares & reach"],
    ['"Yeh kitaab kya kehti hai?"\n60-sec Reel (Urdu book summary)', "Instagram + TikTok", "2× per week", "Reach new audience"],
    ["Author spotlight /\nbehind-the-scenes", "Instagram Stories", "2× per week", "Trust & connection"],
    ['"Book of the Week" with\nBuy Now link + WhatsApp', "Facebook + Instagram", "1× per week", "Direct orders"],
    ["Customer unboxing /\nreview reposts", "All platforms", "1–2× per week", "Social proof"],
    ['Interactive post\n("Which book are you reading?")', "Facebook", "1× per week", "Community engagement"],
    ["New arrival announcement\nwith website link", "Facebook + Instagram + TikTok", "On every new release", "Traffic to website"],
]
col_w3 = [4.8*cm, 3.5*cm, 2.5*cm, 4.7*cm]
story.append(colored_table(headers3, rows3, col_w3))
story.append(sp(8))

# ── 4.3 Paid Ads ─────────────────────────────────────────────────────────────
story.append(h2("4.3  Phase 3 — Paid Advertising  (Month 2–3)"))
story.append(hr())
story.append(sp(2))
for item in [
    "<b>Facebook & Instagram ads:</b> Target Pakistan, ages 18–45, interests: books, Urdu literature, self-improvement, education. Cost per click in Pakistan is low (PKR 10–400), so even a modest budget has strong reach.",
    "<b>Retargeting ads:</b> Show ads to people who visited kashifpublications.com but did not place an order. Offer a small discount or free delivery to convert them.",
    "<b>'Book of the Week' offer ads:</b> A limited-time discount with a countdown timer creates urgency and drives direct purchases.",
    "<b>Video ad Reels:</b> Boost the best-performing organic Reels as paid ads — this is the lowest-cost way to reach a new audience at scale.",
]:
    story.append(bullet(item))
    story.append(sp(2))

story.append(sp(8))

# ── 4.4 Community ────────────────────────────────────────────────────────────
story.append(h2("4.4  Phase 4 — Community & Loyalty Building  (Month 3+)"))
story.append(hr())
story.append(sp(2))
for item in [
    "<b>Facebook Reader Group:</b> Create 'Kashif Publications Readers Club' — a community group where readers discuss books, share reviews, and get exclusive early access to new titles. Book Corner Jhelum's 600K did not happen overnight; it starts here.",
    "<b>Monthly giveaways:</b> One free book per month drives followers, shares, and page likes organically. Tag-a-friend mechanic multiplies reach.",
    "<b>Reading challenge:</b> Launch #KashifReadsChallenge — readers share photos of their Kashif books. Reader-generated content = free marketing and social proof.",
    "<b>Email list:</b> Collect emails from website buyers and offer a 'new arrivals' newsletter. No competitor is doing this — it creates a direct, algorithm-free channel.",
]:
    story.append(bullet(item))
    story.append(sp(2))

story.append(PageBreak())

# ── SECTION 5: SUMMARY TABLE ─────────────────────────────────────────────────
story.append(h1("5. Competitor Winning Formula — One-Line Summary"))
story.append(section_rule())
story.append(sp(4))

headers4 = ["Competitor", "Their Winning Formula"]
rows4 = [
    ["Book Corner Jhelum",      "Facebook community first, everything else second"],
    ["Qasim Ali Shah",          "The author IS the brand — personal trust sells books"],
    ["Sang-e-Meel Publications","Post consistently everywhere and the algorithm rewards you"],
    ["Ferozson Publications",   "Legacy reputation does the work — social media is an afterthought"],
    ["Mawara Publications",     "No clear social media strategy identified"],
]
col_w4 = [5*cm, 10.5*cm]
story.append(colored_table(headers4, rows4, col_w4))
story.append(sp(16))

story.append(info_box(
    "<b>Kashif Publications' Winning Formula Should Be:</b><br/><br/>"
    "Short-form video content (Reels + TikTok) in Urdu, driving to a seamless WhatsApp + "
    "website order flow — filling the gap all competitors have left open. The goal is not "
    "to copy what competitors do, but to do what none of them are doing.",
    bg=HexColor("#EAF4FF"), border=NAVY
))

story.append(sp(16))

# ── SECTION 6: SINGLE BEST ACTION ────────────────────────────────────────────
story.append(h1("6. The Single Best Action to Start Driving Orders"))
story.append(section_rule())
story.append(sp(4))

best = Table([[Paragraph(
    "Launch a weekly <b>\"Book of the Week\" Reel</b> on Instagram and TikTok — "
    "60 seconds, in Urdu, explaining why someone needs to read that specific book. "
    "End every video with the WhatsApp number and website link in caption. "
    "This format is uncontested in this market and directly drives order intent.",
    style("bo", fontSize=11, leading=16, textColor=NAVY, fontName="Helvetica",
          alignment=TA_JUSTIFY)
)]], colWidths=[W])
best.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
    ("LEFTPADDING",   (0,0), (-1,-1), 20),
    ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ("TOPPADDING",    (0,0), (-1,-1), 16),
    ("BOTTOMPADDING", (0,0), (-1,-1), 16),
    ("BOX",           (0,0), (-1,-1), 2, GOLD),
]))
story.append(best)
story.append(sp(16))

# ── FOOTER NOTE ───────────────────────────────────────────────────────────────
story.append(hr(color=MID))
story.append(Paragraph(
    f"This report was prepared exclusively for Kashif Publications (kashifpublications.com) "
    f"based on publicly available social media data as of {date.today().strftime('%B %Y')}. "
    "All follower counts and platform data are subject to change.",
    S["small"]
))

# ── BUILD PDF ─────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF created: {OUTPUT}")
