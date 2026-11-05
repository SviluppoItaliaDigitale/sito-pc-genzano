"""Scarica le righe ElevenLabs da tuple (sessione, generazione, ora, firma) in riga_<k>.mp3 nella cartella corrente."""
import subprocess, sys, json
import os
W = os.environ["ELEVENLABS_WORKSPACE"]  # identificativo dello spazio di lavoro, dalla URL firmata
for i, (s, g, d, sig) in enumerate(json.load(open(sys.argv[1]))):
    u = (f"https://storage.googleapis.com/xi-backend/database/workspace/{W}/content_generation/{s}/{g}/content.mp3?X-Goog-Algorithm=GOOG4-RSA-SHA256"
         f"&X-Goog-Credential=xi-backend-prod%40xi-labs.iam.gserviceaccount.com%2F20261101%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20261101T{d}Z&X-Goog-Expires=7200&X-Goog-SignedHeaders=host&X-Goog-Signature={sig}")
    r = subprocess.run(["curl", "-sS", "-o", f"riga_{i}.mp3", "-w", "%{http_code} %{size_download}", u], capture_output=True, text=True); print(i, r.stdout)
