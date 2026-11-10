/* Encoder GIF89a minimale, ECMAScript 2018, senza dipendenze.
   Usato solo per scaricare l'animazione della cartina meteo. */
(function (root) {
  'use strict';

  function lzw(indices, minCodeSize) {
    var clear = 1 << minCodeSize;
    var eoi = clear + 1;
    var codeSize = minCodeSize + 1;
    var nextCode = eoi + 1;
    var maxCode = (1 << codeSize) - 1;
    var dict = new Uint16Array(4096 * 256);
    var used = new Uint8Array(4096 * 256);
    var gen = 1;
    var outBytes = [];
    var buf = 0;
    var bufBits = 0;

    function emit(code) {
      buf |= (code << bufBits);
      bufBits += codeSize;
      while (bufBits >= 8) {
        outBytes.push(buf & 255);
        buf >>= 8;
        bufBits -= 8;
      }
    }
    function resetDict() {
      gen++;
      if (gen > 250) {
        used = new Uint8Array(4096 * 256);
        gen = 1;
      }
      codeSize = minCodeSize + 1;
      nextCode = eoi + 1;
      maxCode = (1 << codeSize) - 1;
    }

    emit(clear);
    var w = indices[0];
    var i, k, key, trovato;
    for (i = 1; i < indices.length; i++) {
      k = indices[i];
      key = (w << 8) + k;
      trovato = used[key] === gen;
      if (trovato) {
        w = dict[key];
      } else {
        emit(w);
        if (nextCode < 4096) {
          used[key] = gen;
          dict[key] = nextCode;
          nextCode++;
          /* Il codice appena assegnato (nextCode-1) deve ancora
             usare la larghezza corrente; si allarga solo dopo. */
          if (nextCode - 1 >= (1 << codeSize) && codeSize < 12) {
            codeSize++;
            maxCode = (1 << codeSize) - 1;
          }
        } else {
          emit(clear);
          resetDict();
        }
        w = k;
      }
    }
    emit(w);
    emit(eoi);
    if (bufBits > 0) outBytes.push(buf & 255);
    return outBytes;
  }

  function packBlocks(bytes) {
    var out = [];
    var i = 0;
    while (i < bytes.length) {
      var n = Math.min(255, bytes.length - i);
      out.push(n);
      for (var j = 0; j < n; j++) out.push(bytes[i + j]);
      i += n;
    }
    out.push(0);
    return out;
  }

  function quantize(frames, w, h, maxColors) {
    var counts = {};
    var f, p, r, g, b, key, i, n = w * h;
    for (f = 0; f < frames.length; f++) {
      var data = frames[f].data;
      for (i = 0; i < n; i++) {
        p = i * 4;
        r = data[p] >> 3 << 3;
        g = data[p + 1] >> 3 << 3;
        b = data[p + 2] >> 3 << 3;
        key = (r << 16) | (g << 8) | b;
        counts[key] = (counts[key] || 0) + 1;
      }
    }
    var keys = [];
    for (key in counts) {
      if (Object.prototype.hasOwnProperty.call(counts, key)) {
        keys.push({ c: Number(key), n: counts[key] });
      }
    }
    keys.sort(function (a, b) { return b.n - a.n; });
    var palette = [];
    var map = {};
    var take = Math.min(maxColors, keys.length);
    for (i = 0; i < take; i++) {
      var c = keys[i].c;
      var rgb = [c >> 16, (c >> 8) & 255, c & 255];
      palette.push(rgb);
      map[c] = i;
    }
    while (palette.length < 4) palette.push([0, 0, 0]);
    var size = 2;
    while ((1 << size) < palette.length && size < 8) size++;
    var full = 1 << size;
    while (palette.length < full) palette.push([0, 0, 0]);
    return { palette: palette, map: map, size: size };
  }

  function nearest(palette, r, g, b) {
    var best = 0, bestD = 1e15, i, d, p;
    for (i = 0; i < palette.length; i++) {
      p = palette[i];
      d = (p[0] - r) * (p[0] - r) + (p[1] - g) * (p[1] - g) + (p[2] - b) * (p[2] - b);
      if (d < bestD) { bestD = d; best = i; }
    }
    return best;
  }

  function encode(width, height, frames, delayCs, loop) {
    var q = quantize(frames, width, height, 256);
    var palette = q.palette;
    var map = q.map;
    var palSize = q.size;
    var bytes = [];
    function u8(v) { bytes.push(v & 255); }
    function u16(v) { bytes.push(v & 255, (v >> 8) & 255); }
    function str(s) { for (var i = 0; i < s.length; i++) bytes.push(s.charCodeAt(i)); }

    str('GIF89a');
    u16(width); u16(height);
    u8(0x80 | 0x70 | (palSize - 1));
    u8(0);
    u8(0);
    var i;
    for (i = 0; i < palette.length; i++) {
      u8(palette[i][0]); u8(palette[i][1]); u8(palette[i][2]);
    }

    // Netscape loop
    u8(0x21); u8(0xFF); u8(11);
    str('NETSCAPE2.0');
    u8(3); u8(1); u16(typeof loop === 'number' ? loop : 0); u8(0);

    var cacheNear = {};
    for (var f = 0; f < frames.length; f++) {
      var data = frames[f].data;
      var delay = frames[f].delay || delayCs || 25;
      var indices = new Array(width * height);
      var pix, r, g, b, key, idx, packed;
      for (pix = 0; pix < width * height; pix++) {
        i = pix * 4;
        r = data[i]; g = data[i + 1]; b = data[i + 2];
        packed = ((r >> 3) << 3 << 16) | ((g >> 3) << 3 << 8) | ((b >> 3) << 3);
        if (map[packed] !== undefined) {
          indices[pix] = map[packed];
        } else {
          key = (r << 16) | (g << 8) | b;
          if (cacheNear[key] === undefined) cacheNear[key] = nearest(palette, r, g, b);
          indices[pix] = cacheNear[key];
        }
      }
      u8(0x21); u8(0xF9); u8(4);
      u8(0x00);
      u16(delay);
      u8(0);
      u8(0);
      u8(0x2C);
      u16(0); u16(0); u16(width); u16(height);
      u8(0);
      var minCode = palSize < 2 ? 2 : palSize;
      u8(minCode);
      var compressed = lzw(indices, minCode);
      var blocks = packBlocks(compressed);
      for (i = 0; i < blocks.length; i++) u8(blocks[i]);
    }
    u8(0x3B);
    return new Uint8Array(bytes);
  }

  root.CMI_GIF = { encode: encode };
})(typeof window !== 'undefined' ? window : this);
