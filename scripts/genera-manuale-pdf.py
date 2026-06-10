#!/usr/bin/env python3
# ============================================================================
# Genera il PDF impaginato del "Manuale di Protezione Civile" dalla STESSA
# fonte Hugo dei capitoli online (fonte unica di verità). Usa WeasyPrint sul
# rendering della pagina /manuale/versione-stampabile/ (layout stampa.html) +
# il foglio static/css/manuale-print.css (CSS Paged Media: numeri di pagina,
# testatine, indice). Niente browser, niente paged.js a runtime.
#
# Uso:
#   ~/.manuale-venv/bin/python scripts/genera-manuale-pdf.py
#       → build Hugo + http server locale + WeasyPrint → static/manuali/...
#   ~/.manuale-venv/bin/python scripts/genera-manuale-pdf.py --url URL
#       → usa un server già in ascolto (es. hugo server in dev), niente build
#
# Dipendenze: weasyprint (venv ~/.manuale-venv); per il build: hugo.
# ============================================================================
import os, sys, subprocess, functools, threading, time
import http.server, socketserver

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(REPO, "public")
OUT = os.path.join(REPO, "static", "manuali", "manuale-protezione-civile.pdf")
PRINT_PATH = "manuale/versione-stampabile/"
PORT = 8731


def ensure_fonts():
    """Installa Titillium Web (font AGID del portale) in ~/.fonts dai woff2 del
    repo, così le testatine del PDF sono coerenti in locale e in CI. Idempotente."""
    fonts_dir = os.path.expanduser("~/.fonts")
    src = os.path.join(REPO, "static/vendor/bootstrap-italia/fonts/Titillium_Web")
    installed = False
    pairs = (("regular", "TitilliumWeb-regular.ttf"), ("700", "TitilliumWeb-700.ttf"),
             ("italic", "TitilliumWeb-italic.ttf"))
    for w, dst in pairs:
        dstp = os.path.join(fonts_dir, dst)
        srcp = os.path.join(src, "titillium-web-v10-latin-ext_latin-%s.woff2" % w)
        if not os.path.exists(dstp) and os.path.exists(srcp):
            os.makedirs(fonts_dir, exist_ok=True)
            try:
                from fontTools.ttLib import TTFont
                t = TTFont(srcp); t.flavor = None; t.save(dstp); installed = True
            except Exception as e:
                print("· avviso font Titillium:", e)
    if installed:
        subprocess.run(["fc-cache", "-f", fonts_dir], capture_output=True)


def hugo_build():
    print("· Hugo build (baseURL locale)…", flush=True)
    subprocess.run(
        ["hugo", "--quiet", "--minify", "--baseURL", f"http://127.0.0.1:{PORT}/"],
        cwd=REPO, check=True,
    )


def serve(directory, port):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None  # silenzio
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render(url):
    from weasyprint import HTML
    print(f"· WeasyPrint ← {url}", flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    HTML(url).write_pdf(OUT)
    mb = os.path.getsize(OUT) / 1048576
    print(f"OK → {OUT} ({mb:.2f} MB)", flush=True)


def main():
    ensure_fonts()
    # Modalità "server già attivo"
    if "--url" in sys.argv:
        url = sys.argv[sys.argv.index("--url") + 1]
        render(url)
        return
    # Modalità autonoma: build + serve + render
    hugo_build()
    if not os.path.isdir(PUBLIC):
        sys.exit("public/ assente dopo il build")
    httpd = serve(PUBLIC, PORT)
    time.sleep(0.6)
    try:
        render(f"http://127.0.0.1:{PORT}/{PRINT_PATH}")
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
