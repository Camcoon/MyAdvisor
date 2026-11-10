"""Measure computed contrast, including the actual AdminLTE/Bootstrap cascade.

Requires Node, a Chromium browser and the application's pinned CSS downloaded
to docs/assignment2/.browser-assets. Skips explicitly when tools are unavailable;
this automated template fixture is not a human UAT result.
"""
import base64
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("screen", ["advisor", "approved"])
def test_rendered_text_contrast_in_chromium(student_env, tmp_path, screen):
    node = shutil.which("node")
    browser = next((str(p) for p in [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path(shutil.which("chromium") or "/nonexistent-chromium"),
    ] if p.is_file()), None)
    assets = ROOT / "docs/assignment2/.browser-assets"
    if not node or not browser or not all((assets / f).is_file() for f in [
        "bootstrap.min.css", "adminlte.min.css"
    ]):
        pytest.skip("Contrast needs Node, Chromium and the pinned CSS assets; see correction report")
    env = student_env
    env.seed_plan(status="Pending" if screen == "advisor" else "Approved")
    client = env.login("a1" if screen == "advisor" else "s1")
    url = "/admin" if screen == "advisor" else "/app?tab=plan-courses"
    response = client.get(url)
    assert response.status_code == 200
    markup = re.sub(
        r"<script\b[^>]*>.*?</script>", "", response.text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    sources = []

    def stylesheet(match):
        tag = match.group(0)
        href = re.search(r'href="([^"]+)"', tag)
        if not href:
            return ""
        href = href.group(1)
        if "bootstrap@5.3.8/" in href:
            content = (assets / "bootstrap.min.css").read_bytes()
            expected = re.search(r'integrity="sha384-([^"]+)"', tag).group(1)
            assert base64.b64encode(hashlib.sha384(content).digest()).decode() == expected
        elif "admin-lte@4.10.0/" in href:
            content = (assets / "adminlte.min.css").read_bytes()
        elif "/static/css/app.css" in href:
            content = (ROOT / "app/static/css/app.css").read_bytes()
        else:
            return ""  # Fonts/icons cannot supply the audited table/notice colors.
        sources.append({"href": href, "sha256": hashlib.sha256(content).hexdigest()})
        return "<style>" + content.decode("utf-8") + "</style>"

    # Replace links in place to preserve the real stylesheet order/specificity.
    markup = re.sub(r"<link\b[^>]*>", stylesheet, markup, flags=re.IGNORECASE)
    html_path = tmp_path / f"contrast-{screen}.html"
    html_path.write_text(markup, encoding="utf-8")
    result = subprocess.run(
        [node, str(ROOT / "tests/browser/contrast_probe.cjs"), browser, str(html_path)],
        capture_output=True, text=True, timeout=35, check=False,
    )
    assert result.returncode == 0, result.stderr
    measured = json.loads(result.stdout)
    measured["stylesheets"] = sources
    samples = measured["normal"] + measured["hover"]
    assert samples
    if screen == "advisor":
        assert measured["hover"], "Actual hovered table state must be measured"
        assert any("Course COMP 2000" in item["text"] for item in samples)
    else:
        assert any(item["text"] == "This plan has been approved." for item in samples)
    # WCAG normal text threshold, measured from browser-computed foreground and
    # background (including the table's inset hover color), not CSS-string checks.
    assert all(item["ratio"] >= 4.5 for item in samples), samples
    print("CONTRAST_RESULT " + json.dumps({"screen": screen, **measured}))
