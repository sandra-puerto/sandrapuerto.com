# ============================================================================
# LANDING-SGPT — (minify.py)
# Stratum Consumer Pattern
# ============================================================================
#
# Component ......... landing-sgpt
# Function .......... Utility script for minifying static assets locally.
# Warning ........... Use with caution. Custom regex minification is basic
#                     and can sometimes break complex JS/CSS syntax.
# ============================================================================

import os
import re

def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css)
    return css.strip()

def minify_js(js):
    # Fix: Use a negative lookbehind to avoid stripping 'http://' or 'https://'
    js = re.sub(r'(?<!:)//.*', '', js)
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'\s+', ' ', js)
    return js.strip()

def minify_html(html):
    html = re.sub(r'<!--(?!>).*?-->', '', html, flags=re.DOTALL)
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()

base_dir = r"c:\Users\sandra.puerto\opt\landing-sgpt\public"

# Minify CSS
css_path = os.path.join(base_dir, 'css', 'styles.css')
if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    minified = minify_css(content)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    print("styles.css minified.")

# Minify JS
js_path = os.path.join(base_dir, 'js', 'app.js')
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    minified = minify_js(content)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    print("app.js minified.")

# Minify HTML files
for file_name in ['index.html', '404.html', 'maintenance.html']:
    html_path = os.path.join(base_dir, file_name)
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        minified = minify_html(content)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(minified)
        print(f"{file_name} minified.")
