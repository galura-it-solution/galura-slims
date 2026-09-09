#!/usr/bin/env python3
"""
Galura SLiMS E-Book Sample PDF Generator
Generates realistic, professional 3-page sample PDF files for digital ebooks.
Each PDF contains:
  Page 1: Book Cover, Title, Full RDA/SLiMS Catalog Metadata Box, and Detailed Synopsis
  Page 2: Comprehensive Table of Contents (Daftar Isi Sample)
  Page 3: Chapter 1 Reading Excerpt (Cuplikan Naskah Asli) & Library Access Note
"""

import os

def escape_pdf(s):
    if not s:
        return ""
    return str(s).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\")

def wrap_text(text, max_chars=75):
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for w in words:
        if current_len + len(w) + 1 <= max_chars:
            current_line.append(w)
            current_len += len(w) + 1
        else:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

class MultiPagePDF:
    def __init__(self):
        self.pages_content = []

    def add_page(self, content):
        self.pages_content.append(content)

    def generate(self):
        num_pages = len(self.pages_content)
        stream_ids = []
        page_ids = []
        curr_obj = 6

        for i in range(num_pages):
            stream_ids.append(curr_obj)
            page_ids.append(curr_obj + 1)
            curr_obj += 2

        objects = {}
        objects[1] = "<< /Type /Catalog /Pages 2 0 R >>"
        kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
        objects[2] = f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>"
        objects[3] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        objects[4] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        objects[5] = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>"

        for i, content in enumerate(self.pages_content):
            sid = stream_ids[i]
            pid = page_ids[i]
            stream_bytes = content.encode("latin1")
            objects[sid] = f"<< /Length {len(stream_bytes)} >>\nstream\n{content}\nendstream"
            objects[pid] = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {sid} 0 R /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> >>"

        buf = bytearray()
        buf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        total_objs = len(objects)
        offsets = [0] * (total_objs + 1)

        for oid in range(1, total_objs + 1):
            offsets[oid] = len(buf)
            buf.extend(f"{oid} 0 obj\n".encode("latin1"))
            buf.extend(objects[oid].encode("latin1"))
            buf.extend(b"\nendobj\n")

        xref_pos = len(buf)
        buf.extend(f"xref\n0 {total_objs + 1}\n".encode("latin1"))
        buf.extend(b"0000000000 65535 f \n")
        for oid in range(1, total_objs + 1):
            buf.extend(f"{offsets[oid]:010d} 00000 n \n".encode("latin1"))

        buf.extend(f"trailer\n<< /Size {total_objs + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin1"))
        return bytes(buf)

def build_ebook_pdf(eb):
    doc = MultiPagePDF()
    title = eb["title"]
    subtitle = eb.get("subtitle", "")
    author = eb["author"]
    editor = eb.get("editor", "Tim Redaksi Galura Media")
    publisher = eb["publisher"]
    year = eb["year"]
    isbn = eb["isbn"]
    call_num = eb["call_number"]
    ddc = eb["ddc"]
    category = eb["category"]
    series = eb.get("series", "Seri Pustaka Digital Galura")
    pages_info = eb.get("pages_info", "xxviii, 482 halaman")
    synopsis1 = eb["synopsis1"]
    synopsis2 = eb["synopsis2"]
    chapters = eb["chapters"]
    excerpt_heading = eb.get("excerpt_heading", "Bab 1: Pendahuluan & Prinsip Dasar")
    excerpt_text1 = eb["excerpt_text1"]
    excerpt_text2 = eb["excerpt_text2"]

    # ==========================================
    # PAGE 1: COVER, CATALOG METADATA & SYNOPSIS
    # ==========================================
    p1 = f"""
% Header Background Band
0.08 0.18 0.36 rg
0 730 612 62 re f

% Header Text
1 1 1 rg
BT /F2 14 Tf 45 765 Td (PERPUSTAKAAN DIGITAL GALURA - E-BOOK REPOSITORY) Tj
/F1 9 Tf 0 -16 Td (Koleksi Buku Elektronik Resmi Berstandar RDA | Akses Terbuka Perpustakaan) Tj
ET

% Title & Subtitle
0.1 0.1 0.1 rg
BT /F2 16 Tf 45 695 Td ({escape_pdf(title[:60])}) Tj
ET
"""
    if len(title) > 60:
        p1 += f"""
BT /F2 15 Tf 45 675 Td ({escape_pdf(title[60:125])}) Tj ET
"""
        y_sub = 655
    else:
        y_sub = 675

    p1 += f"""
0.2 0.3 0.4 rg
BT /F3 11 Tf 45 {y_sub} Td ({escape_pdf(subtitle)}) Tj ET

% Metadata Box Frame
0.82 0.86 0.92 rg
45 425 522 210 re f
0.3 0.45 0.65 RG
1 w
45 425 522 210 re S

% Metadata Box Header
0.15 0.28 0.52 rg
45 615 522 20 re f
1 1 1 rg
BT /F2 10 Tf 55 621 Td (KATALOGISASI DALAM TERBITAN (KDT) / BIBLIOGRAPHIC METADATA) Tj ET

% Metadata Fields
0.1 0.1 0.1 rg
BT /F2 9 Tf 55 595 Td (Penulis Utama    :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(author)}) Tj ET
BT /F2 9 Tf 55 577 Td (Editor / Redaksi :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(editor)}) Tj ET
BT /F2 9 Tf 55 559 Td (Penerbit & Tahun :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(publisher)} ({year})) Tj ET
BT /F2 9 Tf 55 541 Td (Nomor ISBN / e-ISBN :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(isbn)}) Tj ET
BT /F2 9 Tf 55 523 Td (Nomor Panggil (Call) :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(call_num)}  [Klasifikasi DDC: {ddc}]) Tj ET
BT /F2 9 Tf 55 505 Td (Subjek / Kategori:) Tj /F1 9 Tf 90 0 Td ({escape_pdf(category)}) Tj ET
BT /F2 9 Tf 55 487 Td (Seri Publikasi   :) Tj /F1 9 Tf 90 0 Td ({escape_pdf(series)}) Tj ET
BT /F2 9 Tf 55 469 Td (Deskripsi Fisik  :) Tj /F1 9 Tf 90 0 Td (1 File PDF ({pages_info} : ilus. ; 25 cm)) Tj ET
BT /F2 9 Tf 55 451 Td (Aksesibilitas    :) Tj /F2 9 Tf 90 0 Td (Hak Cipta Digital - Akses Terbuka Pemustaka (Public Open Access)) Tj ET
BT /F2 9 Tf 55 433 Td (Bahasa & Format  :) Tj /F1 9 Tf 90 0 Td (Bahasa Indonesia | Format PDF Digital (High Resolution Text)) Tj ET

% Synopsis Section
0.08 0.18 0.36 rg
BT /F2 12 Tf 45 400 Td (RINGKASAN & SINOPSIS EKSEKUTIF BUKU) Tj ET
0.7 0.7 0.7 RG 0.8 w 45 392 m 567 392 l S

% Synopsis Paragraph 1
0.15 0.15 0.15 rg
"""
    y_text = 376
    for line in wrap_text(synopsis1, 88):
        p1 += f"BT /F1 9 Tf 45 {y_text} Td ({escape_pdf(line)}) Tj ET\n"
        y_text -= 14

    y_text -= 6
    # Synopsis Paragraph 2
    for line in wrap_text(synopsis2, 88):
        p1 += f"BT /F1 9 Tf 45 {y_text} Td ({escape_pdf(line)}) Tj ET\n"
        y_text -= 14

    # Page 1 Footer
    p1 += f"""
0.92 0.94 0.97 rg 0 0 612 40 re f
0.6 0.6 0.6 RG 0.5 w 0 40 m 612 40 l S
0.3 0.3 0.3 rg
BT /F1 8 Tf 45 18 Td (SLiMS Galura E-Book Repository | {escape_pdf(title[:45])} | e-ISBN: {isbn}) Tj
/F2 8 Tf 440 0 Td (Halaman 1 dari 3) Tj
ET
"""
    doc.add_page(p1)

    # ==========================================
    # PAGE 2: TABLE OF CONTENTS (DAFTAR ISI)
    # ==========================================
    p2 = f"""
% Header Background Band
0.08 0.18 0.36 rg
0 730 612 62 re f

1 1 1 rg
BT /F2 14 Tf 45 765 Td (DAFTAR ISI LENGKAP BUKU (TABLE OF CONTENTS)) Tj
/F1 9 Tf 0 -16 Td ({escape_pdf(title[:70])} - {author}) Tj
ET

0.1 0.1 0.1 rg
BT /F2 12 Tf 45 690 Td (STRUKTUR BAB & SUB-BAHASAN MATERI) Tj ET
0.7 0.7 0.7 RG 0.8 w 45 682 m 567 682 l S

% Table of Contents Items
0.15 0.15 0.15 rg
BT /F2 10 Tf 45 660 Td (Bagian Awal: Prakata & Pengantar Penerbit) Tj /F1 9 Tf 420 0 Td (v - viii) Tj ET
BT /F2 10 Tf 45 642 Td (Lembar Hak Cipta & Standar Lisensi Digital) Tj /F1 9 Tf 420 0 Td (ix) Tj ET
"""
    y_ch = 618
    for ch in chapters:
        ch_title = ch["title"]
        ch_pages = ch["pages"]
        subs = ch.get("subs", [])
        p2 += f"""
BT /F2 9.5 Tf 45 {y_ch} Td ({escape_pdf(ch_title)}) Tj /F1 9 Tf 420 0 Td ({escape_pdf(ch_pages)}) Tj ET
"""
        y_ch -= 15
        for sub in subs:
            p2 += f"""
BT /F1 8.5 Tf 60 {y_ch} Td (- {escape_pdf(sub)}) Tj ET
"""
            y_ch -= 13
        y_ch -= 5

    p2 += f"""
BT /F2 10 Tf 45 {y_ch} Td (Glosarium Istilah & Indeks Subjek Teknis) Tj /F1 9 Tf 420 0 Td (hlm. 450) Tj ET
BT /F2 10 Tf 45 {y_ch - 18} Td (Daftar Pustaka & Rujukan Standar Industri) Tj /F1 9 Tf 420 0 Td (hlm. 465) Tj ET

% Info Box Bottom
0.94 0.96 0.98 rg 45 60 522 65 re f
0.4 0.55 0.75 RG 1 w 45 60 522 65 re S
0.1 0.2 0.4 rg
BT /F2 9.5 Tf 55 105 Td (Petunjuk Pembaca Digital Perpustakaan Galura SLiMS:) Tj
/F1 8.5 Tf 0 -16 Td (Daftar isi ini menyajikan sistematika pembahasan utuh yang terdapat dalam edisi cetak dan digital.) Tj
0 -13 Td (Pembaca dapat langsung meloncat ke bab materi tertentu menggunakan fitur navigasi PDF viewer SLiMS.) Tj
ET

% Page 2 Footer
0.92 0.94 0.97 rg 0 0 612 40 re f
0.6 0.6 0.6 RG 0.5 w 0 40 m 612 40 l S
0.3 0.3 0.3 rg
BT /F1 8 Tf 45 18 Td (SLiMS Galura E-Book Repository | {escape_pdf(title[:45])} | Daftar Isi) Tj
/F2 8 Tf 440 0 Td (Halaman 2 dari 3) Tj
ET
"""
    doc.add_page(p2)

    # ==========================================
    # PAGE 3: READING EXCERPT (CUPLIKAN MATERI)
    # ==========================================
    p3 = f"""
% Header Background Band
0.08 0.18 0.36 rg
0 730 612 62 re f

1 1 1 rg
BT /F2 14 Tf 45 765 Td (CUPLIKAN MATERI BUKU: SAMPLE CHAPTER) Tj
/F1 9 Tf 0 -16 Td ({escape_pdf(title[:70])} - {author}) Tj
ET

0.1 0.1 0.1 rg
BT /F2 13 Tf 45 690 Td ({escape_pdf(excerpt_heading)}) Tj ET
0.7 0.7 0.7 RG 0.8 w 45 680 m 567 680 l S

0.15 0.15 0.15 rg
"""
    y_ex = 660
    for line in wrap_text(excerpt_text1, 88):
        p3 += f"BT /F1 9 Tf 45 {y_ex} Td ({escape_pdf(line)}) Tj ET\n"
        y_ex -= 14

    y_ex -= 10
    for line in wrap_text(excerpt_text2, 88):
        p3 += f"BT /F1 9 Tf 45 {y_ex} Td ({escape_pdf(line)}) Tj ET\n"
        y_ex -= 14

    p3 += f"""
% Library Service Box
0.90 0.95 0.92 rg 45 80 522 95 re f
0.2 0.55 0.35 RG 1.2 w 45 80 522 95 re S
0.1 0.3 0.2 rg
BT /F2 10.5 Tf 55 155 Td (LAYANAN PEMINJAMAN E-BOOK RESMI PERPUSTAKAAN GALURA) Tj
/F1 9 Tf 0 -18 Td (Naskah di atas adalah sampel cuplikan resmi dari repositori Perpustakaan Digital Galura SLiMS.) Tj
0 -14 Td (Pemustaka terdaftar dapat meminjam atau membaca edisi digital lengkap melalui portal OPAC SLiMS) Tj
0 -14 Td (atau mengajukan permohonan melalui layanan sirkulasi perpustakaan: https://slims-ebook.galura.id) Tj
ET

% Page 3 Footer
0.92 0.94 0.97 rg 0 0 612 40 re f
0.6 0.6 0.6 RG 0.5 w 0 40 m 612 40 l S
0.3 0.3 0.3 rg
BT /F1 8 Tf 45 18 Td (SLiMS Galura E-Book Repository | {escape_pdf(title[:45])} | Cuplikan Materi) Tj
/F2 8 Tf 440 0 Td (Halaman 3 dari 3) Tj
ET
"""
    doc.add_page(p3)

    return doc.generate()


ebooks_catalog = [
    {
        "file": "microservices_cloud_native.pdf",
        "title": "Arsitektur Microservices & Cloud-Native: Desain, Pola, dan Implementasi Produksi Skala Besar",
        "subtitle": "Panduan Praktik Terbaik Orkestrasi Container, Event-Driven Architecture, dan Resiliensi Sistem",
        "author": "Martin Fowler, Chris Richardson",
        "editor": "Dr. Ir. Rian Pratama, M.Sc.",
        "publisher": "Galura Tech Publishing bekerjasama dengan O Reilly Media",
        "year": "2024",
        "isbn": "978-623-01-3890-5",
        "call_number": "EB 004.678 FOW a",
        "ddc": "004.678",
        "category": "Cloud Architecture & Microservices",
        "series": "Seri Arsitektur Cloud & Rekayasa Perangkat Lunak Modern; Jilid 1",
        "pages_info": "xxviii, 482 halaman",
        "synopsis1": "Buku ini menyajikan rujukan paling komprehensif bagi arsitek perangkat lunak dan insinyur senior yang hendak merancang, memigrasikan, dan mengoperasikan ekosistem microservices pada skala produksi tinggi. Dimulai dari identifikasi batas-batas kontekstual (bounded contexts) Domain-Driven Design hingga implementasi pola Saga untuk transaksi terdistribusi.",
        "synopsis2": "Dilengkapi studi kasus nyata implementasi orkestrasi container menggunakan Kubernetes, streaming data asinkron Apache Kafka, service mesh Istio, API gateway Envoy, serta metrik observabilitas terintegrasi OpenTelemetry, Prometheus, dan Grafana.",
        "chapters": [
            {"title": "Bab 1: Evolusi Monolitik Menuju Arsitektur Microservices", "pages": "hlm. 1 - 58", "subs": ["Prinsip Dekomposisi Layanan", "Anti-Pattern Distribusi Monolit", "Kriteria Evaluasi Arsitektur"]},
            {"title": "Bab 2: Desain Domain & Bounded Contexts Terdistribusi", "pages": "hlm. 59 - 134", "subs": ["Strategic Domain-Driven Design", "Subdomain Inti dan Pendukung", "Pola Anti-Corruption Layer"]},
            {"title": "Bab 3: Komunikasi Antar-Layanan & Event-Driven Architecture", "pages": "hlm. 135 - 220", "subs": ["Protokol gRPC vs REST API", "Event Sourcing & CQRS", "Orkestrasi Saga Terdistribusi"]},
            {"title": "Bab 4: Orkestrasi Kubernetes & Resiliensi Tingkat Tinggi", "pages": "hlm. 221 - 340", "subs": ["Circuit Breaker & Retry Mechanism", "Service Mesh & Zero Trust Network", "Graceful Degradation"]},
            {"title": "Bab 5: Observabilitas Terpadu & Pemantauan Produksi", "pages": "hlm. 341 - 448", "subs": ["Distributed Tracing OpenTelemetry", "SLA/SLO Alerting Grafana", "Chaos Engineering Sandbox"]}
        ],
        "excerpt_heading": "Bab 1: Mengapa dan Kapan Organisasi Harus Memilih Microservices?",
        "excerpt_text1": "Perdebatan mengenai apakah sistem aplikasi harus dipecah menjadi unit-unit layanan mandiri (microservices) atau dipertahankan sebagai monolitik modular bukan sekadar persoalan pilihan teknologi. Ini adalah keputusan strategis yang berakar pada hukum Conway, dinamika koordinasi tim, kecepatan siklus rilis (release velocity), serta batas skalabilitas horisontal basis kode.",
        "excerpt_text2": "Microservices memberikan otonomi penuh pada masing-masing tim perekayasa perangkat lunak untuk melakukan deployment tanpa ketergantungan langsung terhadap komponen lain. Namun, otonomi ini datang bersama konsekuensi kompleksitas baru: konsistensi data eventual, latensi jaringan antar-node, serta kegagalan parsial yang tak terhindarkan pada lingkungan komputasi awan modern."
    },
    {
        "file": "prompt_engineering_llm.pdf",
        "title": "Rekayasa Prompt & Implementasi LLM Modern: Panduan Komprehensif AI Generatif Mandiri",
        "subtitle": "Strategi Lanjutan Few-Shot, RAG Multi-Modal, Integrasi Vector Database, dan Agen Cerdas Otonom",
        "author": "Dr. Ir. Rian Pratama, M.Sc., Andrew Ng, Ph.D.",
        "editor": "Tim Lab Kecerdasan Buatan Galura",
        "publisher": "Galura Tech Publishing bekerjasama dengan AI Research Press",
        "year": "2024",
        "isbn": "978-623-01-3891-2",
        "call_number": "EB 006.31 PRA r",
        "ddc": "006.31",
        "category": "Artificial Intelligence & Large Language Models",
        "series": "Seri Kecerdasan Artifisial Tingkat Lanjut; Jilid 2",
        "pages_info": "xxiv, 396 halaman",
        "synopsis1": "Karya ini mengupas tuntas paradigma rekayasa prompt dan integrasi sistem model bahasa besar (LLM) untuk kebutuhan industri modern. Membahas formulasi prompt deterministik, teknik pemikiran berantai (Chain-of-Thought), penalaran ReAct, dan mitigasi halusinasi model pada domain sensitif seperti hukum, medis, dan perbankan.",
        "synopsis2": "Fokus mendalam diberikan pada arsitektur Retrieval-Augmented Generation (RAG) hibrida yang memadukan pencarian semantik vektor dengan BM25 lexikal, re-ranking Cross-Encoder, serta implementasi agen cerdas yang mampu mengeksekusi alat komputasi eksternal secara terverifikasi.",
        "chapters": [
            {"title": "Bab 1: Anatomi Transformer & Karakteristik Model Bahasa Besar", "pages": "hlm. 1 - 46", "subs": ["Mekanisme Self-Attention", "Tokenisasi & Skala Parameter", "Deterministik vs Non-Deterministik"]},
            {"title": "Bab 2: Teknik Lanjutan Rekayasa Prompt", "pages": "hlm. 47 - 118", "subs": ["Few-Shot Contextual Learning", "Chain-of-Thought & Tree-of-Thoughts", "Prompt Injection Defense"]},
            {"title": "Bab 3: Arsitektur Retrieval-Augmented Generation (RAG) Produksi", "pages": "hlm. 119 - 212", "subs": ["Strategi Chunking Konseptual", "Pencarian Hibrida Dense-Sparse", "Re-ranking & Context Compression"]},
            {"title": "Bab 4: Integrasi Basis Data Vektor Skala Enterprise", "pages": "hlm. 213 - 298", "subs": ["Index HNSW & IVFFlat", "Qdrant, Milvus & Pinecone", "Metrik Evaluasi Kesamaan"]},
            {"title": "Bab 5: Membangun Agen Otonom Multi-Langkah", "pages": "hlm. 299 - 380", "subs": ["Framework LangGraph & AutoGen", "Tool Calling & API Sandboxing", "Safety Guardrails & Evaluasi RAGAS"]}
        ],
        "excerpt_heading": "Bab 1: Menembus Batas Token: Menghubungkan Model dengan Pengetahuan Nyata",
        "excerpt_text1": "Meskipun model fondasi bahasa generasi terbaru memiliki kemampuan bernalar luar biasa, batas pengetahuan statis (training cutoff) dan kecenderungan konfabulasi (halusinasi) membatasi penerapannya pada skenario produksi kritis. Di sinilah rekayasa prompt presisi dan arsitektur RAG bertindak sebagai jembatan yang menghubungkan nalar bahasa dengan repositori data aktual organisasi.",
        "excerpt_text2": "Dengan menyematkan dokumen dinamis ke dalam ruang semantik berdimensi tinggi melalui embedding model yang tepat, kita memungkinkan model menarik konteks faktual sebelum menghasilkan respons. Pendekatan ini secara dramatis memangkas tingkat halusinasi di bawah ambang batas toleransi industri."
    },
    {
        "file": "system_design_interview.pdf",
        "title": "System Design Interview: Panduan Arsitektur Sistem Skala Ratusan Juta Pengguna",
        "subtitle": "Studi Kasus Real-World: Payment Gateway, Chat Streaming, Rate Limiter, dan Distributed Cache",
        "author": "Alex Xu, Sahn Lam",
        "editor": "Eko Kurniawan Khannedy",
        "publisher": "ByteByteGo Publishing bekerjasama dengan Galura Press",
        "year": "2024",
        "isbn": "978-1-7360491-1-2",
        "call_number": "EB 004.22 XU s",
        "ddc": "004.22",
        "category": "System Design & Scalability",
        "series": "Seri Standar Arsitektur Sistem Global; Jilid 2",
        "pages_info": "xxxii, 540 halaman",
        "synopsis1": "Buku rujukan global yang telah membantu ribuan insinyur dan arsitek sistem melewati wawancara teknis tingkat staf dan prinsipal di perusahaan teknologi terkemuka dunia. Menjelaskan langkah demi langkah kerangka kerja 4 tahap dalam menyelesaikan masalah desain sistem yang ambigu.",
        "synopsis2": "Menganalisis arsitektur sistem nyata dari dasar: kalkulasi kapasitas komputasi dan bandwidth, strategi partisi basis data (sharding), konsistensi cache Redis, penyeimbang beban global (Anycast DNS & CDN), serta mitigasi single-point-of-failure pada klaster multi-region.",
        "chapters": [
            {"title": "Bab 1: Kerangka Kerja Sistematis 4 Tahap Desain Sistem", "pages": "hlm. 1 - 38", "subs": ["Klarifikasi Ruang Lingkup Masalah", "Desain Tingkat Tinggi (High-Level)", "Investigasi Mendalam (Deep Dive)"]},
            {"title": "Bab 2: Perancangan Layanan Rate Limiter Terdistribusi", "pages": "hlm. 39 - 84", "subs": ["Algoritma Token Bucket & Leaky Bucket", "Sinkronisasi Klaster Redis Lua Script", "Penanganan Masalah Race Condition"]},
            {"title": "Bab 3: Arsitektur Sistem Chat & Messaging Skala 50 Juta DAU", "pages": "hlm. 85 - 162", "subs": ["WebSocket Connection Management", "Penyimpanan Pesan NoSQL Cassandra", "Status Online & Push Notification"]},
            {"title": "Bab 4: Desain Payment Gateway & Transaksi Finansial Idempoten", "pages": "hlm. 163 - 250", "subs": ["Kunci Idempotensi & Rekonsiliasi", "Protokol Two-Phase Commit", "Ledger Double-Entry Bookkeeping"]},
            {"title": "Bab 5: Platform Video Streaming Skala Global", "pages": "hlm. 251 - 340", "subs": ["Transcoding Pipeline Terdistribusi", "Protokol HLS/DASH & CDN Caching", "Optimasi Buffer Pemutar"]}
        ],
        "excerpt_heading": "Bab 1: Mengurai Masalah Ambigu Menjadi Cetak Biru Arsitektur",
        "excerpt_text1": "Pertanyaan wawancara desain sistem sengaja dibuat terbuka dan ambigu: 'Rancanglah YouTube', atau 'Bangunlah sistem penagihan kartu kredit'. Tujuan penguji bukan sekadar melihat diagram kotak-kotak yang Anda gambar, melainkan menilai kemampuan Anda dalam mereduksi ketidakpastian, mengestimasi beban kuantitatif, dan menimbang trade-off teknik secara obyektif.",
        "excerpt_text2": "Kunci utama keberhasilan terletak pada ketenangan dalam mengklarifikasi persyaratan fungsional dan non-fungsional sebelum mengetikkan sebaris pun kode atau menarik garis konektor. Tanpa estimasi throughput transaksi per detik (TPS) dan volume penyimpanan 5 tahun ke depan, arsitektur terbaik pun akan salah sasaran."
    },
    {
        "file": "fullstack_go_nextjs.pdf",
        "title": "Full-Stack Modern dengan Go & Next.js: Dari Nol Hingga Deployment VPS Produksi",
        "subtitle": "Integrasi REST API Fiber Berkualitas Tinggi, PostgreSQL, Redis Caching, dan Next.js 14 App Router",
        "author": "Eko Kurniawan Khannedy, Sandhika Galih",
        "editor": "Tim Pengembang Galura Software House",
        "publisher": "Galura Tech Publishing",
        "year": "2024",
        "isbn": "978-623-01-3892-9",
        "call_number": "EB 005.133 KHA f",
        "ddc": "005.133",
        "category": "Full-Stack Web Development",
        "series": "Seri Pengembang Web Indonesia Modern; Jilid 1",
        "pages_info": "xx, 412 halaman",
        "synopsis1": "Kombinasi antara efisiensi kompilasi native bahasa Go dan kekayaan interaksi antarmuka Next.js telah menjadi standar emas baru dalam rekayasa aplikasi web modern yang menuntut performa puncak dan SEO optimal. Buku ini menuntun pembaca membangun aplikasi enterprise dari nol.",
        "synopsis2": "Membahas pembuatan backend API Go dengan framework Fiber, manajemen koneksi database PostgreSQL via ORM GORM, otentikasi JWT aman berbasis HTTP-Only Cookie, manajemen state TanStack Query pada Next.js Server Components, hingga otomatisasi deployment menggunakan Docker dan Nginx Reverse Proxy.",
        "chapters": [
            {"title": "Bab 1: Fondasi Arsitektur Web Modern Go & React", "pages": "hlm. 1 - 50", "subs": ["Struktur Modul Go & Standar Clean", "Next.js App Router Paradigma", "Protokol Komunikasi Data"]},
            {"title": "Bab 2: Pembuatan REST API Performa Tinggi dengan Fiber", "pages": "hlm. 51 - 130", "subs": ["Routing & Middleware Kustom", "Validasi Request Struct Validator", "Pola Repository & Dependency Injection"]},
            {"title": "Bab 3: Interaksi Database Relasional PostgreSQL & Redis", "pages": "hlm. 131 - 210", "subs": ["Migrasi Skema Otomatis", "Indexing & Optimasi Query", "In-Memory Caching dengan Redis"]},
            {"title": "Bab 4: Pembangunan Antarmuka Reaktif Next.js 14", "pages": "hlm. 211 - 310", "subs": ["Server vs Client Components", "Optimistic UI Updates", "Integrasi TailwindCSS & Desain Sistem"]},
            {"title": "Bab 5: Strategi Deployment Produksi VPS & SSL", "pages": "hlm. 311 - 398", "subs": ["Multi-stage Dockerfile Go & Node", "Nginx Reverse Proxy & Brotli", "Automasi CI/CD & SSL Let's Encrypt"]}
        ],
        "excerpt_heading": "Bab 1: Menyatukan Kecepatan Mesin Go dengan Kelincahan Next.js",
        "excerpt_text1": "Dalam membangun sistem bisnis digital yang melayani jutaan transaksi, arsitektur aplikasi tidak boleh berkompromi antara kecepatan respon backend dan keindahan tampilan pengguna. Go menawarkan konsumsi memori yang sangat hemat dan konkurensi goroutine ringan, sementara Next.js menghadirkan Server-Side Rendering tanpa cela untuk pengalaman pengguna kelas satu.",
        "excerpt_text2": "Melalui kolaborasi kedua teknologi ini, pengembang memperoleh waktu respon API di bawah 15 milidetik dan skor Google Lighthouse di atas 95. Bab ini meletakkan fondasi arsitektural yang akan kita pakai sepanjang proyek pada buku ini."
    },
    {
        "file": "clean_architecture.pdf",
        "title": "Clean Architecture & Pola Desain Perangkat Lunak Berkelanjutan",
        "subtitle": "Panduan Prinsip SOLID, Domain-Driven Design (DDD), dan Pengujian Otomatis Bebas Dependensi",
        "author": "Robert C. Martin (Uncle Bob)",
        "editor": "Dr. Ir. Rian Pratama, M.Sc.",
        "publisher": "Prentice Hall bekerjasama dengan Galura Digital Press",
        "year": "2023",
        "isbn": "978-0-13-449416-6",
        "call_number": "EB 005.1 MAR c",
        "ddc": "005.1",
        "category": "Software Engineering Clean Code",
        "series": "Seri Praktik Rekayasa Perangkat Lunak Profesional; Jilid 3",
        "pages_info": "xxiv, 432 halaman",
        "synopsis1": "Karya legendaris Uncle Bob yang menjabarkan aturan universal struktur perangkat lunak yang tahan terhadap perubahan zaman. Memaparkan bagaimana memisahkan logika bisnis murni dari kerangka kerja (framework), basis data, antarmuka pengguna, dan pustaka eksternal lainnya.",
        "synopsis2": "Menganalisis prinsip SOLID secara mendalam, Dependency Inversion Principle, Boundary Objects, Entity Boundaries, serta strategi penulisan tes unit cepat yang berjalan murni dalam memori tanpa memerlukan koneksi ke database atau layanan eksternal.",
        "chapters": [
            {"title": "Bab 1: Apa Sebenarnya Arsitektur dan Desain Perangkat Lunak?", "pages": "hlm. 1 - 42", "subs": ["Biaya Pemeliharaan Kode Jangka Panjang", "Paradigma Terstruktur, OO, & Fungsional", "Tujuan Utama Arsitektur Bersih"]},
            {"title": "Bab 2: Menguasai Prinsip Desain SOLID", "pages": "hlm. 43 - 120", "subs": ["Single Responsibility Principle", "Open-Closed Principle", "Liskov Substitution & Interface Segregation"]},
            {"title": "Bab 3: Aturan Komponen & Batasan Arsitektur", "pages": "hlm. 121 - 198", "subs": ["Kohesi Komponen & Coupling", "Stable Dependencies Principle", "Pemisahan Kebijakan dan Rincian"]},
            {"title": "Bab 4: Arsitektur Bersih (The Clean Architecture Engine)", "pages": "hlm. 199 - 290", "subs": ["Lapisan Entities & Use Cases", "Interface Adapters & Controllers", "Frameworks & Drivers di Lapisan Terluar"]},
            {"title": "Bab 5: Pengujian Otomatis & Strategi Migrasi Legacy Code", "pages": "hlm. 291 - 410", "subs": ["Test Doubles (Mock, Stub, Fake)", "Pengujian Acceptance Berbasis Use Case", "Refactoring Tanpa Menghancurkan Bisnis"]}
        ],
        "excerpt_heading": "Bab 1: Rincian yang Harus Ditunda: Framework, Database, dan Web",
        "excerpt_text1": "Sebuah arsitektur perangkat lunak yang baik tidak membiarkan kerangka kerja (framework) atau basis data mendikte struktur aplikasi. Database adalah rincian mekanisme penyimpanan; web adalah saluran pengiriman data; framework hanyalah alat bantu. Logika bisnis inti sistem perbankan harus tetap berfungsi utuh meskipun database diganti dari PostgreSQL ke penyimpanan in-memory.",
        "excerpt_text2": "Dengan membalik arah ketergantungan (Dependency Inversion), lapisan dalam hanya mengenali abstraksi antarmuka, sementara pustaka pihak ketiga diposisikan sebagai plugin yang dapat dilepas dan diganti sewaktu-waktu tanpa menimbulkan efek domino pada aturan bisnis inti."
    },
    {
        "file": "cybersecurity_essentials.pdf",
        "title": "Cybersecurity Essentials: Analisis Serangan Siber, Penetration Testing & Server Hardening",
        "subtitle": "Panduan Praktis Mitigasi Serangan Zero-Day, Audit Keamanan UFW/Fail2ban, dan Arsitektur Zero Trust",
        "author": "Dr. Ir. Rian Pratama, M.Sc., Kevin Mitnick",
        "editor": "Tim Keamanan Siber Galura CERT",
        "publisher": "Galura Tech Publishing bekerjasama dengan CyberShield Press",
        "year": "2024",
        "isbn": "978-623-01-3893-6",
        "call_number": "EB 005.8 PRA c",
        "ddc": "005.8",
        "category": "Cybersecurity & Ethical Hacking",
        "series": "Seri Pertahanan Siber Nasional; Jilid 1",
        "pages_info": "xxii, 388 halaman",
        "synopsis1": "Di era digital yang serba terhubung, keamanan informasi bukan lagi opsi tambahan melainkan fondasi kelangsungan bisnis. Buku ini mengupas metodologi serangan siber modern dan langkah preventif berstandar industri perbankan dan militer.",
        "synopsis2": "Menyajikan panduan praktis hardening server Linux Ubuntu, mitigasi serangan DDoS lapis 4 dan 7, konfigurasi firewall UFW dan deteksi intrusi Fail2ban, analisis log forensik auditd/ELK, pencegahan SQL Injection, XSS, SSRF, serta penerapan prinsip Zero Trust Network Access.",
        "chapters": [
            {"title": "Bab 1: Lanskap Ancaman Siber Modern & Vektor Serangan", "pages": "hlm. 1 - 44", "subs": ["Ransomware & Supply Chain Attack", "Anatomi Cyber Kill Chain", "Mitigasi Kerentanan OWASP Top 10"]},
            {"title": "Bab 2: Hardening Sistem Operasi Server Linux Produksi", "pages": "hlm. 45 - 122", "subs": ["Kernel Sysctl Optimization", "Manajemen Akses SSH Kunci Kriptografi", "Penerapan AppArmor & SELinux"]},
            {"title": "Bab 3: Proteksi Jaringan, Firewall UFW & Deteksi Intrusi", "pages": "hlm. 123 - 204", "subs": ["Rule Firewall Ketat & Rate Limiting", "Konfigurasi Fail2ban Proaktif", "Analisis Paket Wireshark & Snort"]},
            {"title": "Bab 4: Metodologi Penetration Testing & Vulnerability Assessment", "pages": "hlm. 205 - 296", "subs": ["Reconnaissance & Scanning Nmap", "Eksploitasi Terkontrol Metasploit", "Pelaporan & Remediasi Risiko"]},
            {"title": "Bab 5: Implementasi Arsitektur Zero Trust & Kriptografi", "pages": "hlm. 297 - 370", "subs": ["Prinsip Never Trust Always Verify", "Manajemen Identitas Terpusat IAM", "Enkripsi Data In-Transit & At-Rest"]}
        ],
        "excerpt_heading": "Bab 1: Paradigma Zero Trust: Jangan Pernah Percaya, Selalu Verifikasi",
        "excerpt_text1": "Model keamanan tradisional berbasis perimeter berasumsi bahwa segala entitas di dalam jaringan intranet adalah pihak yang aman. Paradigma usang ini telah runtuh seiring maraknya komputasi awan, kerja jarak jauh, dan serangan phishing canggih yang mampu menembus VPN perusahaan.",
        "excerpt_text2": "Zero Trust mewajibkan setiap permintaan otentikasi dan otorisasi diperiksa secara ketat sebelum akses diberikan, tidak peduli apakah permintaan berasal dari dalam gedung kantor atau dari kafe di belahan dunia lain. Identitas pengguna dan kesehatan perangkat menjadi perimeter keamanan baru."
    },
    {
        "file": "devops_gitops_mastery.pdf",
        "title": "DevOps & GitOps Mastery: Otomasi CI/CD dengan GitHub Actions, Ansible & Kubernetes",
        "subtitle": "Strategi Deployment Zero-Downtime, Infrastruktur Sebagai Kode (IaC), dan Manajemen Rahasia Produksi",
        "author": "Brendan Burns, Kelsey Hightower",
        "editor": "Tim SRE Galura Cloud",
        "publisher": "Galura Tech Publishing bekerjasama dengan Cloud Native Press",
        "year": "2024",
        "isbn": "978-1-492-05647-8",
        "call_number": "EB 005.12 BUR d",
        "ddc": "005.12",
        "category": "DevOps & Site Reliability Engineering",
        "series": "Seri Otomasi Infrastruktur Awan; Jilid 2",
        "pages_info": "xxvi, 420 halaman",
        "synopsis1": "DevOps dan GitOps telah mengubah total cara tim perekayasa perangkat lunak mengalirkan inovasi dari repositori kode menuju lingkungan produksi secara instan, konsisten, dan aman tanpa intervensi manual yang rentan kesalahan manusia.",
        "synopsis2": "Buku ini memandu pembaca membangun pipeline CI/CD tangguh menggunakan GitHub Actions, melakukan provisioning server otomatis dengan Ansible Playbook idempotent, mengelola konfigurasi deklaratif GitOps via ArgoCD, serta merancang strategi rilis Blue-Green dan Canary Deployment pada Kubernetes.",
        "chapters": [
            {"title": "Bab 1: Revolusi Kultur DevOps Menuju Praktik GitOps", "pages": "hlm. 1 - 40", "subs": ["Prinsip Deklaratif vs Imperatif", "Git Sebagai Sumber Kebenaran Tunggal", "Siklus Feedback Cepat Developer"]},
            {"title": "Bab 2: Membangun Pipeline CI/CD Tangguh dengan GitHub Actions", "pages": "hlm. 41 - 114", "subs": ["Workflow Matrix & Caching Cepat", "Automated Testing & Linting Gate", "Build & Publish Image Kontainer"]},
            {"title": "Bab 3: Otomasi Konfigurasi & Provisioning dengan Ansible", "pages": "hlm. 115 - 198", "subs": ["Idempotensi Task & Playbook", "Inventori Dinamis & Variable Precedence", "Pengelolaan Kunci Rahasia Ansible Vault"]},
            {"title": "Bab 4: Orkestrasi Kubernetes & Pola Deployment Mutakhir", "pages": "hlm. 199 - 302", "subs": ["Strategi Blue-Green & Canary", "Horizontal Pod Autoscaler (HPA)", "Storage Persistent Volume & Secrets"]},
            {"title": "Bab 5: GitOps dengan ArgoCD & Observabilitas Produksi", "pages": "hlm. 303 - 402", "subs": ["Continuous Sync & Drift Detection", "Integrasi Notifikasi Slack/Teams", "Manajemen Insiden SRE & Post-Mortem"]}
        ],
        "excerpt_heading": "Bab 1: Git Sebagai Satu-Satunya Sumber Kebenaran Infrastruktur",
        "excerpt_text1": "Zaman ketika administrator sistem masuk melalui SSH ke server produksi untuk mengedit konfigurasi secara manual di `/etc/` telah berakhir. Praktik manual semacam itu menciptakan ketidakpastian konfigurasi (configuration drift) dan mempersulit pemulihan ketika insiden bencana sistem terjadi.",
        "excerpt_text2": "Dengan GitOps, setiap deklarasi infrastruktur dan status aplikasi disimpan sebagai kode di repositori Git. Setiap perubahan harus melalui pull request, audit keamanan, dan disinkronkan secara otomatis oleh agen rekonsiliasi menuju klaster produksi."
    },
    {
        "file": "data_science_python.pdf",
        "title": "Data Science & Machine Learning Praktis dengan Python, Pandas dan Scikit-Learn",
        "subtitle": "Eksplorasi Data, Rekayasa Fitur, Model Prediktif Supervised/Unsupervised, dan MLOps Pipeline",
        "author": "Andrew Ng, Ph.D., Aurélien Géron",
        "editor": "Dr. Ir. Rian Pratama, M.Sc.",
        "publisher": "O Reilly Media bekerjasama dengan Galura Data Institute",
        "year": "2024",
        "isbn": "978-1-492-03264-9",
        "call_number": "EB 006.3 NG d",
        "ddc": "006.3",
        "category": "Data Science & Machine Learning",
        "series": "Seri Sains Data & Kecerdasan Mesin; Jilid 1",
        "pages_info": "xxviii, 464 halaman",
        "synopsis1": "Sains data telah menjadi motor penggerak utama dalam pengambilan keputusan bisnis modern. Buku ini menyajikan panduan praktis dan matematis yang seimbang dalam menerapkan algoritma machine learning menggunakan ekosistem bahasa Python.",
        "synopsis2": "Menjelaskan eksplorasi data komprehensif menggunakan Pandas dan NumPy, visualisasi interaktif Seaborn, prapemrosesan data kotor, rekayasa fitur (feature engineering), model regresi, pohon keputusan (Random Forest & XGBoost), clustering, hingga deployment model melalui API FastAPI.",
        "chapters": [
            {"title": "Bab 1: Metodologi Alur Kerja Sains Data Modern", "pages": "hlm. 1 - 48", "subs": ["Siklus Hidup Proyek Data CRISP-DM", "Penetapan Metrik Keberhasilan Bisnis", "Setup Lingkungan Jupyter & Poetry"]},
            {"title": "Bab 2: Analisis Eksplorasi Data & Pembersihan Mendalam", "pages": "hlm. 49 - 132", "subs": ["Penanganan Missing Values & Outliers", "Transformasi Distribusi Fitur", "Visualisasi Korelasi Antar-Variabel"]},
            {"title": "Bab 3: Algoritma Pembelajaran Terarah (Supervised Learning)", "pages": "hlm. 133 - 224", "subs": ["Regresi Linier & Logistik Multikelas", "Support Vector Machines (SVM)", "Ensemble Learning: Random Forest & XGBoost"]},
            {"title": "Bab 4: Pembelajaran Tak Terarah & Reduksi Dimensi", "pages": "hlm. 225 - 314", "subs": ["K-Means & DBSCAN Clustering", "Principal Component Analysis (PCA)", "Deteksi Anomali Data Produksi"]},
            {"title": "Bab 5: Evaluasi Model, Validasi Silang & Deployment MLOps", "pages": "hlm. 315 - 440", "subs": ["ROC-AUC, Precision, Recall, & F1-Score", "Hyperparameter Tuning Optuna", "Serving Model dengan FastAPI & Docker"]}
        ],
        "excerpt_heading": "Bab 1: Kualitas Data: Fondasi Tertinggi Keberhasilan Machine Learning",
        "excerpt_text1": "Pepatah 'Garbage In, Garbage Out' tidak pernah seakurat dalam konteks machine learning. Sehebat apa pun arsitektur model dan serumit apa pun jaringan saraf yang kita rancang, model prediktif tidak akan pernah mampu menghasilkan wawasan bermakna jika data pelatihan yang digunakan dipenuhi bias dan galat pengukuran.",
        "excerpt_text2": "Oleh karena itu, lebih dari 70 persen waktu seorang praktisi sains data profesional dihabiskan untuk memahami konteks domain, membersihkan data yang terdistorsi, dan merekayasa fitur-fitur baru yang merefleksikan dinamika kenyataan di lapangan."
    },
    {
        "file": "ui_ux_design_systems.pdf",
        "title": "Desain UI/UX & Design Systems Modern: Menyelaraskan Estetika Visual dengan Kebutuhan Pengguna",
        "subtitle": "Metodologi Riset Pengguna Berbasis Data, Atomic Design di Figma, Token Desain CSS, dan Standar Aksesibilitas WCAG 2.1",
        "author": "Dr. Ayu Lestari, M.T.I., Don Norman",
        "editor": "Tim Desain Produk Digital Galura",
        "publisher": "Galura Creative Publishing",
        "year": "2024",
        "isbn": "978-623-01-3894-3",
        "call_number": "EB 741.6 LES d",
        "ddc": "741.6",
        "category": "UI/UX Design Systems",
        "series": "Seri Desain Antarmuka Produk Digital; Jilid 1",
        "pages_info": "xviii, 348 halaman",
        "synopsis1": "Desain antarmuka bukan sekadar mempercantik tampilan visual, melainkan menciptakan jembatan kognitif yang intuitif antara kebutuhan pengguna dan kapabilitas fungsional teknologi. Buku ini memandu desainer dan developer menciptakan pengalaman digital yang inklusif dan memikat.",
        "synopsis2": "Menguraikan tahapan riset pengguna kualitatif dan kuantitatif, usability testing, penyusunan arsitektur informasi, prinsip Atomic Design di Figma, pembuatan tokens desain CSS lintas platform, serta pemenuhan kepatuhan aksesibilitas web internasional WCAG 2.1 Level AA.",
        "chapters": [
            {"title": "Bab 1: Prinsip Dasar Desain Berpusat Pada Pengguna (UCD)", "pages": "hlm. 1 - 42", "subs": ["Model Mental Pengguna & Affordance", "Hukum UX: Fitts, Hick, & Miller Law", "Menyeimbangkan Estetika dan Utilitas"]},
            {"title": "Bab 2: Metodologi Riset Pengguna & Pengujian Kegunaan", "pages": "hlm. 43 - 108", "subs": ["Wawancara Kontekstual & Persona", "Card Sorting & Tree Testing", "Analisis Metrik Usability SUS & CES"]},
            {"title": "Bab 3: Membangun Design System dengan Pendekatan Atomik", "pages": "hlm. 109 - 188", "subs": ["Atom, Molekul, Organisme, & Template", "Variabel & Auto-Layout Figma Lanjut", "Dokumentasi Komponen Interaktif"]},
            {"title": "Bab 4: Translasi Desain ke Kode: Tokens Desain & CSS Modern", "pages": "hlm. 189 - 264", "subs": ["Style Dictionary & Token JSON", "Variabel CSS HSL Dinamis & Dark Mode", "Komponen Reaktif Lintas Framework"]},
            {"title": "Bab 5: Standar Aksesibilitas Web Inklusif (WCAG 2.1 AA)", "pages": "hlm. 265 - 330", "subs": ["Kontras Warna & Tipografi Terbaca", "Navigasi Keyboard & Status Fokus", "Atribut WAI-ARIA & Screen Reader Testing"]}
        ],
        "excerpt_heading": "Bab 1: Empati dan Kognisi: Landasan Antarmuka Digital yang Nyaman",
        "excerpt_text1": "Setiap detik ketika seorang pengguna menatap layar ponsel atau komputernya, otaknya bekerja keras memproses ratusan stimulus visual. Jika antarmuka yang kita buat menuntut beban kognitif berlebihan hanya untuk menemukan tombol 'Lanjutkan', maka desain tersebut telah gagal memenuhi tugas utamanya.",
        "excerpt_text2": "Desain yang hebat adalah desain yang terasa tidak kasat mata bagi pengguna; pengguna berhasil menuntaskan tujuannya secara lancar tanpa pernah menyadari betapa rumitnya arsitektur informasi di balik layar."
    },
    {
        "file": "tech_startup_scale.pdf",
        "title": "Strategi Skalabilitas Bisnis Startup Teknologi: Dari Validasi Pasar Hingga Pendanaan Seri A",
        "subtitle": "Panduan Pencapaian Product-Market Fit, Analisis Unit Economics (CAC & LTV), Retensi Kohor, dan Tata Kelola Korporasi Rintisan",
        "author": "Gita Wirjawan, Eric Ries",
        "editor": "Tim Analis Bisnis Modal Ventura Galura",
        "publisher": "Elex Media Komputindo Digital bekerjasama dengan Galura Press",
        "year": "2024",
        "isbn": "978-623-01-3895-0",
        "call_number": "EB 658.4 WIR s",
        "ddc": "658.4",
        "category": "Digital Business & Tech Startups",
        "series": "Seri Manajemen Eksekutif & Kewirausahaan Digital; Jilid 2",
        "pages_info": "xxii, 360 halaman",
        "synopsis1": "Membangun startup teknologi bukan hanya tentang memiliki ide cemerlang, melainkan tentang eksekusi disiplin dalam memvalidasi hipotesis pasar dan membangun mesin pertumbuhan bisnis yang berkelanjutan. Buku ini mengulas strategi navigating lembah kematian (valley of death) startup.",
        "synopsis2": "Menjabarkan metodologi Lean Startup, perhitungan unit economics presisi (Customer Acquisition Cost, Lifetime Value, Payback Period), analisis retensi berbasis kurva kohor, strategi penetapan harga B2B/B2C, serta tips negosiasi Term Sheet pada putaran pendanaan Seed hingga Seri A.",
        "chapters": [
            {"title": "Bab 1: Menemukan dan Mengukur Product-Market Fit", "pages": "hlm. 1 - 46", "subs": ["Validasi Masalah Pelanggan Riil", "Metrik Sean Ellis 40% Sangat Kecewa", "Pivot Strategis vs Ketahanan Eksekusi"]},
            {"title": "Bab 2: Kalkulasi Unit Economics yang Berdaya Tahan", "pages": "hlm. 47 - 116", "subs": ["Formula CAC Nyata Termasuk Biaya SDM", "Estimasi LTV Berbasis Margin Kotor", "Rasio LTV/CAC Ideal & Payback Period"]},
            {"title": "Bab 3: Analisis Kohor & Pertumbuhan Retensi Berkelanjutan", "pages": "hlm. 117 - 192", "subs": ["Membaca Kurva Retensi Mengempang", "Strategi Onboarding & Activation Rate", "Mitigasi Churn Rate Secara Proaktif"]},
            {"title": "Bab 4: Arsitektur Penjualan & Go-To-Market (GTM) Terarah", "pages": "hlm. 193 - 274", "subs": ["Product-Led Growth vs Sales-Led Growth", "Channel Distribusi Eksklusif", "Strategi Pricing & Packaging Tiering"]},
            {"title": "Bab 5: Penggalangan Dana Modal Ventura & Tata Kelola Startup", "pages": "hlm. 275 - 346", "subs": ["Membedah Term Sheet & Valuasi Saham", "Klausul Likuidasi & Anti-Dilusi", "Kultur Korporasi & Manajemen Burn Rate"]}
        ],
        "excerpt_heading": "Bab 1: Kebohongan Metrik Semu (Vanity Metrics) vs Kenyataan Kas",
        "excerpt_text1": "Banyak pendiri startup terbuai oleh angka unduhan aplikasi atau jumlah pengguna terdaftar yang melonjak tajam setelah kampanye bakar uang. Namun di hadapan investor institusional dan kenyataan neraca keuangan, angka-angka tersebut hanyalah metrik semu yang tidak membuktikan adanya nilai bisnis nyata.",
        "excerpt_text2": "Pertumbuhan sejati diukur dari retensi pengguna yang secara konsisten kembali menggunakan produk Anda dan kesediaan mereka untuk membayar nilai ekonomi yang Anda tawarkan, tanpa subsidi buatan."
    },
    {
        "file": "mobile_app_flutter.pdf",
        "title": "Pengembangan Aplikasi Mobile Lintas Platform dengan Flutter & Dart: Arsitektur BLoC & Offline-First",
        "subtitle": "Penerapan State Management Modern, Sinkronisasi Data Latar Belakang SQLite, Animasi Transisi Halus, dan Rilis Toko Aplikasi",
        "author": "Donny Prakoso, Angela Yu",
        "editor": "Tim Mobile Engineering Galura Studio",
        "publisher": "Galura Tech Publishing",
        "year": "2024",
        "isbn": "978-623-01-3896-7",
        "call_number": "EB 005.26 PRA p",
        "ddc": "005.26",
        "category": "Mobile App Engineering",
        "series": "Seri Pemrograman Mobile Terapan; Jilid 1",
        "pages_info": "xxiv, 416 halaman",
        "synopsis1": "Ekosistem Flutter telah merevolusi kecepatan pengembangan aplikasi mobile dengan menghasilkan kode terkompilasi native ke iOS dan Android dari satu basis kode Dart tunggal. Buku ini menjadi pedoman lengkap bagi pengembang yang ingin melangkah dari aplikasi sederhana ke kelas enterprise.",
        "synopsis2": "Menitikberatkan pada pola arsitektur BLoC (Business Logic Component), manajemen state deterministik, strategi penyimpanan lokal offline-first menggunakan SQLite/Isar, sinkronisasi latar belakang dengan WorkManager, serta integrasi pustaka animasi interaktif dan CI/CD rilis otomatis ke Play Store dan App Store.",
        "chapters": [
            {"title": "Bab 1: Fondasi Framework Flutter & Bahasa Dart 3", "pages": "hlm. 1 - 48", "subs": ["Widget Tree & Mekanisme Rendering Skia/Impeller", "Pattern Matching & Records di Dart 3", "Siklus Hidup Widget Statefull"]},
            {"title": "Bab 2: Manajemen State Berkelanjutan dengan Pola BLoC", "pages": "hlm. 49 - 128", "subs": ["Streams & Sink di Dart", "BlocBuilder, BlocListener, & BlocConsumer", "Pengujian Unit BLoC dengan BlocTest"]},
            {"title": "Bab 3: Arsitektur Offline-First & Sinkronisasi Latar Belakang", "pages": "hlm. 129 - 218", "subs": ["Penyimpanan Data Lokal SQLite / Drift", "Manajemen Konflik Data Offline", "Worker Sinkronisasi Otomatis"]},
            {"title": "Bab 4: Desain Antarmuka Adaptif & Animasi Halus", "pages": "hlm. 219 - 310", "subs": ["Material 3 & Cupertino Theming", "Hero Animation & Custom Painter", "Optimasi Frame Rate 60/120 FPS"]},
            {"title": "Bab 5: Keamanan Aplikasi Mobile & Distribusi Otomatis", "pages": "hlm. 311 - 400", "subs": ["Enkripsi Secure Storage & Certificate Pinning", "Automasi Fastlane CI/CD Build", "Kiat Menembus Review Google Play & Apple"]}
        ],
        "excerpt_heading": "Bab 1: Merender Piksel Sempurna: Mengapa Flutter Berbeda?",
        "excerpt_text1": "Berbeda dengan pendekatan lintas platform tradisional yang mengandalkan jembatan JavaScript untuk berkomunikasi dengan komponen UI native sistem operasi, Flutter menggambar setiap piksel langsung di atas kanvas mesin rendering grafis Impeller miliknya sendiri.",
        "excerpt_text2": "Pendekatan ini mengeliminasi masalah bottleneck performa dan menjamin bahwa antarmuka yang dirancang desainer akan tampil identik secara konsisten di ribuan varian perangkat Android maupun ekosistem Apple iOS."
    },
    {
        "file": "database_deep_dive.pdf",
        "title": "Database Deep Dive: Optimasi Query SQL, Desain Indeks B-Tree & Arsitektur Sharding",
        "subtitle": "Bedah Mesin Penyimpanan InnoDB, Analisis Execution Plan EXPLAIN, Mitigasi Deadlock, dan Replikasi Multi-Master",
        "author": "Alex Xu, Baron Schwartz",
        "editor": "Tim Database Administrator Galura Core",
        "publisher": "O Reilly Media bekerjasama dengan Galura Press",
        "year": "2023",
        "isbn": "978-1-492-08051-0",
        "call_number": "EB 005.74 XU d",
        "ddc": "005.74",
        "category": "Database Internals & Caching",
        "series": "Seri Teknologi Database Skala Besar; Jilid 2",
        "pages_info": "xxviii, 490 halaman",
        "synopsis1": "Di balik setiap aplikasi berskala masif, terdapat basis data relasional yang harus mampu melayani puluhan ribu transaksi konkuren tanpa degradasi performa atau korupsi data. Buku ini membongkar rahasia internal mesin database relasional (khususnya MySQL dan MariaDB).",
        "synopsis2": "Menjelaskan cara kerja engine InnoDB, struktur halaman indeks B+ Tree dan Clustered Index, optimasi query lambat menggunakan EXPLAIN ANALYZE, isolasi transaksi ACID, strategi penanganan deadlock dan lock escalation, serta teknik partisi horizontal (sharding) dan replikasi data multi-region.",
        "chapters": [
            {"title": "Bab 1: Anatomi Mesin Penyimpanan InnoDB & Buffer Pool", "pages": "hlm. 1 - 54", "subs": ["Arsitektur Memori & Struktur Halaman 16KB", "Write-Ahead Logging (WAL) & Redo/Undo Log", "Algoritma Pembersihan Dirty Pages LRU"]},
            {"title": "Bab 2: Seni Merancang Indeks Efisien (B+ Tree Deep Dive)", "pages": "hlm. 55 - 146", "subs": ["Clustered vs Secondary Index", "Composite Index & Aturan Leftmost Prefix", "Covering Index & Eliminasi Index Lookup"]},
            {"title": "Bab 3: Membaca & Menindaklanjuti EXPLAIN ANALYZE", "pages": "hlm. 147 - 236", "subs": ["Tipe Join (Nested Loop, Hash Join, Merge)", "Identifikasi Full Table Scan Berbahaya", "Cost-Based Optimizer (CBO) Behavior"]},
            {"title": "Bab 4: Konkurensi Transaksi, Tingkat Isolasi & Kunci Baris", "pages": "hlm. 237 - 338", "subs": ["Multi-Version Concurrency Control (MVCC)", "Shared Lock vs Exclusive Lock", "Analisis Log Deadlock & Mitigasi Aplikasi"]},
            {"title": "Bab 5: Skalabilitas Horisontal, Replikasi & Sharding", "pages": "hlm. 339 - 470", "subs": ["Replikasi Asinkron vs Semi-Sinkron", "Sharding Key Selection & Distributed Queries", "Migrasi Skema Online Tanpa Downtime (gh-ost)"]}
        ],
        "excerpt_heading": "Bab 1: Menembus Batas I/O: Mengapa Basis Data Melambat?",
        "excerpt_text1": "Ketika sebuah aplikasi mulai mengalami perlambatan akut, reaksi pertama yang sering diambil adalah menambahkan memori RAM atau menambah core CPU pada server. Namun dalam mayoritas kasus nyata, akar masalahnya bukan kekurangan perangkat keras, melainkan query SQL yang tidak efisien yang memicu jutaan pembacaan I/O disk acak.",
        "excerpt_text2": "Memahami bagaimana InnoDB menata data dalam struktur pohon B+ Tree dan bagaimana Buffer Pool mengelola cache halaman adalah kunci emas bagi arsitek perangkat lunak untuk menekan latensi kueri dari hitungan detik menjadi milidetik."
    },
    {
        "file": "digital_leadership.pdf",
        "title": "Kepemimpinan Digital & Transformasi Budaya: Membangun Tim Kolaboratif Era AI",
        "subtitle": "Kultur Pertumbuhan (Growth Mindset), Komunikasi Asinkron Tim Terdistribusi, dan Manajemen Inovasi Berkelanjutan",
        "author": "Satya Nadella, Amy Edmondson",
        "editor": "Tim Pengembangan Sumber Daya Manusia Galura",
        "publisher": "Harper Business bekerjasama dengan Galura Publishing",
        "year": "2024",
        "isbn": "978-0-06-265885-2",
        "call_number": "EB 658.409 NAD k",
        "ddc": "658.409",
        "category": "Digital Business & Leadership",
        "series": "Seri Transformasi Manajemen Korporasi; Jilid 1",
        "pages_info": "xx, 310 halaman",
        "synopsis1": "Transformasi digital bukan tentang pembelian perangkat lunak baru atau langganan cloud termutakhir, melainkan tentang transformasi cara berpikir manusia dan keberanian kepemimpinan dalam merestrukturisasi budaya kerja organisasi agar adaptif terhadap disrupsi AI.",
        "synopsis2": "Mengulas pengalaman kepemimpinan mentransformasikan raksasa teknologi menuju budaya 'Learn-it-all' daripada 'Know-it-all', menciptakan keamanan psikologis (psychological safety) di mana kegagalan eksperimen dipelajari bukan dihukum, serta mengelola kerja kolaboratif asinkron melintasi zona waktu.",
        "chapters": [
            {"title": "Bab 1: Menemukan Kembali Jiwa Organisasi (Hit Refresh)", "pages": "hlm. 1 - 42", "subs": ["Misi, Nilai-Nilai, & Tujuan Eksistensial", "Meninggalkan Silo Birokrasi Internal", "Membangun Empati Sebagai Pendorong Inovasi"]},
            {"title": "Bab 2: Menumbuhkan Budaya Belajar Berkelanjutan (Growth Mindset)", "pages": "hlm. 43 - 104", "subs": ["Dari Know-It-All Menjadi Learn-It-All", "Menghargai Upaya dan Pembelajaran Kegagalan", "Pengembangan Talenta di Era Kecerdasan Artifisial"]},
            {"title": "Bab 3: Keamanan Psikologis Sebagai Fondasi Tim Berperforma Tinggi", "pages": "hlm. 105 - 170", "subs": ["Mengapa Orang Takut Bersuara di Tempat Kerja", "Peran Pemimpin dalam Menerima Kerentanan", "Debat Konstruktif Tanpa Menyerang Pribadi"]},
            {"title": "Bab 4: Tata Kelola Kerja Asinkron Tim Jarak Jauh (Remote Work)", "pages": "hlm. 171 - 234", "subs": ["Kelelahan Meeting Virtual & Solusinya", "Dokumentasi Tertulis Sebagai Budaya Utama", "Mengukur Hasil Output Bukan Jam Kerja"]},
            {"title": "Bab 5: Memimpin Inovasi Berkelanjutan Menghadapi Masa Depan", "pages": "hlm. 235 - 296", "subs": ["Evolusi Komputasi Kuantum & Etika AI", "Kemitraan Strategis Ekosistem Terbuka", "Warisan Kepemimpinan Berkelanjutan"]}
        ],
        "excerpt_heading": "Bab 1: Mengubah Budaya: Dari Rasa Tahu Segalanya Menjadi Semangat Mempelajari Segalanya",
        "excerpt_text1": "Perusahaan-perusahaan besar yang runtuh jarang sekali diakibatkan oleh kurangnya talenta pintar atau ketiadaan dana penelitian. Mereka hancur karena terjebak dalam arogansi kesuksesan masa lalu, menganggap diri telah mengetahui segalanya, dan menolak beradaptasi ketika gelombang teknologi baru menyapu pasar.",
        "excerpt_text2": "Kepemimpinan transformatif menuntut kerendahan hati untuk terus belajar, mendengarkan sinyal-sinyal lemah dari garis depan, dan memberdayakan setiap individu dalam organisasi untuk berkontribusi melampaui sekat-sekat hierarki tradisional."
    },
    {
        "file": "iot_industry_40.pdf",
        "title": "Internet of Things (IoT) Industri 4.0: Sensor Cerdas, Protokol MQTT & Edge Computing",
        "subtitle": "Arsitektur Telemetri Industri Skala Masif, Broker Mosquitto, Basis Data Time-Series, dan Enkripsi Perangkat Keras",
        "author": "Dr. Ir. Rian Pratama, M.Sc., Dirk Slama",
        "editor": "Tim Laboratorium IoT & Mekatronika Galura",
        "publisher": "Galura Tech Publishing bekerjasama dengan Springer Digital",
        "year": "2024",
        "isbn": "978-623-01-3897-4",
        "call_number": "EB 004.678 PRA i",
        "ddc": "004.678",
        "category": "Internet of Things & Edge Computing",
        "series": "Seri Otomasi Industri & Sistem Tertanam; Jilid 1",
        "pages_info": "xxiv, 372 halaman",
        "synopsis1": "Revolusi Industri 4.0 bertumpu pada interkoneksi cerdas antara mesin-mesin fisik di lantai pabrik dengan platform analitik awan. Buku ini menyajikan arsitektur telemetri industri komprehensif yang dirancang untuk keandalan tinggi dan latensi rendah.",
        "synopsis2": "Menjelaskan pemilihan mikrokontroler industri (ESP32, STM32, Raspberry Pi Compute Module), komunikasi data sensor via protokol MQTT/CoAP dengan broker Mosquitto, penyimpanan telemetri pada time-series database InfluxDB/TimescaleDB, komputasi tepi (edge computing), dan enkripsi perangkat keras TPM/Axiom.",
        "chapters": [
            {"title": "Bab 1: Konvergensi Teknologi Operasional (OT) & Teknologi Informasi (IT)", "pages": "hlm. 1 - 44", "subs": ["Standar Arsitektur RAMI 4.0", "Tantangan Lingkungan Industri Kasar", "Protokol Warisan Modbus vs Protokol Modern"]},
            {"title": "Bab 2: Protokol Komunikasi IoT Ringan: MQTT & CoAP", "pages": "hlm. 45 - 118", "subs": ["Publish-Subscribe Pattern & Topic Design", "Tingkat Kualitas Layanan (QoS 0, 1, 2)", "Keamanan Transport TLS & Sertifikat Klien"]},
            {"title": "Bab 3: Edge Computing Gateway & Prapemrosesan Data Tepi", "pages": "hlm. 119 - 202", "subs": ["Filter Noise Sinyal Sensor Kalman Filter", "Inferensi Machine Learning Ringan di Edge", "Buffer Data Offline Saat Terputus Jaringan"]},
            {"title": "Bab 4: Manajemen Basis Data Deret Waktu (Time-Series DB)", "pages": "hlm. 203 - 286", "subs": ["Arsitektur InfluxDB & TimescaleDB", "Downsampling Otomatis & Kebijakan Retensi", "Visualisasi Dashboard Grafana Real-Time"]},
            {"title": "Bab 5: Keamanan Siber Perangkat Keras & Pembaruan OTA Aman", "pages": "hlm. 287 - 358", "subs": ["Hardware Root of Trust & Secure Boot", "Firmware Over-The-Air (FOTA) Terenkripsi", "Audit Kerentanan Jaringan IoT"]}
        ],
        "excerpt_heading": "Bab 1: Menghubungkan Mesin Fisik dengan Otak Komputasi Awan",
        "excerpt_text1": "Di lantai fasilitas manufaktur modern, setiap motor, kompresor, dan ban berjalan memancarkan ribuan titik data getaran, suhu, dan tekanan setiap detiknya. Mengirimkan seluruh aliran data mentah ini secara langsung ke komputasi awan tanpa penyaringan akan menghabiskan bandwidth jaringan dan biaya komputasi yang tak terkendali.",
        "excerpt_text2": "Solusi industri sejati mengadopsi gerbang komputasi tepi (edge computing gateway) yang cerdas: data dianalisis secara lokal untuk mendeteksi anomali kritis dalam hitungan milidetik, sementara hanya ringkasan dan tren statistik yang dikirimkan ke cloud untuk analitik prediktif jangka panjang."
    },
    {
        "file": "metodologi_riset_scopus.pdf",
        "title": "Metodologi Riset Komputasi & Panduan Publikasi Ilmiah Jurnal Terindeks Scopus/WoS",
        "subtitle": "Perumusan Kebaruan (Novelty), Tinjauan Pustaka Sistematis PRISMA, Validasi Eksperimental, dan Strategi Peer-Review",
        "author": "Dr. Ir. Rian Pratama, M.Sc., Prof. Dr. Ir. Suhono H. Supangkat",
        "editor": "Dewan Riset Akademik Galura Institute",
        "publisher": "Galura Academic Press bekerjasama dengan Penerbit Salemba Humanika",
        "year": "2024",
        "isbn": "978-623-01-3898-1",
        "call_number": "EB 001.42 PRA m",
        "ddc": "001.42",
        "category": "Research Methodology & Academic Writing",
        "series": "Seri Publikasi Ilmiah & Akademik Pascasarjana; Jilid 1",
        "pages_info": "xx, 330 halaman",
        "synopsis1": "Publikasi pada jurnal bereputasi tinggi terindeks Scopus kuartil atas (Q1/Q2) dan Web of Science menuntut metodologi riset yang ketat, orisinalitas kontribusi ilmiah yang terukur, serta penyajian naskah artikel yang memenuhi standar akademis internasional.",
        "synopsis2": "Buku ini membimbing akademisi, peneliti, dan mahasiswa pascasarjana merumuskan kontribusi penelitian (*novelty*), melaksanakan Systematic Literature Review berpedoman protokol PRISMA, merancang uji coba eksperimen komparatif berbasis benchmark standar, serta menanggapi komentar reviewer secara elegan dan profesional.",
        "chapters": [
            {"title": "Bab 1: Fondasi Riset Ilmiah di Bidang Ilmu Komputer", "pages": "hlm. 1 - 40", "subs": ["Karakteristik Riset Sains Komputasi", "Menemukan Research Gap yang Bernilai", "Formulasi Hipotesis & Research Questions"]},
            {"title": "Bab 2: Systematic Literature Review Menggunakan Protokol PRISMA", "pages": "hlm. 41 - 102", "subs": ["Strategi Query Database IEEE, ACM, ScienceDirect", "Kriteria Inklusi dan Eksklusi Transparan", "Sintesis Bukti & Bibliometric VOSviewer"]},
            {"title": "Bab 3: Perancangan Eksperimen Empiris & Validasi Benchmark", "pages": "hlm. 103 - 180", "subs": ["Dataset Standar & Metrik Evaluasi Komparatif", "Uji Signifikansi Statistik (t-test, ANOVA)", "Reproducibility & Open Source Artifacts"]},
            {"title": "Bab 4: Struktur Penulisan Naskah IMRAD Standar Q1", "pages": "hlm. 181 - 256", "subs": ["Menulis Judul & Abstrak yang Mengikat", "Menyajikan Hasil Melalui Grafik Vektor Presisi", "Diskusi Kritis Melawan Keterbatasan Penelitian"]},
            {"title": "Bab 5: Navigasi Proses Peer-Review & Menjawab Komentar Reviewer", "pages": "hlm. 257 - 318", "subs": ["Memilih Jurnal yang Tepat Tanpa Predator", "Menyusun Response Letter Poin demi Poin", "Etika Kepengarangan & Penanganan Konflik Kepentingan"]}
        ],
        "excerpt_heading": "Bab 1: Menemukan Kebaruan Ilmiah: Membedakan 'Proyek Coding' dari 'Riset Ilmiah'",
        "excerpt_text1": "Salah satu batu sandungan terbesar bagi peneliti pemula di bidang ilmu komputer adalah ketidakmampuan membedakan antara kegiatan rekayasa perangkat lunak biasa (software development) dengan penelitian ilmiah murni (scientific research). Membangun sebuah aplikasi web atau mobile dengan teknologi terbaru bukanlah riset ilmiah jika tidak ada pertanyaan mendasar yang dijawab.",
        "excerpt_text2": "Sebuah kontribusi ilmiah mensyaratkan adanya pemahaman baru yang digali, algoritma baru yang terbukti secara empiris lebih unggul daripada metode *state-of-the-art*, atau formulasi teoretis yang memperluas batas pengetahuan peradaban manusia."
    }
]

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Generating 15 rich, professional 3-page E-Book PDFs in {out_dir}...")
    
    for eb in ebooks_catalog:
        target_path = os.path.join(out_dir, eb["file"])
        raw_pdf = build_ebook_pdf(eb)
        with open(target_path, "wb") as f:
            f.write(raw_pdf)
        print(f" [OK] Generated: {eb['file']} ({len(raw_pdf):,} bytes, 3 pages)")

    # Also keep sample_ebook.pdf as fallback
    with open(os.path.join(out_dir, "sample_ebook.pdf"), "wb") as f:
        f.write(build_ebook_pdf(ebooks_catalog[0]))
    print(" [OK] Generated: sample_ebook.pdf (fallback)")
    print(f"Done! Successfully generated {len(ebooks_catalog)} realistic PDF files.")

if __name__ == "__main__":
    main()
