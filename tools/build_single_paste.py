"""Build the single-paste files for each page.

Sources:
  block1-html-js.html  Home markup + the shared settings and script
  block2.css           shared styles for every page
  pages/<name>.html    markup for the other pages (nav, sections, footer)

Each output file (one paste into a GHL Custom JS/HTML element) is laid out as:
  1. <script> settings (BOOKING_URL, LOGO_URL, CALENDAR_URL) - kept separate so a typo here
     can't stop the styles from loading
  2. <script> styles injected into <head>
  3. the page markup (#ghl-dummy)
  4. <script> page behaviour
The styles go in first so the page never shows unstyled.

Run: python3 tools/build_single_paste.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
home = (root / "block1-html-js.html").read_text()
css = (root / "block2.css").read_text()
assert "`" not in css and "${" not in css

home_markup, script = home.split("<script>\n", 1)
start = script.index("// ============================================================\n// REQUIRED: PASTE YOUR BOOKING")
logo_line = script.index("var CALENDAR_URL = ")
end = script.index("\n", logo_line) + 1
settings, script = script[start:end], script[:start] + script[end:]

head_scripts = f"""<script>
{settings}</script>

<script>
// ---------- Page styles (added by the script so the page builder can't strip them) ----------
(function () {{
  if (document.getElementById('ghl-dummy-css')) return;
  var css = `
{css}`;
  var s = document.createElement('style');
  s.id = 'ghl-dummy-css';
  s.textContent = css;
  (document.head || document.documentElement).appendChild(s);
}})();
</script>

"""


def build(markup: str, label: str, out_name: str) -> None:
    out = (
        f"<!-- ===== START: Rip & Roll Turf {label} page (copy everything down to the END line) ===== -->\n"
        + head_scripts
        + markup.rstrip("\n") + "\n\n<script>\n" + script.lstrip("\n").rstrip("\n")
        + f"\n<!-- ===== END: Rip & Roll Turf {label} page ===== -->\n"
    )
    (root / out_name).write_text(out)
    print(f"{out_name}: {out.count(chr(10))} lines")


build(home_markup, "HOME", "home-single-paste.html")
build((root / "pages" / "about.html").read_text(), "ABOUT", "about-single-paste.html")
build((root / "pages" / "contact.html").read_text(), "CONTACT", "contact-single-paste.html")
