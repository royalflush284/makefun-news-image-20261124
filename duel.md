# Duel varian internal — Final 1, NI24 build v2

## Varian A (cream number strip, black/red scenes alternate)
- 264.429 byte (sesudah perbaikan kartu), 1024x1024, IHDR OK.
- Strip angka berbingkai merah di atas krem — kontras sedang.

## Varian B (black number strip, scenes alternate terbalik) — PEMENANG
- 260.160 byte, 1024x1024, IHDR OK.
- Strip angka hitam dengan angka krem — kontras paling kuat di seluruh
  halaman; lead 1 (Gaza) berlatar merah terbaca lebih bersih.
- Dipilih sebagai entry.png (sha256
  a63df2a67631a23de2ff3aa51d1dbaf79c575f68c3d693a253ec6fe4e5c1129e).

## Perbaikan dari ronde render pertama
- Kartu mini: deck/headline dipangkas ke maks 2 baris (clamp + elipsis),
  mini_h 350 -> 400, total H 4400 -> 4600 — tidak ada lagi teks yang
  menabrak garis chip/tag.
- DATE CHECK: jarak item 58 -> 50 px, baris penutup tidak lagi menabrak
  item ke-8.
- ALSO ON: brief dipadatkan ke 1 baris (21 brief, 16-36) — footer kini
  tampil utuh.
- Kata segar: 31/31 frasa ni24-fresh.txt hadir di teks halaman
  (freshcheck-final1.py), sesudah menambah "Kyiv strikes", "Antalya Pact",
  "Iran sanctions", "Kraken", "Pochettino", "Solana", "UN AI weapons",
  "Miley Cyrus" sebagai fakta, bukan tempelan.

## Uji baca 300 px
- Masthead, tanggal, headline lead dan struktur halaman terbaca; tidak ada
  teks garble. Teks isi kecil pada skala 300 px — wajar untuk halaman
  koran padat (genre yang sama dengan Top 1-3 NI22).
