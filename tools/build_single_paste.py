"""Build home-single-paste.html from block1-html-js.html + block2.css.

Layout of the output (one paste into a GHL Custom JS/HTML element):
  1. <script> settings (BOOKING_URL, LOGO_URL) - kept separate so a typo here
     can't stop the styles from loading
     <script> styles injected into <head>
  2. the page markup (#ghl-dummy)
  3. <script> page behaviour
The styles go in first so the page never shows unstyled.

Run: python3 tools/build_single_paste.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html = (root / "block1-html-js.html").read_text()
css = (root / "block2.css").read_text()

markup, script = html.split("<script>\n", 1)
start = script.index("// ============================================================\n// REQUIRED: PASTE YOUR BOOKING")
logo_line = script.index("var LOGO_URL = ")
end = script.index("\n", logo_line) + 1
settings, script = script[start:end], script[:start] + script[end:]
assert "`" not in css and "${" not in css

head_script = f"""<script>
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
out = (
    "<!-- ===== START: Rip & Roll Turf HOME page (copy everything down to the END line) ===== -->\n"
    + head_script
    + markup.rstrip("\n") + "\n\n<script>\n" + script.lstrip("\n").rstrip("\n")
    + "\n<!-- ===== END: Rip & Roll Turf HOME page ===== -->\n"
)
(root / "home-single-paste.html").write_text(out)
print("home-single-paste.html:", out.count("\n"), "lines")
