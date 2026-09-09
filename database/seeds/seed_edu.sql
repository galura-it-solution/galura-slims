-- Seed Data Koleksi Buku Perpustakaan Edukasi untuk SLiMS EDU (senayan_edu)

-- 1. Penulis (mst_author)
INSERT IGNORE INTO `mst_author` (`author_id`, `author_name`, `authority_type`, `input_date`, `last_update`) VALUES
(101, 'Prof. Dr. Bambang Sudarsono, M.Sc.', 'p', NOW(), NOW()),
(102, 'Dr. Ir. Hendra Setiawan, M.T.', 'p', NOW(), NOW()),
(103, 'Dra. Sri Wahyuni, M.Pd.', 'p', NOW(), NOW()),
(104, 'Ahmad Fauzi, S.Si., M.Kom.', 'p', NOW(), NOW()),
(105, 'Rina Marlina, S.Pd., M.Hum.', 'p', NOW(), NOW()),
(106, 'Dr. Budi Santoso, M.Si.', 'p', NOW(), NOW()),
(107, 'Johnathan Miller, Ph.D.', 'p', NOW(), NOW()),
(108, 'Sarah Jenkins, M.Ed.', 'p', NOW(), NOW()),
(109, 'Prof. Dr. Suwandi Kartonegoro', 'p', NOW(), NOW()),
(110, 'Drs. Supriyanto, M.M.', 'p', NOW(), NOW()),
(111, 'Dewi Lestari Handayani, S.Sn.', 'p', NOW(), NOW()),
(112, 'Arif Rachman Hakim, S.T., M.Eng.', 'p', NOW(), NOW());

-- 2. Penerbit (mst_publisher)
INSERT IGNORE INTO `mst_publisher` (`publisher_id`, `publisher_name`, `input_date`, `last_update`) VALUES
(101, 'Penerbit Erlangga Edukasi', NOW(), NOW()),
(102, 'Pusat Kurikulum dan Perbukuan Kemendikbud', NOW(), NOW()),
(103, 'Informatika Bandung', NOW(), NOW()),
(104, 'Gramedia Widiasarana Indonesia (Grasindo)', NOW(), NOW()),
(105, 'Oxford University Press Indonesia', NOW(), NOW()),
(106, 'Balai Pustaka', NOW(), NOW()),
(107, 'Penerbit Andi Offset', NOW(), NOW());

-- 3. Tempat Terbit (mst_place)
INSERT IGNORE INTO `mst_place` (`place_id`, `place_name`, `input_date`, `last_update`) VALUES
(101, 'Jakarta', NOW(), NOW()),
(102, 'Bandung', NOW(), NOW()),
(103, 'Yogyakarta', NOW(), NOW()),
(104, 'Surabaya', NOW(), NOW());

-- 4. Topik / Subjek (mst_topic)
INSERT IGNORE INTO `mst_topic` (`topic_id`, `topic`, `topic_type`, `input_date`, `last_update`) VALUES
(101, 'Matematika Terapan', 't', NOW(), NOW()),
(102, 'Fisika Dasar', 't', NOW(), NOW()),
(103, 'Biologi Sel dan Molekuler', 't', NOW(), NOW()),
(104, 'Kimia Dasar', 't', NOW(), NOW()),
(105, 'Pemrograman Komputer', 't', NOW(), NOW()),
(106, 'Robotika & Otomasi', 't', NOW(), NOW()),
(107, 'Bahasa & Sastra Indonesia', 't', NOW(), NOW()),
(108, 'English for Academic Studies', 't', NOW(), NOW()),
(109, 'Sejarah Indonesia', 't', NOW(), NOW()),
(110, 'Geografi & Lingkungan', 't', NOW(), NOW()),
(111, 'Pendidikan Kewarganegaraan', 't', NOW(), NOW()),
(112, 'Ekonomi & Finansial', 't', NOW(), NOW()),
(113, 'Desain Komunikasi Visual', 't', NOW(), NOW()),
(114, 'Teknik Jaringan Komputer', 't', NOW(), NOW()),
(115, 'Ensiklopedi Sains Digital', 't', NOW(), NOW());

-- 5. Bibliografi Buku Edukasi (biblio)
INSERT INTO `biblio` (`biblio_id`, `gmd_id`, `title`, `edition`, `isbn_issn`, `publisher_id`, `publish_year`, `collation`, `series_title`, `call_number`, `language_id`, `publish_place_id`, `classification`, `notes`, `image`, `opac_hide`, `promoted`, `input_date`, `last_update`) VALUES
(101, 1, 'Matematika Terapan: Kalkulus, Aljabar Linier & Statistik untuk Siswa Vokasi', 'Cet. 2', '978-602-01-1001-1', 101, '2024', 'xxii, 380 hlm. : ilus. ; 25 cm.', 'Seri Edukasi Sains', '510.7 Sud m', 'id', 101, '510.7', 'Buku panduan lengkap matematika terapan yang memadukan teori kalkulus dasar, aljabar linier praktis, dan statistika aplikatif untuk studi sains dan vokasi.', NULL, 0, 1, NOW(), NOW()),
(102, 1, 'Fisika Eksperimental: Dari Mekanika Klasik Hingga Elektromagnetika Modern', 'Ed. Revisi', '978-602-01-1002-8', 101, '2023', 'xviii, 420 hlm. : ilus. ; 26 cm.', 'Sains Terpadu', '530.07 Hen f', 'id', 101, '530.07', 'Menjelaskan prinsip hukum gerak Newton, termodinamika, gelombang optik, dan elektromagnetika disertai panduan praktikum laboratorium sekolah.', NULL, 0, 1, NOW(), NOW()),
(103, 1, 'Biologi Sel, Genetika & Ekosistem Hayati Berkelanjutan', 'Cet. 1', '978-602-02-1003-5', 102, '2024', 'xiv, 340 hlm. : ilus. ; 25 cm.', 'Buku Sekolah Berstandar Nasional', '570.1 Sri b', 'id', 101, '570.1', 'Pembahasan mendalam struktur sel tumbuhan dan hewan, hukum pewarisan genetika Mendel, DNA rekombinan, serta kelestarian ekosistem lingkungan hidup.', NULL, 0, 1, NOW(), NOW()),
(104, 1, 'Kimia Dasar: Ikatan Kimia, Stoikiometri & Reaksi Larutan', 'Cet. 3', '978-602-03-1004-2', 104, '2023', 'xvi, 310 hlm. : ilus. ; 24 cm.', 'Pustaka Kimia Populer', '540 Bud k', 'id', 101, '540', 'Buku ajar kimia yang menyajikan konsep tabel periodik modern, ikatan ionik & kovalen, stoikiometri reaksi, termokimia, serta kesetimbangan asam-basa.', NULL, 0, 0, NOW(), NOW()),
(105, 1, 'Dasar-Dasar Algoritma & Logika Pemrograman untuk Pelajar', 'Cet. 1', '978-602-04-1005-9', 103, '2024', 'xii, 280 hlm. : ilus. ; 23 cm.', 'Teknologi Informasi & Komputasi', '005.1 Ahm d', 'id', 102, '005.1', 'Panduan pengenalan logika algoritma, flowchart, pseudocode, struktur data array/list, dan pengenalan sintaks bahasa pemrograman modern.', NULL, 0, 1, NOW(), NOW()),
(106, 1, 'Pengantar Robotika dan Otomasi Cerdas untuk Sekolah Kejuruan', 'Cet. 1', '978-602-04-1006-6', 103, '2024', 'xiv, 260 hlm. : ilus. ; 24 cm.', 'Teknologi Otomasi', '629.892 Ari p', 'id', 102, '629.892', 'Membahas perancangan mikrokontroler (Arduino/ESP32), sensor ultrasonik & inframerah, aktuator motor servo, dan logika robotika beroda.', NULL, 0, 1, NOW(), NOW()),
(107, 1, 'Keterampilan Menulis Akademik dan Retorika Bahasa Indonesia', 'Cet. 2', '978-602-05-1007-3', 106, '2023', 'xx, 290 hlm. ; 21 cm.', 'Seri Bahasa dan Sastra', '410 Rin k', 'id', 101, '410', 'Buku ajar penyusunan karya tulis ilmiah, penalaran paragraf eksposisi/argumentasi, kaidah EYD terbaru, dan keterampilan presentasi retoris.', NULL, 0, 0, NOW(), NOW()),
(108, 1, 'Academic English Proficiency: Reading Comprehension & Essay Writing', '3rd Edition', '978-019-01-1008-0', 105, '2024', 'x, 320 p. : ill. ; 26 cm.', 'Global Language Series', '428 Joh a', 'en', 101, '428', 'Comprehensive textbook for English learners focusing on critical academic reading, vocabulary enhancement, syntax mastery, and argumentative essay drafting.', NULL, 0, 0, NOW(), NOW()),
(109, 1, 'Nusantara: Jejak Peradaban Jalur Rempah dan Pembentukan Bangsa', 'Cet. 4', '978-602-06-1009-7', 106, '2023', 'xxviii, 460 hlm. : peta ; 24 cm.', 'Sejarah Nasional', '959.8 Suw n', 'id', 101, '959.8', 'Kajian komprehensif dinamika maritim Nusantara, kerajaan Hindu-Buddha & Islam, masa kolonialisme, revolusi kemerdekaan, hingga Indonesia kontemporer.', NULL, 0, 1, NOW(), NOW()),
(110, 1, 'Geografi Lingkungan dan Mitigasi Bencana Kebumian Indonesia', 'Cet. 1', '978-602-07-1010-3', 107, '2024', 'xviii, 350 hlm. : peta, graf. ; 25 cm.', 'Geosains Terapan', '910.02 Sup g', 'id', 103, '910.02', 'Menelaah geomorfologi kepulauan Indonesia, dinamika cincin api vulkanisme, klimatologi tropis, serta sistem mitigasi bencana gempa bumi dan tsunami.', NULL, 0, 0, NOW(), NOW()),
(111, 1, 'Pendidikan Kewarganegaraan: Etika Berdemokrasi di Era Digital', 'Cet. 2', '978-602-02-1011-0', 102, '2024', 'xii, 240 hlm. ; 23 cm.', 'Pilar Kebangsaan', '323.6 Sri p', 'id', 101, '323.6', 'Membekali generasi muda dengan kesadaran hak dan kewajiban konstitusional, literasi hukum digital, nilai-nilai Pancasila, dan integrasi nasional.', NULL, 0, 0, NOW(), NOW()),
(112, 1, 'Ekonomi Kreatif dan Literasi Finansial Generasi Muda', 'Cet. 1', '978-602-01-1012-7', 101, '2024', 'xvi, 275 hlm. : graf. ; 23 cm.', 'Ekonomi Terapan', '330.1 Fau e', 'id', 101, '330.1', 'Buku panduan mengelola keuangan pribadi, prinsip investasi legal, pemahaman siklus inflasi, dan perintisan wirausaha kreatif berbasis teknologi.', NULL, 0, 0, NOW(), NOW()),
(113, 1, 'Desain Grafis dan Komunikasi Visual: Dari Konsep ke Produksi Karya', 'Cet. 1', '978-602-04-1013-4', 103, '2023', 'xii, 230 hlm. : ilus. berwarna ; 26 cm.', 'Kreatif Visual', '741.6 Dew d', 'id', 102, '741.6', 'Pedoman prinsip desain visual: tipografi, teori warna, hierarki layout, branding identitas visual, dan pengoperasian perangkat lunak desain vektor.', NULL, 0, 0, NOW(), NOW()),
(114, 1, 'Administrasi Infrastruktur Jaringan Komputer dan Keamanan Server', 'Cet. 2', '978-602-04-1014-1', 103, '2024', 'xviii, 390 hlm. : ilus. ; 25 cm.', 'Jaringan & Server', '004.6 Ari a', 'id', 102, '004.6', 'Konfigurasi routing statis & dinamis, VLAN, firewall filtering, DNS, web server Linux, dan manajemen bandwidth jaringan lokal maupun WAN.', NULL, 0, 1, NOW(), NOW()),
(115, 1, 'Ensiklopedi Sains Populer: Penemuan Abad 21 yang Mengubah Dunia', 'Cet. 1', '978-602-01-1015-8', 104, '2024', 'xxiv, 510 hlm. : ilus. berwarna ; 28 cm.', 'Ensiklopedi Sains', '503 Sud e', 'id', 101, '503', 'Rangkuman lengkap penemuan sains terobosan: fusi nuklir, komputasi kuantum, terapi gen CRISPR, eksplorasi luar angkasa Mars, dan energi terbarukan.', NULL, 0, 1, NOW(), NOW())
ON DUPLICATE KEY UPDATE `title`=VALUES(`title`), `last_update`=NOW();

-- 6. Relasi Penulis (biblio_author)
DELETE FROM `biblio_author` WHERE `biblio_id` BETWEEN 101 AND 115;
INSERT INTO `biblio_author` (`biblio_id`, `author_id`, `level`) VALUES
(101, 101, 1),
(102, 102, 1),
(103, 103, 1),
(104, 106, 1),
(105, 104, 1),
(106, 112, 1),
(107, 105, 1),
(108, 107, 1),
(108, 108, 2),
(109, 109, 1),
(110, 110, 1),
(111, 103, 1),
(112, 104, 1),
(113, 111, 1),
(114, 112, 1),
(115, 101, 1),
(115, 102, 2);

-- 7. Relasi Topik (biblio_topic)
DELETE FROM `biblio_topic` WHERE `biblio_id` BETWEEN 101 AND 115;
INSERT INTO `biblio_topic` (`biblio_id`, `topic_id`, `level`) VALUES
(101, 101, 1),
(102, 102, 1),
(103, 103, 1),
(104, 104, 1),
(105, 105, 1),
(106, 106, 1),
(107, 107, 1),
(108, 108, 1),
(109, 109, 1),
(110, 110, 1),
(111, 111, 1),
(112, 112, 1),
(113, 113, 1),
(114, 114, 1),
(115, 115, 1);

-- 8. Eksemplar Buku Fisik (item) untuk Perpustakaan EDU
DELETE FROM `item` WHERE `biblio_id` BETWEEN 101 AND 115;
INSERT INTO `item` (`item_id`, `biblio_id`, `coll_type_id`, `item_code`, `inventory_code`, `received_date`, `supplier_id`, `order_no`, `location_id`, `item_status_id`, `site`, `source`, `price`, `price_currency`, `input_date`, `last_update`) VALUES
(101, 101, 3, 'EDU-MAT-001', 'INV/EDU/2024/001', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 01', 1, 95000, 'Rupiah', NOW(), NOW()),
(102, 101, 3, 'EDU-MAT-002', 'INV/EDU/2024/002', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 01', 1, 95000, 'Rupiah', NOW(), NOW()),
(103, 102, 3, 'EDU-FIS-001', 'INV/EDU/2024/003', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 02', 1, 105000, 'Rupiah', NOW(), NOW()),
(104, 102, 3, 'EDU-FIS-002', 'INV/EDU/2024/004', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 02', 1, 105000, 'Rupiah', NOW(), NOW()),
(105, 103, 3, 'EDU-BIO-001', 'INV/EDU/2024/005', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 03', 1, 88000, 'Rupiah', NOW(), NOW()),
(106, 104, 3, 'EDU-KIM-001', 'INV/EDU/2024/006', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sains 03', 1, 82000, 'Rupiah', NOW(), NOW()),
(107, 105, 3, 'EDU-KOM-001', 'INV/EDU/2024/007', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Teknologi 01', 1, 78000, 'Rupiah', NOW(), NOW()),
(108, 105, 3, 'EDU-KOM-002', 'INV/EDU/2024/008', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Teknologi 01', 1, 78000, 'Rupiah', NOW(), NOW()),
(109, 106, 3, 'EDU-ROB-001', 'INV/EDU/2024/009', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Teknologi 02', 1, 115000, 'Rupiah', NOW(), NOW()),
(110, 107, 1, 'EDU-IND-001', 'INV/EDU/2024/010', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Bahasa 01', 1, 72000, 'Rupiah', NOW(), NOW()),
(111, 108, 2, 'EDU-ENG-001', 'INV/EDU/2024/011', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Bahasa 02', 1, 120000, 'Rupiah', NOW(), NOW()),
(112, 109, 1, 'EDU-SEJ-001', 'INV/EDU/2024/012', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sosial 01', 1, 135000, 'Rupiah', NOW(), NOW()),
(113, 110, 2, 'EDU-GEO-001', 'INV/EDU/2024/013', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sosial 02', 1, 90000, 'Rupiah', NOW(), NOW()),
(114, 111, 3, 'EDU-PKN-001', 'INV/EDU/2024/014', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sosial 03', 1, 65000, 'Rupiah', NOW(), NOW()),
(115, 112, 2, 'EDU-EKO-001', 'INV/EDU/2024/015', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Sosial 04', 1, 75000, 'Rupiah', NOW(), NOW()),
(116, 113, 2, 'EDU-DKV-001', 'INV/EDU/2024/016', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Seni 01', 1, 110000, 'Rupiah', NOW(), NOW()),
(117, 114, 3, 'EDU-NET-001', 'INV/EDU/2024/017', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Teknologi 03', 1, 125000, 'Rupiah', NOW(), NOW()),
(118, 115, 2, 'EDU-ENS-001', 'INV/EDU/2024/018', CURDATE(), '0', 'PO-EDU-2024-01', 'SL', '0', 'Rak Referensi 01', 1, 210000, 'Rupiah', NOW(), NOW())
ON DUPLICATE KEY UPDATE `last_update`=NOW();
