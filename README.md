# 🏥 Torul MYO Hastane Bilgi Yönetim Sistemi (HBYS) Projesi - Final Sunum Versiyonu

## 👨‍💻 Proje Sahibi
* **Adı Soyadı:** Hüseyin Akın
* **Bölüm:** Bilgisayar Teknolojileri
* **Okul:** Torul Meslek Yüksekokulu

---

## ✨ Proje Tanıtımı ve Mimari (Mimics Real-World System)

Bu proje, bir hastane ortamındaki temel süreçleri yönetmek üzere, modern web teknolojileri ve güvenli veritabanı standartları kullanılarak geliştirilmiştir. Projenin ana hedefi, bir öğrenci projesinde **güvenlik, analiz ve tam işlevsellik (Full-Stack CRUD)** gösterimini birleştirmektir.

### ⚙️ Temel Teknoloji Yığını (Tech Stack)

| Kategori | Teknoloji | Kullanım Alanı |
| :--- | :--- | :--- |
| **Backend** | **Python (Flask)** | Uygulama mantığı, Routing (Yol atama) ve Veritabanı Yönetimi (ORM yerine manuel SQL). |
| **Veritabanı**| **Microsoft SQL Server** | Kurumsal düzeyde veri saklama ve ilişkilendirme. |
| **Önyüz (Frontend)** | **HTML5, CSS3, Bootstrap 5** | Responsive ve kurumsal tasarım (Gümüşhane Üniversitesi Kimliği). |
| **Analiz/Grafik**| **Chart.js (JavaScript)** | Dashboard üzerinde dinamik veri görselleştirme. |
| **Güvenlik** | **Werkzeug.security** | Şifre Hash'leme (scrypt algoritması). |

---

## 🚀 Projenin İleri Düzey Fonksiyonları ve Öğrenilen Konular

Bu projeyi diğerlerinden ayıran ve bir yazılım geliştiricisi olarak yetkinliğinizi gösteren en kritik özellikler aşağıdadır:

### 1. Veritabanı Mimarisi ve Güvenliği
* **Şifre Güvenliği (Profesyonel Standard):** Kullanıcı şifreleri veritabanına düz metin olarak değil, `werkzeug.security` kütüphanesi ile **scrypt** algoritması kullanılarak **Hash'lenmiş** şekilde kaydedilmiştir.
* **Schema (Şema) Yönetimi:** Proje, kurulum ve veri taşıma kolaylığı için tek bir **`.sql`** script dosyası (`TorulMYOHastane_Setup.sql`) olarak paketlenmiştir.
* **Kompleks Sorgular:** Hasta-Randevu ilişkileri (`JOIN`) ve Dashboard için **dinamik sayım/filtreleme** (`COUNT`, `GROUP BY`, `CAST(GETDATE())`) sorguları etkin kullanılmıştır.

### 2. Yönetim ve Raporlama (UX)
* **Dinamik Dashboard:** Ana sayfada **Chart.js** ile oluşturulmuş, anlık veritabanı verilerine dayalı Randevu Dağılım Grafiği sunulur. (Veri Analizi Yeteneği)
* **Muayene ve Rapor Çıktısı:** Randevular, Muayene/Tanı girişi (`UPDATE` işlemi) ile kapatılır. Tamamlanan randevular için **yazıcıya hazır (Print-Ready)** ve kurumsal kimliğe uygun **Reçete Çıktısı** (PDF formatını taklit eden HTML) oluşturulmuştur. (Raporlama Yeteneği)
* **Tam CRUD İşlemleri:** Hasta **Ekleme**, **Görüntüleme**, **Düzenleme (UPDATE)** ve Randevu **Arama/Silme** işlemleri eksiksizdir.

---

## 🛠️ Kurulum ve Çalıştırma Adımları

Projenin çalıştırılabilmesi için aşağıdaki adımların sırasıyla tamamlanması gerekmektedir:

1.  **Gerekli Python Kütüphanelerini Kurunuz:**
    ```bash
    pip install flask pyodbc werkzeug
    ```

2.  **Veritabanını Oluşturunuz:**
    * SQL Server Management Studio'da (SSMS) `TorulMYOHastane_Setup.sql` dosyasını açıp **Execute** ederek tabloları ve `admin` kullanıcısını kurunuz.

3.  **Uygulamayı Başlatınız:**
    ```bash
    python app.py
    ```

### Giriş Bilgileri

| Kullanıcı Adı | Şifre |
| :--- | :--- |
| **admin** | **1234** |
