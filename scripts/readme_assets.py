#!/usr/bin/env python3
"""Build the README's generated parts: hero banner, tech stack badges and app cards.

    python scripts/readme_assets.py

App cards copy the github-stats-extended pin card (dark theme) so they sit
naturally next to the "GitHub Stats" cards. Edit STACK / GROUPS below, re-run,
and commit the changes. Needs Pillow.
"""
import base64
import colorsys
import io
import os
import re
import urllib.parse
import urllib.request

from PIL import Image, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
PLAY = "https://play.google.com/store/apps/details?id="
PLAY_DEV = "https://play.google.com/store/apps/dev?id=5785086860664884952"
APPSTORE_DEV = "https://apps.apple.com/us/developer/imam-hossain/id6797708668"


# ---------------------------------------------------------------- tech stack
def _logo(svg):
    return urllib.parse.quote("data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode(), safe="")


def _squares(c):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>"
            f"<path fill='{c[0]}' d='M1 1h10.5v10.5H1z'/><path fill='{c[1]}' d='M12.5 1H23v10.5H12.5z'/>"
            f"<path fill='{c[2]}' d='M1 12.5h10.5V23H1z'/><path fill='{c[3]}' d='M12.5 12.5H23V23H12.5z'/></svg>")


# shields.io no longer ships Microsoft or Amazon logos, so these are drawn here.
MICROSOFT = _logo(_squares(["#F25022", "#7FBA00", "#00A4EF", "#FFB900"]))
WINDOWS = _logo(_squares(["#fff"] * 4))
AWS = _logo("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><text x='12' y='12.5' text-anchor='middle' "
            "font-family='Arial,Helvetica,sans-serif' font-weight='700' font-size='11' fill='#fff'>aws</text>"
            "<path d='M3 15.5c5.6 3.6 12.4 3.6 18 0' fill='none' stroke='#FF9900' stroke-width='2' stroke-linecap='round'/>"
            "<path d='M18 14.6l3.2.9-.9 3.1' fill='none' stroke='#FF9900' stroke-width='2' stroke-linecap='round' "
            "stroke-linejoin='round'/></svg>")

# group -> badges: (name, colour, shields logo slug or drawn logo or None, logo colour, link)
STACK = [
    ("Languages", [
        ("Kotlin", "0095D5", "kotlin", "white", None),
        ("Swift", "FA7343", "swift", "white", None),
        ("Dart", "0175C2", "dart", "white", None),
        ("Java", "ED8B00", "openjdk", "white", None),
        ("Python", "3776AB", "python", "white", None),
        ("C#", "239120", None, None, None),
        ("JavaScript", "323330", "javascript", "F7DF1E", None),
        ("PHP", "777BB4", "php", "white", None),
        ("C", "00599C", "c", "white", None),
        ("C++", "00599C", "c++", "white", None),
    ]),
    ("Mobile", [
        ("Android", "3DDC84", "android", "white", None),
        ("Jetpack Compose", "4285F4", "jetpackcompose", "white", None),
        ("Flutter", "02569B", "flutter", "white", None),
        ("iOS", "000000", "ios", "white", None),
        ("SwiftUI", "0D96F6", "swift", "white", None),
    ]),
    ("Backend & Web", [
        ("Django", "092E20", "django", "white", None),
        ("Flask", "000000", "flask", "white", None),
        (".NET", "512BD4", "dotnet", "white", None),
        ("Node.js", "339933", "nodedotjs", "white", None),
        ("Laravel", "FF2D20", "laravel", "white", None),
        ("WordPress", "21759B", "wordpress", "white", None),
        ("Wix", "000000", "wix", "white", None),
        ("Bright Data Proxy", "3D7FFC", None, None, None),
    ]),
    ("AI & ML", [
        ("Microsoft Foundry", "5C2D91", MICROSOFT, None, None),
        ("AWS Bedrock", "232F3E", AWS, None, None),
        ("Replicate", "000000", "replicate", "white", None),
        ("OpenVINO", "0071C5", "intel", "white", None),
    ]),
    ("AI Coding Tools", [
        ("ChatGPT", "10A37F", None, None, None),
        ("Codex", "000000", None, None, None),
        ("Claude Code", "D97757", "claude", "white", None),
        ("OpenCode", "211E1E", "opencode", "white", None),
        ("Antigravity", "4285F4", None, None, None),
        ("Gemini", "8E75B2", "googlegemini", "white", None),
        ("Qwen", "615CED", "qwen", "white", None),
    ]),
    ("Cloud & Serverless", [
        ("AWS", "232F3E", AWS, None, None),
        ("AWS Lambda", "232F3E", AWS, None, None),
        ("AWS Lightsail", "232F3E", AWS, None, None),
        ("Azure", "0078D4", MICROSOFT, None, None),
        ("Google Cloud", "4285F4", "googlecloud", "white", None),
        ("Google Cloud Functions", "4285F4", "googlecloud", "white", None),
        ("Vercel", "000000", "vercel", "white", None),
        ("Render", "46E3B7", "render", "black", None),
        ("Cloudflare", "F38020", "cloudflare", "white", None),
        ("Heroku", "430098", None, None, None),
    ]),
    ("Containers & DevOps", [
        ("Docker", "2496ED", "docker", "white", None),
        ("Kubernetes", "326CE5", "kubernetes", "white", None),
        ("Azure Kubernetes Service", "0078D4", MICROSOFT, None, None),
        ("GKE", "4285F4", "googlecloud", "white", None),
        ("GitHub Actions", "2088FF", "githubactions", "white", None),
    ]),
    ("Databases", [
        ("Supabase", "3ECF8E", "supabase", "white", None),
        ("MySQL", "00000F", "mysql", "white", None),
        ("SQLite", "07405E", "sqlite", "white", None),
        ("MongoDB", "4EA94B", "mongodb", "white", None),
        ("JSON", "5E5C5C", "json", "white", None),
    ]),
    ("Ad Monetization", [
        ("AppLovin MAX", "24292F", None, None, None),
        ("Unity Ads", "000000", "unity", "white", None),
        ("Liftoff", "24292F", None, None, None),
        ("Meta Audience Network", "0467DF", "meta", "white", None),
        ("Mintegral", "24292F", None, None, None),
    ]),
    ("Tools", [
        ("Git", "F05032", "git", "white", None),
        ("Android Studio", "3DDC84", "androidstudio", "white", None),
        ("Xcode", "147EFB", "xcode", "white", None),
        ("Postman", "FF6C37", "postman", "white", None),
        ("Jira", "0052CC", "jira", "white", None),
        ("Adobe XD", "470137", None, None, None),
        ("Arduino", "00979D", "arduino", "white", None),
    ]),
    ("Platforms & OS", [
        ("Google Play", "414141", "googleplay", "white", PLAY_DEV),
        ("App Store", "0D96F6", "appstore", "white", APPSTORE_DEV),
        ("macOS", "000000", "apple", "white", None),
        ("Windows", "0078D6", WINDOWS, None, None),
        ("Zorin OS", "0CC1F3", "zorin", "white", None),
    ]),
]


BADGE_RADIUS = 6


def badge_slug(name):
    s = name.lower().replace("#", "-sharp").replace("+", "-plus").replace(".", "dot")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def badge_file(name, color, logo, logo_color):
    """Fetch the shields.io for-the-badge SVG and round its corners (the style itself has none)."""
    label = urllib.parse.quote(name.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="._")
    url = f"https://img.shields.io/badge/{label}-{color}?style=for-the-badge"
    if logo:
        url += "&logo=" + (logo if logo.startswith("data%3A") else urllib.parse.quote(logo, safe=""))
    if logo_color:
        url += f"&logoColor={logo_color}"
    svg = fetch(url).decode()
    svg, n = re.subn(r'<g shape-rendering="crispEdges"><rect ', f'<g><rect rx="{BADGE_RADIUS}" ', svg, count=1)
    if not n:
        raise SystemExit(f"Unexpected shields.io markup for {name!r}; can't round its corners")
    rel = f"assets/badges/{badge_slug(name)}.svg"
    write(rel, svg)
    return rel


def badge(name, color, logo, logo_color, href):
    md = f"![{name}]({badge_file(name, color, logo, logo_color)})"
    return f"[{md}]({href})" if href else md

# App groups, in README order. Each app: slug, name, type (card dot label), description,
# Android package, also on the App Store, Play icon key.
GROUPS = [
    ("Downloaders", "Save videos, reels, stories and photos from your favorite social apps.", [
        ("media-saver", "Media Saver: Video Download", "All-in-one",
         "Download & save HD videos, photos, reels & stories from all your favorite apps.",
         "com.newagedevs.mediasaver", False,
         "MUa7YdaOv5dIL3_kscgk5wNVdIHo7xgOmcxewWzGJORe9vd6PgvdaGlnP59prv94NV9vUmolRhIi4uZFtBWLKg"),
        ("facebook-video-downloader", "Fb Video Downloader", "Facebook",
         "Download images, videos, reels & stories from Facebook easily.",
         "com.newagedevs.facebook_video_downloader", False,
         "MLZj1OlPaq58-Bpv4CgeFvxSqCwiV03erzrn77MTrURu_17C3IREq7FPx86MIAiAMTQ9EzXWh9hVcnyUY7p_eZs"),
        ("insaver", "InSaver: Reels Downloader", "Instagram",
         "Download Reels, Stories, Threads & videos in HD. No watermark, no login.",
         "com.newagedevs.reels_video_downloader", False,
         "kdQ49cjLFNSu5fEN0z37KB6Vc3CTmvMBqmvW6xmy0gw3zt7AcoFWfV_ADDTKCKx-G2oKkoA-pa4hpY2UroGW"),
        ("threads-video-downloader", "Threads Video Downloader", "Threads",
         "Save Threads videos, photos & GIFs in one tap — fast, simple, no login.",
         "com.newagedevs.threads_video_downloader", False,
         "3hcagmNXQbYhssbBBCBzMbKYoE895e_xcyoRA-DHifx1WHsd3eB6CAyVPHGtS4Ec7CkbVjablPTZNV29Lz9z16g"),
        ("hd-video-downloader", "Hd Video Downloader", "Facebook",
         "Save Facebook videos, Reels & Stories in HD and 4K. Fast & easy.",
         "com.newagedevs.story_video_downloader", False,
         "46MRAnyGDr2E8D0KgSVAFwU5-Q6OmBrw8NZNZo0sBIqiILG8qLDLE0G3SIYtSq9DKtlf6NqBEd4KGB4NyxybHns"),
    ]),
    ("Tools", "Everyday utilities for audio, your phone, network, links, privacy and travel.", [
        ("sonary", "Sonary: MP3 & Noise Remover AI", "AI Audio",
         "Extract, convert, trim and merge audio. Remove vocals and noise with AI.",
         "com.newagedevs.sonary", True,
         "vdnVcvDwadlcJWssb0ru-UBiM0vjZWCmD0AJ08WuidTfhU89rJVTd0VnKrTb1r7-QB5ovLd5p0puUK4DIIpicg"),
        ("gesture-volume", "Gesture Volume: Edge Bar", "Accessibility",
         "Volume, brightness and a deck of tools, from one bar on your screen edge.",
         "com.newagedevs.gesturevolume", False,
         "4zmNR3loFQwTrgJ2ClMGP5ZjXV_0Tg-QfjbIwGxbkwxFGHrmSICBkEyyEj9G1JlcCyFudv5L0ZmHZgEeKV2yExw"),
        ("force-5g-lte", "Force 5G/LTE & Network Monitor", "Network",
         "Switch network mode: 5G only (NR), 4G LTE only, 3G or 2G — and monitor it.",
         "com.newagedevs.enable_network", False,
         "ymabFLg5tZTuyb0b6qp1LIgMvg9iS0O26L0gF9Xyq_CbrXJW7E1juLczONff9rGbdHo25Dmn6JSWJ0r0N35B"),
        ("temp-mail", "Temp Mail - Disposable Email", "Privacy",
         "Instant disposable email. No signup. Block spam & bots. Stay private.",
         "com.newagedevs.temp_mail", False,
         "mLpd6Y_65gUCpnyK4j8YBJeT2tSc7Ix7F3GAv2Ohze-vYMERkZgQBhjiMeERAp5VVsHbvO2jZVKSHCyeaaEA"),
        ("shortly", "Shortly: URL & Link Shortener", "Links & QR",
         "Shorten and expand URLs, create QR codes, and check links safely.",
         "com.newagedevs.url_shortener", False,
         "0dxWtNlPIGpfi0ibqJiYGZEkjNnBFuk85PbmFdM5UR4wwRgVNFiBAr6ofbZIAv6jNEnaR3Xae8H2krC-ZbkxaQ"),
        ("smart-route-bd", "Smart Route BD: Bus & Metro", "Travel",
         "Unofficial Dhaka transit guide: bus, metro, train & launch fares — offline.",
         "com.newage.bdbusroute", False,
         "I-p81AkneFZAdrVnVfefJgV4iPlJBr0EANG273NV5PEtMY1WV0XuVCgv69nwMVcyAjqvst00J78P-xFYsySXfA"),
    ]),
    ("Widgets & Games", "Home-screen widgets and casual games.", [
        ("couple-widgets", "Couple Widgets: Days Together", "Widget",
         "Count your days together with beautiful widgets you design yourselves.",
         "com.newagedevs.couplewidgets", False,
         "crxsJ7z2UvBDOdLLR0P8y76HEy4JF3xzzqur8YHxlvbc0VRmoD-Ujw81ecbDLgbW7WfhGyjUzqGhpfxK7oQC8w"),
        ("arrow-rush", "Arrow Rush: Untangle Puzzle", "Puzzle game",
         "Untangle a knot of arrows. Every tap counts. Hundreds of handcrafted levels.",
         "com.newagedevs.arrow_rush", True,
         "H9iTy3lTyoGcul_nTmz3NYceg8id7bNL1JXZzUbSkfzugPpUFd_xrsVIpg5nEwep4GoUKqJ1W2UvcIYd_f6H5WA"),
    ]),
]
APPS = [app for _, _, apps in GROUPS for app in apps]

# Pin-card look, github-stats-extended `theme=dark`.
PIN = dict(bg="#151515", border="#e4e2e2", title="#fff", text="#9f9f9f", icon="#79ff97",
           font="'Segoe UI', Ubuntu, Sans-Serif")

HERO_COVERS = [  # front -> back, store artwork from newagedevs.com
    ("facebook-video-downloader", -5.0),
    ("reels-video-downloader", -1.67),
    ("media-saver", 1.67),
    ("threads-video-downloader", 5.0),
]
HERO_SUBTITLE = [
    "I ship end-to-end solutions — Android, iOS & Flutter apps,",
    "web & backend systems, cloud and AI — plus polished in-house apps",
    "on Google Play & the App Store, trusted by over a million users.",
]
HERO_PLATFORMS = ["Android", "iOS", "Web", "Desktop", "AI"]
HERO_STATS = [("20+", "Total Projects"), ("13", "Published Apps"), ("50+", "Countries"),
              ("50K+", "Reviews"), ("1.6M+", "Downloads")]
HERO_FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
HERO_THEMES = {
    "light": dict(
        ink="#0B172C", muted="#4A5872", brand="#1B63D6", bg0="#FFFFFF", bg1="#EAF2FF", blob="#D6E6FF",
        blob2="#DDF7FA", wave="#E3EDFD", underline="#54DDE8", pill_bg="#E3EDFD", pill_fg="#1B4FA8",
        pill_stroke="#C9DBFA", tag_bg="#FFFFFF", tag_fg="#1F3355", tag_stroke="#D3E0F5", cover_stroke="#FFFFFF",
        shadow="#1B63D6", shadow_op=0.22, stat_bg="#FFFFFF", stat_stroke="#DCE6F5", divider="#E4ECF8",
        frame="#DCE6F5", stats=["#1B63D6", "#0F766E", "#6D3FD4", "#9A6207", "#C02B52"],
    ),
    "dark": dict(
        ink="#F2F6FC", muted="#A9B6CC", brand="#6EA8FF", bg0="#0B172C", bg1="#10264D", blob="#1B3F7A",
        blob2="#0F4A55", wave="#0E2141", underline="#54DDE8", pill_bg="#16305A", pill_fg="#BFD6FF",
        pill_stroke="#24467E", tag_bg="#122749", tag_fg="#DCE6F5", tag_stroke="#25416E", cover_stroke="#2A4677",
        shadow="#000000", shadow_op=0.45, stat_bg="#0F2142", stat_stroke="#23406E", divider="#1D355E",
        frame="#1D355E", stats=["#6EA8FF", "#2DD4BF", "#A78BFA", "#FBBF24", "#FB7185"],
    ),
}


# ---------------------------------------------------------------- helpers
def _font(names):
    dirs = ["C:/Windows/Fonts", "/System/Library/Fonts/Supplemental", "/Library/Fonts",
            "/usr/share/fonts/truetype/msttcorefonts", "/usr/share/fonts/truetype/liberation",
            "/usr/share/fonts/liberation-sans", "/usr/share/fonts/truetype/liberation2"]
    for d in dirs:
        for n in names:
            if os.path.exists(os.path.join(d, n)):
                return ImageFont.truetype(os.path.join(d, n), 100)
    raise SystemExit(f"Need Segoe UI, Arial or Liberation Sans to measure text (looked for {names})")


# Segoe UI first (the cards' primary font), then Arial-metric fallbacks.
REGULAR = _font(["segoeui.ttf", "arial.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"])
SEMIBOLD = _font(["seguisb.ttf", "arialbd.ttf", "Arial Bold.ttf", "LiberationSans-Bold.ttf"])
BOLD = _font(["segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "LiberationSans-Bold.ttf"])


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def width(s, size, weight=400, ls=0.0):
    font = BOLD if weight >= 700 else SEMIBOLD if weight >= 600 else REGULAR
    return font.getlength(s) * size / 100 + ls * len(s)


def text(x, y, s, size, fill, weight=400, anchor="start", ls=0.0, fit=None):
    """<text> pinned to its measured width, so the layout holds whatever font renders it."""
    w = width(s, size, weight, ls)
    if fit:
        w = min(w, fit)
    extra = (f' text-anchor="{anchor}"' if anchor != "start" else "") + (f' letter-spacing="{ls}"' if ls else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs"{extra}>{esc(s)}</text>')


def wrap(s, size, max_w, weight=400):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and width(trial, size, weight) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in c)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def data_uri(img, fmt="PNG", **kw):
    buf = io.BytesIO()
    img.save(buf, fmt, **kw)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def accent_of(img):
    """Dominant saturated colour of an icon, brightened to read as a dot on the dark card."""
    buckets = {}
    px = img.convert("RGBA").resize((48, 48)).load()
    for r, g, b, a in (px[x, y] for x in range(48) for y in range(48)):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if a > 200 and s > 0.35 and v > 0.35:
            buckets.setdefault(round(h * 24) % 24, []).append((r, g, b))
    if not buckets:
        return "#9f9f9f"
    pixels = max(buckets.values(), key=len)
    h, l, s = colorsys.rgb_to_hls(*(sum(c[i] for c in pixels) / len(pixels) / 255 for i in range(3)))
    return hexc([v * 255 for v in colorsys.hls_to_rgb(h, min(max(l, 0.55), 0.7), max(s, 0.6))])


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ---------------------------------------------------------------- app card
PHONE = ('<rect x="3.75" y="0.75" width="8.5" height="14.5" rx="1.75" fill="none" stroke="{c}" stroke-width="1.5"/>'
         '<circle cx="8" cy="12.25" r="1" fill="{c}"/>')


def app_card(app, icon_uri, accent):
    _slug, name, kind, desc, _pkg, ios, _key = app
    W, H = 400, 140
    title_x = 56
    size = 18
    while width(name, size, 600) > W - title_x - 25 and size > 15:
        size -= 0.5
    lines = wrap(desc, 13, W - 50)
    if len(lines) > 2:
        raise SystemExit(f"Description for {name!r} needs 3 lines; shorten it: {desc!r}")

    b = [f'<rect x="0.5" y="0.5" rx="4.5" width="{W - 1}" height="{H - 1}" fill="{PIN["bg"]}" stroke="{PIN["border"]}"/>',
         '<clipPath id="icon"><rect x="25" y="17.5" width="22" height="22" rx="5"/></clipPath>',
         f'<image x="25" y="17.5" width="22" height="22" clip-path="url(#icon)" href="{icon_uri}"/>',
         '<rect x="25.5" y="18" width="21" height="21" rx="4.5" stroke="#fff" stroke-opacity="0.18"/>',
         text(title_x, 35, name, size, PIN["title"], 600, fit=W - title_x - 25)]
    for i, line in enumerate(lines):
        b.append(text(25, 65.6 + i * 15.6, line, 13, PIN["text"]))

    # Footer row, laid out like the pin card's language / stars / forks.
    b.append(f'<circle cx="30" cy="115" r="6" fill="{accent}"/>')
    b.append(text(45, 120, kind, 12, PIN["text"]))
    x = 30 + 15 + width(kind, 12) + 25
    platforms = "Android · iOS" if ios else "Android"
    b.append(f'<g transform="translate({x:.1f} 108)">{PHONE.format(c=PIN["icon"])}</g>')
    b.append(text(x + 20, 120, platforms, 12, PIN["text"]))

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" '
            f'role="img" font-family="{PIN["font"]}">\n<title>{esc(name)}</title>\n<desc>{esc(desc)}</desc>\n'
            + "\n".join(b) + "\n</svg>\n")


# ---------------------------------------------------------------- hero
COVER_W, COVER_H = 330, 161


def hero(theme, covers):
    t = HERO_THEMES[theme]
    W, H, X = 1200, 600, 64
    b = ['<defs>',
         f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg0"]}"/>'
         f'<stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>',
         f'<radialGradient id="blob" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{t["blob"]}" stop-opacity="0.9"/>'
         f'<stop offset="1" stop-color="{t["blob"]}" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="blob2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{t["blob2"]}" stop-opacity="0.9"/>'
         f'<stop offset="1" stop-color="{t["blob2"]}" stop-opacity="0"/></radialGradient>',
         f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>',
         f'<clipPath id="card"><rect width="{COVER_W}" height="{COVER_H}" rx="16"/></clipPath>',
         f'<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" '
         f'stdDeviation="14" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"]}"/></filter>',
         f'<filter id="soft" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="8" '
         f'stdDeviation="12" flood-color="{t["shadow"]}" flood-opacity="{t["shadow_op"] * 0.5:.2f}"/></filter>',
         '</defs>',
         '<g clip-path="url(#frame)">',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         '<circle cx="980" cy="150" r="360" fill="url(#blob)"/>',
         '<circle cx="120" cy="560" r="300" fill="url(#blob2)"/>',
         f'<path d="M0 470C100 470 200 520 300 520S500 470 600 470 800 520 900 520 1100 470 1200 470V{H}H0Z" '
         f'fill="{t["wave"]}" opacity="0.7"/>',
         '</g>',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="{t["frame"]}"/>']

    eyebrow = "HI, I'M MD. IMAM HOSSAIN"
    b.append(f'<rect x="{X}" y="56" width="{width(eyebrow, 13, 700, 1.6) + 44:.0f}" height="32" rx="16" '
             f'fill="{t["pill_bg"]}" stroke="{t["pill_stroke"]}"/>')
    b.append(f'<circle cx="{X + 18}" cy="72" r="4" fill="{t["brand"]}"/>')
    b.append(text(X + 30, 77, eyebrow, 13, t["pill_fg"], 700, ls=1.6))

    hs = 52
    w3 = width("cloud & AI", hs, 800)
    b.append(text(X, 150, "Building software across", hs, t["ink"], 800))
    b.append(text(X, 214, "mobile, web,", hs, t["brand"], 800))
    b.append(f'<path d="M{X + 2} 294C{X + w3 * 0.3:.0f} 284 {X + w3 * 0.7:.0f} 284 {X + w3 - 2:.0f} 290" fill="none" '
             f'stroke="{t["underline"]}" stroke-width="7" stroke-linecap="round" opacity="0.9"/>')
    b.append(text(X, 278, "cloud & AI", hs, t["brand"], 800))
    b.append(text(X + w3 + 1, 278, ".", hs, t["ink"], 800))

    b.append(f'<rect x="{X}" y="320" width="3" height="76" rx="1.5" fill="{t["brand"]}"/>')
    for i, line in enumerate(HERO_SUBTITLE):
        if width(line, 17) > 590:
            raise SystemExit(f"Hero subtitle line too long, it would run into the covers: {line!r}")
        b.append(text(X + 20, 338 + i * 26, line, 17, t["muted"]))

    b.append(text(X, 438, "I build for", 13, t["muted"], 600))
    tx = X + width("I build for", 13, 600) + 14
    for p in HERO_PLATFORMS:
        w = width(p, 13, 700)
        b.append(f'<rect x="{tx:.1f}" y="417" width="{w + 26:.1f}" height="30" rx="15" fill="{t["tag_bg"]}" '
                 f'stroke="{t["tag_stroke"]}"/>')
        b.append(text(tx + 13, 437, p, 13, t["tag_fg"], 700))
        tx += w + 34

    for i in reversed(range(len(HERO_COVERS))):
        slug, rot = HERO_COVERS[i]
        b.append(f'<g transform="translate({712 + i * 32} {244 - i * 58}) rotate({rot} {COVER_W / 2} {COVER_H / 2})" '
                 f'filter="url(#shadow)">')
        b.append(f'<rect x="-3" y="-3" width="{COVER_W + 6}" height="{COVER_H + 6}" rx="19" fill="{t["cover_stroke"]}"/>')
        b.append(f'<image width="{COVER_W}" height="{COVER_H}" clip-path="url(#card)" '
                 f'preserveAspectRatio="xMidYMid slice" href="{covers[slug]}"/>')
        b.append('</g>')

    sx, sy, sw, sh = X, 470, W - 2 * X, 96
    b.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="20" fill="{t["stat_bg"]}" '
             f'stroke="{t["stat_stroke"]}" filter="url(#soft)"/>')
    cw = sw / len(HERO_STATS)
    for i, (val, label) in enumerate(HERO_STATS):
        mx = sx + cw * i + cw / 2
        if i:
            b.append(f'<line x1="{sx + cw * i:.1f}" y1="{sy + 22}" x2="{sx + cw * i:.1f}" y2="{sy + sh - 22}" '
                     f'stroke="{t["divider"]}" stroke-width="1.5"/>')
        b.append(text(mx, sy + 50, val, 34, t["stats"][i], 800, anchor="middle"))
        b.append(text(mx, sy + 74, label, 14, t["muted"], 500, anchor="middle"))

    title = "Hi, I'm Md. Imam Hossain — Building software across mobile, web, cloud & AI"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{esc(title)}" font-family="{HERO_FONT}">\n<title>{esc(title)}</title>\n'
            + "\n".join(b) + "\n</svg>\n")


# ---------------------------------------------------------------- README
def replace_block(readme, name, content):
    pattern = re.compile(rf"(<!-- {name}:start -->\n).*?(<!-- {name}:end -->)", re.S)
    if not pattern.search(readme):
        raise SystemExit(f"README.md is missing the <!-- {name}:start --> / <!-- {name}:end --> markers")
    return pattern.sub(lambda m: m.group(1) + content + "\n" + m.group(2), readme)


def main():
    covers = {}
    for slug, _ in HERO_COVERS:
        im = Image.open(io.BytesIO(fetch(f"https://newagedevs.com/media/app-covers/{slug}.webp"))).convert("RGB")
        covers[slug] = data_uri(im.resize((COVER_W * 2, COVER_H * 2), Image.LANCZOS), "JPEG", quality=82, optimize=True)
    for theme in HERO_THEMES:
        write(f"assets/hero-{theme}.svg", hero(theme, covers))

    for app in APPS:
        img = Image.open(io.BytesIO(fetch(f"https://play-lh.googleusercontent.com/{app[6]}=s128"))).convert("RGBA")
        write(f"assets/apps/{app[0]}.svg", app_card(app, data_uri(img.resize((66, 66), Image.LANCZOS)), accent_of(img)))

    sections = []
    for title, blurb, apps in GROUPS:
        platforms = ["Android"] + (["iOS"] if any(a[5] for a in apps) else [])
        tags = " ".join(f"`{tag}`" for tag in [f"{len(apps)} apps"] + platforms)
        # Same markup as the pin cards: one image link per line, so they flow two per row and stack on phones.
        cards = "\n".join(f"[![{a[1]}](assets/apps/{a[0]}.svg)]({PLAY}{a[4]})" for a in apps)
        sections.append(f"### {title}\n\n{tags} {blurb}\n\n{cards}")
    # Groups only set the order; the badges render as one left-aligned paragraph with no labels.
    stack = "\n".join(badge(*b) for _, badges in STACK for b in badges)
    with open(README, encoding="utf-8") as f:
        readme = replace_block(replace_block(f.read(), "apps", "\n\n".join(sections)), "stack", stack)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)


if __name__ == "__main__":
    main()
