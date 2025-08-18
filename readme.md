# 🎬 Offline Video Subtitle Generator

<div align="center">

**AI destekli, tamamen offline altyazı oluşturma aracı**

OpenAI Whisper kullanarak videolarınıza profesyonel altyazılar ekleyin - internet bağlantısı gerektirmez!

</div>

---

## 🎬 Orijinal ve Altyazılı Görüntü Karşılaştırması

<div align="center">

Bu iki görsel, **altyazı ekleme öncesi ve sonrası** videonun nasıl göründüğünü net bir şekilde gösteriyor.

<br>

| Orijinal Görüntü | Altyazılı Görüntü |
| :---: | :---: |
| ![Orijinal Görüntü](assets/Screenshot%202025-08-18%20at%2015.02.24.png) | ![Altyazılı Görüntü](assets/Screenshot%202025-08-18%20at%2015.02.51.png) |

</div>

---

## ✨ Özellikler

- 🤖 **AI Destekli Transkripsiyon**: OpenAI Whisper ve faster-whisper desteği
- 🌐 **Tamamen Offline**: İnternet bağlantısı gerektirmez
- 🎨 **7 Profesyonel Altyazı Stili**: Cinema, YouTube, Netflix ve daha fazlası
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
git clone [https://github.com/username/offline-subtitle-tool.git](https://github.com/username/offline-subtitle-tool.git)
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
