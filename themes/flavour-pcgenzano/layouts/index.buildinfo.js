window.SITE_BUILD_TIME = "{{ now.Format "2006-01-02T15:04:05Z07:00" }}";
{{- /* SHA della stessa build (audit 25/09/2026, F19): verifica-fingerprint-live.sh
   lo confronta con la meta pc-build-sha delle pagine. Senza, un deploy che
   aggiornasse questo file ma nessun HTML campione farebbe sembrare fresco un
   sito le cui pagine sono tutte ferme alla build precedente. */}}
window.SITE_BUILD_SHA = "{{ with site.Data.buildinfo }}{{ .sha }}{{ end }}";
