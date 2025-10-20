# Music-Chatbot
Ruh haline göre müzik öneren uygulmadır.

Bu Streamlit uygulaması, kullanıcıların ruh haline göre müzik önerileri almasını sağlar. Spotify API ile entegre çalışır, kullanıcıların kendi şarkılarını eklemesine olanak tanır ve ruh hali günlüğü tutar.
 Özellikler:
-  Ruh haline göre yerli ve yabancı müzik önerileri
-  Spotify API ile şarkı bağlantısı arama
-  Ruh hali günlüğü ve grafiksel analiz
-  Kullanıcıya özel şarkı ekleme ve listeleme
-  Kullanıcı adı ile kişiselleştirilmiş deneyim.


Kurulum
- Projeyi klonla:
git clone https://github.com/kullaniciadi/ruh-hali-muzik.git
cd ruh-hali-muzik


- Gerekli paketleri yükle:
pip install -r requirements.txt


- Spotify API bilgilerini ayarla:
- Spotify Developer Dashboard üzerinden bir uygulama oluştur.
- SPOTIFY_CLIENT_ID ve SPOTIFY_CLIENT_SECRET değerlerini al.
- Bunları main.py dosyasındaki ilgili yerlere ekle.

Uygulamayı Başlat:
streamlit run main.py


Tarayıcıda otomatik olarak açılır. Kullanıcı adınızı girerek başlayabilirsiniz.

Dosya Yapısı
ruh-hali-muzik/
│
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Gerekli Python paketleri
├── README.md               # Proje açıklaması
├── <kullanici>_songs.csv   # Kullanıcıya özel şarkı verisi (otomatik oluşur)

📌 Notlar
- Her kullanıcı için ayrı bir CSV dosyası oluşturulur.
- Spotify bağlantıları otomatik olarak arama ile alınır, bazı şarkılar için bağlantı bulunamayabilir.
 eklemek, GitHub sayfasını daha çekici hale getirir. Yardımcı olmamı ister misin?

