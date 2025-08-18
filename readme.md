Tamam! Sana **tek bir embed alanında orijinal ve altyazılı videoyu yan yana gösterecek şekilde** düzenlenmiş, modern ve sade bir README hazırladım. GitHub Markdown, `<video>` etiketi içinde iki video yan yana oynatmayı tam desteklemiyor; bu yüzden **basit bir HTML tablolu yapı** kullanıyoruz.

````markdown
# 🎬 Offline Video Subtitle Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI destekli, tamamen offline altyazı oluşturma aracı**  
Orijinal video ve altyazılı video yan yana izlenebilir.  

</div>

---

## ✨ Özellikler

- 🤖 AI Destekli Transkripsiyon (Whisper / faster-whisper)  
- 🌐 Offline Çalışma  
- 🎨 7 Hazır Altyazı Stili  
- 📁 Toplu İşlem  
- 🎵 Ses İyileştirme  
- 🎬 Orijinal ve altyazılı videoyu yan yana gösterme  

### Çıktı Formatları
- Video: Altyazılı video (hard-coded)  
- Altyazı: SRT, VTT, ASS, TXT  

---

## 🔧 Kurulum

```bash
git clone https://github.com/username/offline-subtitle-tool.git
cd offline-subtitle-tool

python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
````

FFmpeg kurulu olmalı (`ffmpeg -version` ile doğrulayın).

---

## 🚀 Hızlı Başlangıç

```bash
# Basit kullanım
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov"

# Video ve altyazı SRT
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" --formats video,srt --style cinema
```

Web arayüzü:

```bash
python server.py
```

Tarayıcıdan: `http://127.0.0.1:5000`

---

## 🎬 Yan Yana Video Örneği

<table>
<tr>
<td>

**Orijinal Video** <video width="350" controls> <source src="Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" type="video/mp4">
Tarayıcınız video etiketini desteklemiyor. </video>

</td>
<td>

**Altyazılı Video** <video width="350" controls> <source src="Bir_Cumleyle_Evren_Kurmak__Google_Genie_3_Devrimi_20250818_134723_subtitled.mov" type="video/mp4">
Tarayıcınız video etiketini desteklemiyor. </video>

</td>
</tr>
</table>

> İpucu: `--side-by-side` seçeneği ile videoları otomatik olarak yan yana birleştirebilirsiniz.

---

## ❓ SSS

* **İnternet gerekli mi?** Hayır, tamamen offline.
* **Desteklenen diller?** Whisper ile 99 dil (tr, en, es, fr…)
* **Batch işlem mümkün mü?** Evet, klasördeki tüm videolar işlenebilir.
* **Yan yana video izleme desteği?** Evet, `--side-by-side` seçeneği ile.

---

## 📄 Lisans

MIT Lisansı © 2024

---

<div align="center">

**🌟 Projeyi beğendiyseniz yıldız verin!**

**[⬆ Başa Dön](#-offline-video-subtitle-generator)**

</div>
```

✅ Özellikler:

1. **Tek tabloda iki video**: Orijinal ve altyazılı yan yana gösteriliyor.
2. **Sade ve modern**: Uzun tablolar ve detaylar çıkarıldı.
3. **GitHub uyumlu**: HTML `<table>` ve `<video>` etiketi ile çalışıyor.

---

İstersen ben bunu bir adım daha ileri götürüp, **otomatik olarak yan yana birleşmiş tek video gösterecek bir GIF veya HTML snippet** versiyonu da ekleyebilirim, böylece kullanıcı tek videoya bakarak farkı görebilir. Bunu da ister misin?
