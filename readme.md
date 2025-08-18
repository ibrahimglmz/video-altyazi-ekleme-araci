# 🎬 Offline Video Subtitle Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI destekli, tamamen offline altyazı oluşturma aracı**

OpenAI Whisper kullanarak videolarınıza profesyonel altyazılar ekleyin - internet bağlantısı gerektirmez!

</div>

---

## 🎬 Orijinal ve Altyazılı Video Karşılaştırması

<table>
<tr>
<td align="center">
<strong>Orijinal Video</strong><br/>
<video width="350" controls>
<source src="Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" type="video/mp4">
Tarayıcınız video etiketini desteklemiyor.
</video>
</td>
<td align="center">
<strong>Altyazılı Video</strong><br/>
<video width="350" controls>
<source src="Bir_Cumleyle_Evren_Kurmak__Google_Genie_3_Devrimi_20250818_134723_subtitled.mov" type="video/mp4">
Tarayıcınız video etiketini desteklemiyor.
</video>
</td>
</tr>
</table>

---

## ✨ Özellikler

- 🤖 **AI Destekli Transkripsiyon**: OpenAI Whisper ve faster-whisper desteği
- 🌐 **Tamamen Offline**: İnternet bağlantısı gerektirmez
- 🎨 **7 Profesyonel Altyazı Stili**: Cinema, YouTube, Netflix ve daha fazlası
- 🎬 **Video Karşılaştırma**: Orijinal ve altyazılı videoları yan yana görüntüleme
- 📱 **Web Arayüzü**: Flask tabanlı kullanıcı dostu arayüz
- 📄 **Çoklu Format**: SRT, VTT ve video çıktı formatları
- 🎯 **Yüksek Doğruluk**: Gelişmiş ses işleme algoritmaları
- ⚡ **Hızlı İşlem**: GPU desteği ile optimize edilmiş performans

---

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
python -m venv venv

# Sanal ortamı aktifleştirin
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### FFmpeg Kurulumu

**Windows:**
```bash
# Chocolatey ile
choco install ffmpeg

# Veya manuel olarak https://ffmpeg.org/download.html adresinden indirin
```

**macOS:**
```bash
# Homebrew ile
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 🎯 Kullanım

### Komut Satırı Kullanımı

```bash
# Basit kullanım - sadece altyazılı video
python app.py -i "video.mp4"

# Belirli çıktı formatları ile
python app.py -i "video.mp4" --formats video,srt,vtt

# Özel altyazı stili ile
python app.py -i "video.mp4" --style cinema

# Çıktı dizini belirtme
python app.py -i "video.mp4" -o "output_folder"

# Gelişmiş ayarlar
python app.py -i "video.mp4" --model medium --device cuda --style netflix
```

### Web Arayüzü

```bash
# Web arayüzünü başlatın
python web_app.py

# Tarayıcınızda açın: http://localhost:5000
```

### Parametreler

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `-i, --input` | Giriş video dosyası | Gerekli |
| `-o, --output` | Çıktı dizini | `./output` |
| `--formats` | Çıktı formatları (video,srt,vtt) | `video` |
| `--style` | Altyazı stili | `default` |
| `--model` | Whisper model (tiny,base,small,medium,large) | `base` |
| `--device` | İşlem birimi (cpu,cuda) | `cpu` |
| `--language` | Dil kodu (tr,en,auto) | `auto` |

---

## 🎨 Altyazı Stilleri

| Stil | Açıklama | Görünüm |
|------|----------|---------|
| `default` | Standart beyaz altyazı | Klasik stil |
| `cinema` | Sinema tarzı sarı altyazı | Profesyonel |
| `youtube` | YouTube tarzı siyah kenarlı | Modern |
| `netflix` | Netflix tarzı kalın altyazı | Premium |
| `subtitle` | Minimalist tasarım | Temiz |
| `outlined` | Kalın kenarlı altyazı | Belirgin |
| `shadow` | Gölgeli altyazı | Estetik |

---

## 📂 Proje Yapısı

```
offline-subtitle-tool/
├── app.py                 # Ana uygulama
├── web_app.py            # Flask web arayüzü
├── subtitle_processor.py # Altyazı işleme modülü
├── video_processor.py    # Video işleme modülü
├── styles/
│   ├── cinema.ass        # Sinema stili
│   ├── youtube.ass       # YouTube stili
│   └── netflix.ass       # Netflix stili
├── templates/
│   ├── index.html        # Ana sayfa
│   └── result.html       # Sonuç sayfası
├── static/
│   ├── css/
│   └── js/
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

---

## 🛠️ Geliştirme

### Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Test Etme

```bash
# Testleri çalıştırın
python -m pytest tests/

# Test kapsamını kontrol edin
python -m pytest --cov=subtitle_processor tests/
```

---

## 🔧 Sorun Giderme

### Yaygın Sorunlar

**FFmpeg bulunamadı:**
```bash
# PATH kontrolü
ffmpeg -version

# Yeniden kurulum gerekiyorsa yukarıdaki FFmpeg kurulum adımlarını takip edin
```

**CUDA hatası:**
```bash
# CPU kullanımına geçiş
python app.py -i "video.mp4" --device cpu
```

**Bellek hatası:**
```bash
# Daha küçük model kullanın
python app.py -i "video.mp4" --model tiny
```

### Log Dosyaları

Uygulama logları `logs/` dizininde saklanır:
- `app.log` - Genel uygulama logları
- `whisper.log` - Whisper transkripsiyon logları
- `ffmpeg.log` - Video işleme logları

---

## 📊 Performans

### Model Karşılaştırması

| Model | Boyut | Hız | Doğruluk | VRAM |
|-------|-------|-----|----------|------|
| tiny | 39 MB | Çok hızlı | Düşük | ~1GB |
| base | 74 MB | Hızlı | İyi | ~1GB |
| small | 244 MB | Orta | İyi | ~2GB |
| medium | 769 MB | Yavaş | Yüksek | ~5GB |
| large | 1550 MB | Çok yavaş | Çok yüksek | ~10GB |

### Desteklenen Formatlar

**Giriş:** MP4, AVI, MOV, MKV, WMV, FLV, WEBM
**Çıktı:** MP4 (H.264), SRT, VTT

---

## 🌍 Dil Desteği

Whisper 99+ dili destekler. Popüler diller:

- 🇹🇷 Türkçe
- 🇺🇸 İngilizce  
- 🇩🇪 Almanca
- 🇫🇷 Fransızca
- 🇪🇸 İspanyolca
- 🇯🇵 Japonca
- 🇰🇷 Korece
- 🇨🇳 Çince

```bash
# Belirli dil için
python app.py -i "video.mp4" --language tr
```

---

## 🔄 Güncelleme

```bash
# En son sürümü alın
git pull origin main

# Bağımlılıkları güncelleyin
pip install -r requirements.txt --upgrade
```

---

## 📞 Destek

- 🐛 **Bug Report**: [Issues](https://github.com/username/offline-subtitle-tool/issues)
- 💡 **Feature Request**: [Discussions](https://github.com/username/offline-subtitle-tool/discussions)
- 📧 **İletişim**: [email@example.com](mailto:email@example.com)

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [OpenAI Whisper](https://github.com/openai/whisper) - Mükemmel ASR modeli
- [FFmpeg](https://ffmpeg.org/) - Video işleme altyapısı
- [Flask](https://flask.palletsprojects.com/) - Web framework
- Tüm katkıda bulunanlara teşekkürler!

---

<div align="center">

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**

</div>