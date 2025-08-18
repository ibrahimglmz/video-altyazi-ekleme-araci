# 🎬 Offline Professional Video Subtitle Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI destekli, tamamen offline çalışan profesyonel altyazı oluşturma aracı**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Web Arayüzü](#-web-arayüzü) • [Örnekler](#-kullanım-örnekleri)

</div>

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Komut Satırı Kullanımı](#-komut-satırı-kullanımı)
- [Web Arayüzü](#-web-arayüzü)
- [Desteklenen Formatlar](#-desteklenen-formatlar)
- [Altyazı Stilleri](#-altyazı-stilleri)
- [Kullanım Örnekleri](#-kullanım-örnekleri)
- [Sorun Giderme](#-sorun-giderme)
- [SSS](#-sık-sorulan-sorular)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## ✨ Özellikler

### 🎯 Ana Özellikler
- **🤖 AI Destekli Transkripsiyon**: OpenAI Whisper ile yüksek kaliteli ses-metin dönüşümü
- **🌐 Tamamen Offline**: İnternet bağlantısı gerektirmez, verileriniz güvende
- **⚡ GPU Hızlandırma**: CUDA destekli GPU'larda hızlı işleme
- **🎨 Profesyonel Stiller**: 7 farklı önceden tanımlı altyazı stili
- **📱 Web Arayüzü**: Flask tabanlı modern, kullanıcı dostu web arayüzü
- **🔄 Toplu İşlem**: Birden fazla dosyayı aynı anda işleme
- **🎵 Ses İyileştirme**: Otomatik ses kalitesi optimizasyonu

### 📄 Çıktı Formatları
- **SRT**: Yaygın altyazı formatı (SubRip)
- **VTT**: Web uyumlu altyazı formatı (WebVTT)
- **ASS**: Gelişmiş stil desteği (Advanced SubStation Alpha)
- **TXT**: Düz metin transkripsiyon
- **Video**: Altyazılı video dosyası (hard-coded subtitles)

### 🎬 Medya Desteği
- **Video**: MP4, AVI, MOV, MKV, WebM, FLV, M4V, MPG, MPEG
- **Audio**: MP3, WAV, FLAC, AAC, OGG, M4A, OPUS

---

## 🔧 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Python**: 3.7 veya üzeri
- **RAM**: 4GB (8GB önerilen)
- **Depolama**: 2GB boş alan (model dosyaları için)

### Önerilen Gereksinimler
- **RAM**: 16GB (büyük dosyalar için)
- **GPU**: NVIDIA GPU (CUDA desteği)
- **Depolama**: SSD (hızlı işleme için)

### Gerekli Yazılımlar
- **FFmpeg**: Ses/video işleme için
- **Python**: 3.7+ sürümü
- **Git**: Kurulum için (opsiyonel)

---

## 📦 Kurulum

### 1️⃣ Depoyu İndirin

```bash
# Git ile klonlama
git clone https://github.com/username/offline-subtitle-tool.git
cd offline-subtitle-tool

# Veya ZIP dosyası olarak indirin ve açın
```

### 2️⃣ FFmpeg Kurulumu

#### Windows
```bash
# Chocolatey ile
choco install ffmpeg

# Scoop ile
scoop install ffmpeg

# Manuel kurulum: https://ffmpeg.org/download.html
```

#### macOS
```bash
# Homebrew ile
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3️⃣ Python Bağımlılıkları

```bash
# Sanal ortam oluşturun (önerilen)
python -m venv venv

# Sanal ortamı etkinleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Veya manuel kurulum:
pip install openai-whisper faster-whisper torch torchaudio flask pydub tqdm
```

### 4️⃣ Kurulum Doğrulama

```bash
# Komut satırı aracını test edin
python app.py --help

# Web arayüzünü başlatın
python server.py
```

---

## 🚀 Hızlı Başlangıç

### Komut Satırından
```bash
# Basit kullanım
python app.py -i video.mp4

# Gelişmiş kullanım
python app.py -i video.mp4 --formats srt,vtt,video --style cinema --language tr --gpu
```

### Web Arayüzünden
1. Terminal/CMD'den `python server.py` çalıştırın
2. Tarayıcıda `http://127.0.0.1:5000` adresine gidin
3. Dosyanızı yükleyin ve ayarları yapın
4. "Altyazı Oluştur" butonuna tıklayın

---

## 💻 Komut Satırı Kullanımı

### Temel Komut Yapısı
```bash
python app.py [SEÇENEKLER] -i DOSYA_YOLU
```

### 📝 Tüm Parametreler

| Parametre | Kısa | Açıklama | Varsayılan |
|-----------|------|----------|------------|
| `--input` | `-i` | Giriş dosyası/klasörü | *(Zorunlu)* |
| `--output` | `-o` | Çıktı klasörü | `output` |
| `--formats` | - | Çıktı formatları (virgülle ayrılmış) | `srt,video` |
| `--style` | - | Altyazı stili | `default` |
| `--language` | - | Dil kodu (tr, en, auto) | `auto` |
| `--model` | - | Whisper model boyutu | `base` |
| `--batch` | - | Toplu işlem modu | `False` |
| `--gpu` | - | GPU hızlandırma | `False` |
| `--include-timestamps` | - | TXT'de zaman damgası | `False` |
| `--no-audio-enhance` | - | Ses iyileştirmesini kapat | `False` |
| `--overwrite` | - | Mevcut dosyaları üzerine yaz | `False` |

### 🔤 Whisper Model Boyutları

| Model | Boyut | Hız | Kalite | RAM Kullanımı |
|-------|-------|-----|--------|---------------|
| `tiny` | 39MB | ⚡⚡⚡⚡ | ⭐⭐ | ~1GB |
| `base` | 74MB | ⚡⚡⚡ | ⭐⭐⭐ | ~1GB |
| `small` | 244MB | ⚡⚡ | ⭐⭐⭐⭐ | ~2GB |
| `medium` | 769MB | ⚡ | ⭐⭐⭐⭐⭐ | ~5GB |
| `large` | 1550MB | 🐌 | ⭐⭐⭐⭐⭐ | ~10GB |

---

## 🌐 Web Arayüzü

### Başlatma
```bash
python server.py
```
Tarayıcıda `http://127.0.0.1:5000` adresine gidin.

### 🎮 Özellikler
- **📁 Sürükle-Bırak**: Dosya yükleme
- **⚙️ Kolay Ayarlar**: Form tabanlı konfigürasyon
- **📊 İlerleme Takibi**: Gerçek zamanlı işlem durumu
- **📥 Hızlı İndirme**: Tek tıkla dosya indirme
- **🗑️ Dosya Yönetimi**: Upload/output temizleme
- **📱 Responsive**: Mobil uyumlu tasarım

### 🎨 Arayüz Görünümü
- **Koyu Tema**: Modern, göz dostu tasarım
- **Renk Kodları**: Durum mesajları (başarı: yeşil, hata: kırmızı)
- **İkonlar**: Görsel ipuçları
- **Animasyonlar**: Smooth geçişler

---

## 📋 Desteklenen Formatlar

### 🎬 Video Formatları
| Format | Uzantı | Açıklama |
|--------|--------|----------|
| MP4 | `.mp4` | En yaygın video formatı |
| AVI | `.avi` | Klasik video formatı |
| MOV | `.mov` | Apple QuickTime |
| MKV | `.mkv` | Matroska video |
| WebM | `.webm` | Web optimized |
| FLV | `.flv` | Flash video |
| M4V | `.m4v` | iTunes video |

### 🎵 Audio Formatları
| Format | Uzantı | Açıklama |
|--------|--------|----------|
| MP3 | `.mp3` | En yaygın ses formatı |
| WAV | `.wav` | Kayıpsız ses |
| FLAC | `.flac` | Kayıpsız sıkıştırma |
| AAC | `.aac` | Gelişmiş ses kodlama |
| OGG | `.ogg` | Açık kaynak ses |
| M4A | `.m4a` | Apple ses formatı |
| OPUS | `.opus` | Modern ses kodlama |

---

## 🎨 Altyazı Stilleri

### 🎯 Önceden Tanımlı Stiller

#### **Default** - Klasik
```css
• Font: System default (Arial/DejaVu Sans)
• Boyut: 24px
• Renk: Beyaz (#FFFFFF)
• Çerçeve: Siyah, 2px
• Arka plan: Yarı saydam siyah
• Hizalama: Orta-alt
```

#### **Bold** - Kalın ve Belirgin
```css
• Font: System default
• Boyut: 28px (büyük)
• Renk: Beyaz
• Çerçeve: Kalın siyah (3px)
• Arka plan: Koyu gri, yoğun
• Karakter/satır: 42
```

#### **Elegant** - Zarif
```css
• Font: Times New Roman
• Boyut: 26px
• Renk: Bej (#F5F5DC)
• Çerçeve: İnce gri
• Arka plan: Koyu gri, şeffaf
• Marjin: Geniş (60px)
```

#### **Cinema** - Sinema Tarzı
```css
• Font: Arial
• Boyut: 32px (çok büyük)
• Renk: Altın (#FFD700)
• Çerçeve: Siyah
• Arka plan: Mat siyah
• Efekt: Gölge (3px offset)
```

#### **Modern** - Teknolojik
```css
• Font: Roboto/Arial
• Boyut: 24px
• Renk: Matrix yeşili (#00FF41)
• Çerçeve: Koyu gri
• Arka plan: Teknolojik koyu
• Stil: Futuristik
```

#### **Minimal** - Sade
```css
• Font: System default
• Boyut: 20px (küçük)
• Renk: Beyaz
• Çerçeve: Yok
• Arka plan: Çok az şeffaf
• Karakter/satır: 55 (uzun)
```

#### **Terminal** - Kod Stili
```css
• Font: Courier New/Monospace
• Boyut: 22px
• Renk: Terminal yeşili (#00FF00)
• Çerçeve: Koyu yeşil
• Arka plan: Siyah
• Hizalama: Sol
• Stil: Monospace
```

---

## 🔧 Kullanım Örnekleri

### 📺 Temel Video İşleme
```bash
# Basit altyazı oluşturma
python app.py -i film.mp4

# Sadece SRT formatı
python app.py -i film.mp4 --formats srt

# Türkçe dil zorunlu
python app.py -i film.mp4 --language tr
```

### 🎭 Stil Örnekleri
```bash
# Sinema stili altyazı
python app.py -i film.mp4 --style cinema --formats video,srt

# Zarif stil + ASS formatı
python app.py -i belgesel.mp4 --style elegant --formats ass,video

# Terminal stili (kodlama videoları için)
python app.py -i tutorial.mp4 --style terminal --formats srt,txt
```

### ⚡ Performans Optimizasyonu
```bash
# GPU hızlandırma
python app.py -i film.mp4 --gpu --model large

# Hızlı işlem (tiny model)
python app.py -i video.mp4 --model tiny --no-audio-enhance

# Yüksek kalite (large model)
python app.py -i film.mp4 --model large --style cinema
```

### 📁 Toplu İşlem
```bash
# Klasördeki tüm videoları işle
python app.py -i ./videolar --batch --formats srt,vtt

# Farklı çıktı klasörü
python app.py -i ./medya --batch -o ./altyazilar --style modern
```

### 🔊 Ses Dosyaları
```bash
# Podcast transkripsiyon
python app.py -i podcast.mp3 --formats txt --include-timestamps

# Müzik transkripsiyon
python app.py -i sarki.wav --language tr --formats srt,txt
```

### 🌍 Çoklu Dil Desteği
```bash
# Otomatik dil tespiti
python app.py -i video.mp4 --language auto

# İngilizce zorunlu
python app.py -i english-video.mp4 --language en

# İspanyolca
python app.py -i spanish-film.mp4 --language es
```

### 📋 Tam Özellik Örneği
```bash
python app.py \
  -i interview.mp4 \
  -o ./output/interview \
  --formats video,srt,vtt,ass,txt \
  --style cinema \
  --language auto \
  --model medium \
  --gpu \
  --include-timestamps \
  --overwrite
```

---

## 🐛 Sorun Giderme

### ❌ Yaygın Hatalar ve Çözümler

#### **"ffmpeg not found"**
```bash
# Çözüm: FFmpeg yüklemeyi kontrol edin
ffmpeg -version

# Windows PATH'e ekleme
set PATH=%PATH%;C:\ffmpeg\bin

# Yeniden yükleme
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg  
# Linux: sudo apt install ffmpeg
```

#### **"CUDA out of memory"**
```bash
# Çözüm 1: CPU kullanın
python app.py -i video.mp4  # --gpu bayrağını kaldırın

# Çözüm 2: Küçük model kullanın
python app.py -i video.mp4 --gpu --model tiny

# Çözüm 3: Ses iyileştirmeyi kapatın
python app.py -i video.mp4 --gpu --no-audio-enhance
```

#### **"No audio stream found"**
```bash
# Video dosyasının ses kanalı olduğunu kontrol edin
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name video.mp4

# Ses kanalı olmayan videolar için harici ses ekleyin
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4
```

#### **"Permission denied"**
```bash
# Windows: Yönetici olarak çalıştırın
# Linux/macOS: Dosya izinlerini kontrol edin
chmod +x app.py
sudo chown -R $USER:$USER ./output
```

#### **Model İndirme Sorunları**
```bash
# Model klasörünü temizleyin
rm -rf ~/.cache/whisper/

# Manuel model indirme
python -c "import whisper; whisper.load_model('base')"
```

### 🔍 Debug Modu
```bash
# Detaylı log çıktısı
python app.py -i video.mp4 --verbose

# FFmpeg debug
export FFREPORT=file=ffmpeg.log:level=32
python app.py -i video.mp4
```

### 💾 Bellek Sorunları
```bash
# Büyük dosyalar için
# 1. Küçük model kullanın
python app.py -i big-file.mp4 --model tiny

# 2. Ses iyileştirmeyi kapatın  
python app.py -i big-file.mp4 --no-audio-enhance

# 3. Dosyayı parçalara bölün
ffmpeg -i big-file.mp4 -t 00:10:00 -c copy part1.mp4
ffmpeg -i big-file.mp4 -ss 00:10:00 -c copy part2.mp4
```

---

## ❓ Sık Sorulan Sorular

### **Q: İnternet bağlantısı gerekli mi?**
A: Hayır, ilk model indirildikten sonra tamamen offline çalışır.

### **Q: Hangi diller destekleniyor?**
A: Whisper 99 dili destekler: tr, en, es, fr, de, it, pt, ru, ja, ko, zh, ar ve daha fazlası.

### **Q: GPU gereksinimleri neler?**
A: NVIDIA GPU (GTX 1060 veya üzeri) ve CUDA 11.0+ gerekir. AMD GPU desteklenmiyor.

### **Q: Maksimum dosya boyutu?**
A: Teorik limit yok, ancak RAM'inize bağlı. 8GB RAM ile ~2 saatlik video işleyebilirsiniz.

### **Q: Altyazı kalitesini artırmak için?**
A: `--model large` kullanın, ses iyileştirmeyi açık tutun, yüksek kaliteli ses dosyası kullanın.

### **Q: Çoklu hoparlör desteği var mı?**
A: Evet, Whisper konuşmacıları otomatik tanir, ancak isim etiketlemez.

### **Q: Batch işlem sırasında hata olursa?**
A: Diğer dosyalar işlenmeye devam eder. Hatalı dosyalar logda gösterilir.

### **Q: ASS dosyaları neden bu kadar büyük?**
A: ASS formatı stil bilgilerini içerir. Sadece metin için SRT/TXT kullanın.

### **Q: Web arayüzü diğer cihazlardan erişilebilir mi?**
A: Varsayılan olarak hayır (127.0.0.1). `app.run(host="0.0.0.0")` ile ağdan erişebilirsiniz.

### **Q: Timestamp hassasiyeti nedir?**
A: Whisper milisaniye hassasiyetinde zaman damgaları üretir.

---

## 📊 Performans Kıyaslama

### 💻 Test Sistemleri
**Sistem A**: Intel i7-10700K, 32GB RAM, RTX 3070  
**Sistem B**: AMD Ryzen 5 3600, 16GB RAM, CPU only

### ⏱️ İşlem Süreleri (10 dakikalık video)

| Model | Sistem A (GPU) | Sistem A (CPU) | Sistem B (CPU) |
|-------|---------------|----------------|----------------|
| tiny | 30s | 1m 30s | 2m 15s |
| base | 45s | 3m 00s | 4m 30s |
| small | 1m 15s | 8m 00s | 12m 00s |
| medium | 2m 30s | 18m 00s | 25m 00s |
| large | 4m 00s | 35m 00s | 50m 00s |

### 📈 Kalite vs Hız Önerisi

| Kullanım Durumu | Önerilen Model | Açıklama |
|----------------|----------------|----------|
| Hızlı önizleme | tiny | Test ve hızlı kontrol |
| Genel kullanım | base | İyi denge |
| Kaliteli altyazı | small/medium | Profesyonel kullanım |
| En yüksek kalite | large | Zor ses koşulları |

---

## 🔄 Güncellemeler ve Versiyon Geçmişi

### v2.1.0 (Güncel)
- ✅ Web arayüzü eklendi
- ✅ 7 yeni altyazı stili
- ✅ GPU hızlandırma desteği
- ✅ Gelişmiş hata yönetimi
- ✅ Toplu işlem optimizasyonu

### v2.0.0
- ✅ faster-whisper entegrasyonu
- ✅ ASS format desteği
- ✅ Ses iyileştirme filtreleri
- ✅ Çoklu platform desteği

### v1.0.0
- ✅ Temel Whisper entegrasyonu
- ✅ SRT/VTT çıktı
- ✅ Komut satırı arayüzü

---

## 🤝 Katkıda Bulunma

### 🔧 Geliştirme Ortamı Kurulumu

```bash
# Depoyu forklayın ve klonlayın
git clone https://github.com/yourusername/offline-subtitle-tool.git
cd offline-subtitle-tool

# Development branch'i oluşturun
git checkout -b feature/yeni-ozellik

# Geliştirme bağımlılıklarını yükleyin
pip install -r requirements-dev.txt

# Pre-commit hooks kurulumu
pre-commit install
```

### 📝 Katkı Türleri

- 🐛 **Bug Raporları**: Issues bölümünde detaylı açıklama ile
- 💡 **Özellik Önerileri**: Enhancement label'ı ile issue açın
- 📖 **Dokümantasyon**: README, docstring'ler, örnekler
- 🔧 **Kod Katkıları**: Pull request'ler memnuniyetle karşılanır
- 🌍 **Çeviri**: Çoklu dil desteği için

### ✅ Pull Request Süreci

1. Fork'u güncelleyin
2. Feature branch oluşturun
3. Değişiklikleri test edin
4. Commit mesajları anlamlı olsun
5. Pull Request açın
6. Code review bekleyin

### 📋 Kod Standartları

- **Python**: PEP 8 standardı
- **Dokümantasyon**: Google style docstrings
- **Test**: pytest ile unit testler
- **Commit**: Conventional Commits formatı

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

```
MIT License

Copyright (c) 2024 Offline Subtitle Tool Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Teşekkürler

Bu proje aşağıdaki açık kaynak projelerden faydalanmaktadır:

- **[OpenAI Whisper](https://github.com/openai/whisper)**: AI ses tanıma motoru
- **[faster-whisper](https://github.com/guillaumekln/faster-whisper)**: Optimized Whisper implementasyonu  
- **[FFmpeg](https://ffmpeg.org/)**: Ses/video işleme
- **[Flask](https://flask.palletsprojects.com/)**: Web framework
- **[PyTorch](https://pytorch.org/)**: Machine learning framework

---

## 📞 Destek ve İletişim

### 💬 Topluluk Desteği
- **GitHub Issues**: Bug raporları ve sorular için
- **Discussions**: Genel tartışmalar ve öneriler için

### 📧 İletişim
- **Geliştirici**: [GitHub Profile](https://github.com/ibrahimglmz)


### 🔗 Bağlantılar
- **Demo Video**: [YouTube Linki]
- **web sayfam**: [https://ibrahimglmz.github.io/portfolio/]
- **Docker Image**: [DockerHub]

---

<div align="center">

**🌟 Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**

**[⬆ Başa Dön](#-offline-professional-video-subtitle-generator)**

</div>