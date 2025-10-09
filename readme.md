# 🎬 Altyazı Oluşturucu - Grunge Fırça Darbesi Stili

<div align="center">

**AI destekli, tamamen çevrimişdışı altyazı oluşturma aracı**

Grunge fırça darbesi tarzında dinamik arka planlarla videolarınıza artistik altyazılar ekleyin!

![GitHub](https://img.shields.io/badge/GitHub-Açık_Kaynak-green)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange)
![Offline](https://img.shields.io/badge/100%25-Çevrimdışı-red)

</div>

---

## ✨ Özellikler

### 🎨 **Grunge Fırça Darbesi Stili**
- **El ile boyanmış görünüm** - Akrilik fırça darbesi efekti
- **Dinamik boyutlandırma** - Metin uzunluğuna göre esneyen arka plan
- **Yuvarlak sans-serif font** - Okunaklı ve estetik
- **Düzensiz kenarlar** - Grunge doku ile organik görünüm
- **Kırmızı grunge doku** - Transparanlık ile profesyonel görsel

### 🚀 **Güçlü AI İşleme**
- **OpenAI Whisper** entegrasyonu
- **5 farklı model boyutu** (tiny → large)
- **GPU hızlandırma** desteği
- **Çok dilli transkripsiyon** (12+ dil)

### 📄 **Çoklu Format Desteği**
- **Video Girdi**: MP4, AVI, MOV, MKV, WebM, FLV
- **Ses Girdi**: MP3, WAV, FLAC, AAC, OGG, M4A
- **Çıktı Formatları**: SRT, VTT, ASS, TXT, Gömülü Video

---

## 🚀 Hızlı Başlangıç

### 1️⃣ Sanal Ortamı Etkinleştirin
```bash
source .venv/bin/activate
```

### 2️⃣ Web Uygulamasını Başlatın
```bash
python web_app.py
```

### 3️⃣ Tarayıcıda Açın
**Yerel erişim**: http://127.0.0.1:5214/

---

## 🖥️ Kullanım Seçenekleri

### 🌐 Web Arayüzü (Önerilen)
1. **Dosya Yükle**: Video/ses dosyanızı sürükle-bırak ile yükleyin
2. **Ayarları Seç**: Çıktı formatları, dil, model boyutu
3. **İşlet**: "Altyazıları Oluştur" butonuna tıklayın
4. **İndir**: Oluşturulan dosyaları indirin

### 💻 Komut Satırı (CLI)
```bash
# Temel kullanım
python app.py -i video.mp4 -o output_folder

# Gelişmiş seçenekler
python app.py -i video.mp4 -o output --formats srt,video --model large --gpu

# Toplu işleme
python app.py -i video_folder --batch --formats srt,vtt,ass
```

---

## ⚙️ Kurulum Gereksinimleri

### ✅ Ön Gereksinimler
- **Python 3.7+**
- **FFmpeg** (PATH'te yüklü)
- **4GB+ RAM** (8GB önerilir)
- **GPU**: NVIDIA CUDA (isteğe bağlı)

### 📦 Python Paketleri
Tüm gerekli paketler `.venv/` klasöründe yüklü:
- OpenAI Whisper
- faster-whisper
- PyTorch & torchaudio
- Flask (web arayüzü)
- FFmpeg-python
- NumPy, tqdm

---

## 🎨 Grunge Altyazı Stilini Önizleme

```
    ░░▒▒▓▓███████████████▓▓▒▒░░
  ░▒▓██                          ██▓▒░
 ▒▓█      valizler alınmayacak!       █▓▒
░▓█        Grunge fırça darbesi        █▓░
 ▒▓█                                █▓▒
  ░▒▓██                          ██▓▒░
    ░░▒▒▓▓███████████████▓▓▒▒░░
```

**Grunge Stil Özellikleri:**
- **Dokulu Arka Plan**: Kırmızı grunge doku ile el ile boyanmış efekt
- **Font**: Yuvarlak sans-serif (Avenir/Arial Rounded), 32px, beyaz renk
- **Dünamic Boyutlandırma**: Metin uzunluğuna göre otomatik genişleme
- **Düzensiz Kenarlar**: Dalgalı, organik fırça darbesi kenarları
- **Transparanlık**: Sadece fırça darbesi alanı görünür

---

## 📋 CLI Parametreleri

```bash
python app.py [SEÇENEKLER]

Zorunlu:
  -i, --input          Girdi dosya/klasör yolu

İsteğe Bağlı:
  -o, --output         Çıktı dizini (varsayılan: output)
  --formats           Çıktı formatları (varsayılan: srt,video)
  --language          Dil kodu (varsayılan: auto)
  --model             Whisper model (varsayılan: base)
  --gpu               GPU hızlandırmayı etkinleştir
  --batch             Klasördeki tüm dosyaları işle
  --no-audio-enhance  Ses geliştirmeyi devre dışı bırak
  --include-timestamps TXT'ye zaman damgası ekle
```

---

## 🔧 Performans İpuçları

| Model | Hız | Doğruluk | Kullanım |
|-------|-----|----------|----------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | Hızlı test |
| `base` | ⚡⚡ | ⭐⭐⭐ | **Önerilen** |
| `small` | ⚡ | ⭐⭐⭐⭐ | İyi kalite |
| `medium` | 🐌 | ⭐⭐⭐⭐ | Yüksek kalite |
| `large` | 🐌🐌 | ⭐⭐⭐⭐⭐ | En iyi kalite |

### 💡 Optimizasyon Tavsiyeleri
- **GPU**: Büyük dosyalarda 5-10x hız artışı
- **Ses Geliştirme**: Kaliteyi artırır ama işlem süresini uzatır
- **Format Seçimi**: Sadece ihtiyacınız olan formatları seçin
- **Model Boyutu**: İlk test için `base`, final için `large`

---

## 🗂️ Proje Yapısı

```
video-altyazi-ekleme-araci/
├── app.py                 # CLI uygulaması
├── web_app.py            # Flask web arayüzü
├── templates/
│   └── index.html        # Web arayüzü şablonu
├── static/
│   ├── css/style.css     # Stiller
│   └── js/app.js         # JavaScript
├── uploads/              # Yüklenen dosyalar
├── output/               # Oluşturulan çıktılar
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

---

## 🐛 Sorun Giderme

### Web Uygulaması Başlamazsa
```bash
# Virtual environment kontrol
source .venv/bin/activate
python -c "import flask; print('Flask OK')"

# Port kontrol (5214 kullanılıyor)
lsof -i :5214
```

### FFmpeg Bulunamazsa
```bash
# macOS için
brew install ffmpeg

# Kontrol
ffmpeg -version
ffprobe -version
```

### Düşük Performans
1. **GPU'yu etkinleştirin** (`--gpu` veya web arayüzünde checkbox)
2. **Küçük model** deneyin (`tiny` veya `base`)
3. **Ses geliştirmeyi kapatın** (`--no-audio-enhance`)
4. **Gereksiz formatları** seçmeyin

---

## 🔐 Gizlilik ve Güvenlik

✅ **%100 Çevrimdışı** - İnternet bağlantısı gerektirmez
✅ **Yerel İşleme** - Dosyalarınız cihazınızda kalır
✅ **API Yok** - Üçüncü taraf servislere bağımlı değil
✅ **Açık Kaynak** - Kodlar tamamen şeffaf

---

## 📞 Destek

Herhangi bir sorunla karşılaştığınızda:

1. **Virtual environment** etkin mi kontrol edin
2. **FFmpeg** kurulu mu doğrulayın  
3. **Dosya formatı** destekleniyor mu kontrol edin
4. **Konsol logları** hata mesajları için inceleyin

---

## 🎉 Başarıyla Basitleştirildi!

Bu versiyon **sadece altyazı ekleme** odaklıdır:

- ❌ **Kaldırılan**: TTS, ses kaydı, çoklu dil, karmaşık özellikler
- ✅ **Korunan**: Temel altyazı oluşturma, kırmızı stil, web arayüzü
- 🎯 **Odak**: Hızlı, güvenilir ve kolay kullanım

**Artık sadece altyazı oluşturma aracınız hazır!** 🎬