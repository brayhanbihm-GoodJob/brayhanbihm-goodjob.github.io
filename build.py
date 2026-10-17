# Genera el sitio estático de Good Job a partir del aviso legal (una página por documento).
import re, os, sys
SRC = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(__file__))
s = open(SRC, encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", s, re.S).group(0)
font = re.search(r'<link rel="stylesheet"[^>]*>', s).group(0)
footer = re.search(r"<footer>.*?</footer>", s, re.S).group(0)
sec = {m.group(1): m.group(2).strip() for m in re.finditer(r'<section id="([^"]+)">(.*?)</section>', s, re.S)}
PAGES = [("aviso-de-privacidad", "privacidad", "Aviso de privacidad"),
         ("terminos", "terminos", "Términos de uso"),
         ("borrar-cuenta", "borrar-cuenta", "Borrar mi cuenta")]
extra = "<style>nav a[aria-current]{background:var(--fg);color:var(--bg)}a.home{color:inherit;text-decoration:none}</style>"
def page(title, body, current, depth):
    up = "../" * depth
    nav = "".join(f'<a href="{up}{slug}/"' + (' aria-current="page"' if slug == current else "") + f">{label}</a>"
                  for slug, _, label in PAGES)
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Good Job</title>
<meta name="description" content="Good Job: trabajos y oficios. {title}.">
{font}
{style}
{extra}
</head><body><div class="wrap">
<header>
  <p class="brand"><a class="home" href="{up or './'}">Good Job</a></p>
  <p class="sub">Trabajos y oficios cerca de ti.</p>
  <nav aria-label="Documentos">{nav}</nav>
</header>
{body}
{footer}
</div></body></html>
"""
for slug, sid, label in PAGES:
    body = sec[sid]
    for s2, i2, _ in PAGES: body = body.replace(f'href="#{i2}"', f'href="../{s2}/"')
    os.makedirs(os.path.join(OUT, slug), exist_ok=True)
    open(os.path.join(OUT, slug, "index.html"), "w", encoding="utf-8").write(
        page(label, f'<section id="{sid}">\n{body}\n</section>', slug, 1))
home = """<section><h2>Good Job: trabajos y oficios</h2>
<p>Conecta a clientes con trabajadores de oficios y empresas de servicios cerca de ellos. Publica lo que necesitas, recibe propuestas y elige con quién trabajar.</p>
<p><a href="https://play.google.com/store/apps/details?id=mx.goodjob.servicios">Descargar en Google Play</a></p>
<h3>Documentos</h3>
<ul><li><a href="aviso-de-privacidad/">Aviso de privacidad</a></li><li><a href="terminos/">Términos de uso</a></li><li><a href="borrar-cuenta/">Borrar mi cuenta</a></li></ul>
<h3>Contacto</h3><p><a href="mailto:goodjob.support@gmail.com">goodjob.support@gmail.com</a></p></section>"""
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page("Inicio", home, "", 0))
nf = '<section><h2>Página no encontrada</h2><p><a href="/">Ir al inicio de Good Job</a></p></section>'
html404 = page("No encontrada", nf, "", 0)
for slug, _, _ in PAGES: html404 = html404.replace(f'href="{slug}/"', f'href="/{slug}/"')
html404 = html404.replace('href="./"', 'href="/"')
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(html404)
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("ok")
