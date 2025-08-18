Anladım! Senin istediğin, **README içinde doğrudan orijinal video ile altyazılı videoyu yan yana karşılaştırma**. GitHub Markdown sınırlamaları nedeniyle `<video>` etiketi kullanacağız ve iki videoyu **HTML tabloda yan yana** yerleştireceğiz. Böylece kullanıcı GitHub sayfasında videoları karşılaştırabilir.

Aşağıda bunu yapacak örnek **README kodu**:

````markdown
# 🎬 Offline Video Subtitle Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Interface-red.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI destekli, tamamen offline altyazı oluşturma aracı**  

</div>

---

## 🎬 Orijinal ve Altyazılı Videoyu Yan Yana Karşılaştırma

<table>
<tr>
<td>

**Orijinal Video**  
<video width="350" controls>
  <source src="Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" type="video/mp4">
  Tarayıcınız video etiketini desteklemiyor.
</video>

</td>
<td>

**Altyazılı Video**  
<video width="350" controls>
  <source src="Bir_Cumleyle_Evren_Kurmak__Google_Genie_3_Devrimi_20250818_134723_subtitled.mov" type="video/mp4">
  Tarayıcınız video etiketini desteklemiyor.
</video>

</td>
</tr>
</table>

---

## ✨ Özellikler

- 🤖 AI destekli transkripsiyon (Whisper / faster-whisper)  
- 🌐 Offline çalışma  
- 🎨 7 profesyonel altyazı stili  
- 🎬 Orijinal ve altyazılı videoyu karşılaştırma  

---

## 🔧 Kurulum ve Kullanım

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

```bash
# Basit kullanım
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov"

# Video ve SRT altyazı
python app.py -i "Bir Cümleyle Evren Kurmak_ Google Genie 3 Devrimi.mov" --formats video,srt --style cinema
```

---

## 📄 Lisans

MIT Lisansı © 2024

```

✅ Açıklamalar:  
1. `<table>` ile iki video yan yana yerleştirildi.  
2. GitHub, `<video>` etiketi destekliyor, böylece kullanıcı doğrudan sayfada oynatabilir.  
3. Videoların **doğru yol ve isimleri** değiştirilirse aynı şekilde çalışır.  

---

İstersen ben bunu bir adım daha ileri götürüp, **tek video içinde orijinal ve altyazılı videoyu yan yana birleştiren otomatik FFmpeg komutu** da ekleyip, README’de hem tabloyu hem de birleşik videoyu gösterecek şekilde hazırlayabilirim. Bunu yapayım mı?
```
