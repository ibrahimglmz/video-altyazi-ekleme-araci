Harika! O zaman README’yi **tamamen sadeleştirip, tek videoda orijinal ve altyazılı videoyu yan yana gösterecek bir embed örneği** ile yeniden hazırladım. Ayrıca temel kullanım bilgilerini de içeriyor, GitHub’da direkt kullanabilirsin.

---

````markdown
# 🎬 Offline Video Subtitle Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI destekli, tamamen offline çalışan video altyazı oluşturma aracı**  

</div>

---

## ✨ Özellikler

- 🤖 AI Destekli Transkripsiyon (Whisper / faster-whisper)  
- 🌐 Tamamen offline çalışma  
- 🎨 7 profesyonel altyazı stili  
- 📁 Toplu işlem desteği  
- 🎵 Otomatik ses iyileştirme  
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

FFmpeg kurulu olmalı:

```bash
ffmpeg -version
```

---

## 🚀 Hızlı Başlangıç

```bash
# Basit kullanım
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov"

# Video ve SRT altyazı
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" --formats video,srt --style cinema
```

Web arayüzü:

```bash
python server.py
```

Tarayıcıdan: `http://127.0.0.1:5000`

---

## 🎬 Yan Yana Video Örneği

**Not:** Videoları tek bir yan yana video hâline getirip göstermek için FFmpeg ile birleştirebilirsiniz:

```bash
ffmpeg -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" \
       -i "Bir_Cumleyle_Evren_Kurmak__Google_Genie_3_Devrimi_20250818_134723_subtitled.mov" \
       -filter_complex "[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[out]" \
       -map "[out]" side_by_side.mp4
```

Sonrasında GitHub README veya HTML sayfasında embed etmek için:

```html
<video width="700" controls>
  <source src="side_by_side.mp4" type="video/mp4">
  Tarayıcınız video etiketini desteklemiyor.
</video>
```

---

## ❓ Sık Sorulan Sorular

* **İnternet gerekli mi?** Hayır, tamamen offline.
* **Desteklenen diller?** Whisper ile 99 dil: tr, en, es, fr, de…
* **Batch işlem mümkün mü?** Evet, klasördeki tüm videolar işlenebilir.
* **Yan yana video izleme desteği?** Evet, FFmpeg ile birleştirilmiş video kullanabilirsiniz.

---

## 📄 Lisans

MIT Lisansı © 2024

---

<div align="center">

**🌟 Projeyi beğendiyseniz yıldız verin!**

**[⬆ Başa Dön](#-offline-video-subtitle-generator)**

</div>
```

---

✅ **Özellikler:**

1. Orijinal ve altyazılı videoyu **tek bir yan yana video** olarak gösterme.
2. Sade ve modern README, gereksiz tablolar kaldırıldı.
3. Kullanıcıya **komut satırı ve web arayüzü** kullanım örnekleri verildi.
4. **FFmpeg ile birleşik video** komutu eklendi, böylece tek embed gösterim mümkün.

---

İstersen ben bunu GitHub’da doğrudan çalışacak şekilde **yan yana videonun otomatik oynatıldığı bir HTML snippet** de hazırlayabilirim, böylece kullanıcı tek tıkla izleyebilir. Bunu da yapayım mı?
