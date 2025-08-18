Bu, harika ve çok detaylı bir README dosyası\! Kullanıcılar için her şey açık ve anlaşılır. Özellikle karşılaştırmalı görsel ve farklı kullanım senaryoları çok faydalı.

Ancak, görsellerin tüm kullanıcılar tarafından görülebilmesi için yerel dosya yolunu (`/Users/ibrahimgulmez/...`) **GitHub'daki genel bir URL ile değiştirmen gerekiyor.**

GitHub, doğrudan yerel dosya yollarını (bilgisayarındaki C: veya D: sürücüsü gibi) göstermez. Görsellerin README dosyasında görünmesi için şu adımları izlemelisin:

1.  Projenin ana dizininde `assets` (veya `images` gibi) adında bir klasör oluştur.
2.  `Screenshot 2025-08-18 at 15.02.24.png` ve `Screenshot 2025-08-18 at 15.02.51.png` dosyalarını bu klasörün içine taşı.
3.  Projeni bu değişikliklerle birlikte GitHub'a yükle (`git add .`, `git commit -m "add images"`, `git push`).
4.  README dosyasındaki resim yollarını, GitHub'daki yeni konumlarına işaret edecek şekilde güncelle.

İşte bu değişiklikleri içeren, düzenlenmiş ve son haliyle README içeriği:

-----

# 🎬 Offline Video Subtitle Generator

\<div align="center"\>

**AI destekli, tamamen offline altyazı oluşturma aracı**

OpenAI Whisper kullanarak videolarınıza profesyonel altyazılar ekleyin - internet bağlantısı gerektirmez\!

\</div\>

-----

## 🎬 Orijinal ve Altyazılı Görsel Karşılaştırması

\<table\>
\<tr\>
\<td align="center"\>
\<strong\>Orijinal Görsel\</strong\>\<br/\>
\<img src="assets/orijinal\_screenshot.png" width="350" alt="Orijinal Görsel" /\>
\</td\>
\<td align="center"\>
\<strong\>Altyazılı Görsel\</strong\>\<br/\>
\<img src="assets/altyazili\_screenshot.png" width="350" alt="Altyazılı Görsel" /\>
\</td\>
\</tr\>
\</table\>

-----

## ✨ Özellikler

  - 🤖 **AI Destekli Transkripsiyon**: OpenAI Whisper ve faster-whisper desteği
  - 🌐 **Tamamen Offline**: İnternet bağlantısı gerektirmez
  - 🎨 **7 Profesyonel Altyazı Stili**: Cinema, YouTube, Netflix ve daha fazlası
  - 📱 **Web Arayüzü**: Flask tabanlı kullanıcı dostu arayüz
  - 📄 **Çoklu Format**: SRT, VTT ve video çıktı formatları
  - 🎯 **Yüksek Doğruluk**: Gelişmiş ses işleme algoritmaları
  - ⚡ **Hızlı İşlem**: GPU desteği ile optimize edilmiş performans

-----

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler

  - Python 3.7 veya üzeri
  - FFmpeg (sistem PATH'inde bulunmalı)
  - GPU desteği için CUDA (opsiyonel)

### Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/username/offline-subtitle-tool.git
cd offline-subtitle-tool

# Sanal ortam oluşturun
python3 -m venv .venv

# Sanal ortamı aktifleştirin
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Gerekli paketleri yükleyin
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

⚠️ **MacOS ve bazı Python kurulumlarında** doğrudan `pip install` çalışmayabilir. Bu nedenle `python3 -m pip install` kullanmak daha güvenlidir.

### FFmpeg Kurulumu

  - **Windows**: `choco install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`

### 🎯 Kullanım

#### Komut Satırı

```bash
# Basit kullanım
python3 app.py -i "video.mp4"

# Belirli çıktı formatları
python3 app.py -i "video.mp4" --formats video,srt,vtt

# Özel altyazı stili
python3 app.py -i "video.mp4" --style cinema

# Çıktı dizini belirtme
python3 app.py -i "video.mp4" -o "output_folder"

# Gelişmiş ayarlar
python3 app.py -i "video.mp4" --model medium --device cuda --style netflix
```

#### Web Arayüzü

```bash
# Web arayüzünü başlatın
python3 web_app.py

# Tarayıcınızda açın: http://localhost:5000
```

### 🔧 Sorun Giderme

  - **pip bulunamıyor:** `.venv/bin/pip` veya `python3 -m pip` kullanın.
  - **FFmpeg bulunamadı:** Terminalde `ffmpeg -version` ile kontrol edin.
  - **CUDA hatası:** `--device cpu` parametresi ile CPU kullanın.
  - **Bellek hatası:** Daha küçük model (`tiny`) ile çalıştırın.

-----

## 🌍 Açık Kaynak

Bu proje **açık kaynak** ve **herkes tarafından serbestçe kullanılabilir.** Katkılarınız ve geri bildirimleriniz memnuniyetle karşılanır.

  - **LinkedIn:** [İbrahim Gülmez](https://www.google.com/search?q=https://www.linkedin.com/in/ibrahimgulmez/)
  - **Kişisel site:** [Portfolio](https://www.google.com/search?q=https://www.ibrahimgulmez.com)

-----

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın\!

-----

Bu son düzenleme ile görseller artık herkes tarafından görülebilir. Ek olarak, kurulumu daha da basitleştiren tek bir komut bloğu eklememi ister misin?