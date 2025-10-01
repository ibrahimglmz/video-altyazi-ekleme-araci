# 🎬 Profesyonel Video Altyazı Aracı (Çevrimdışı & AI Destekli)

<div align="center">

**AI destekli, tamamen çevrimdışı altyazı ve çok dilli TTS oluşturma aracı**

OpenAI Whisper kullanarak videolarınıza profesyonel altyazılar ekleyin, metinleri konuşmaya çevirin ve çok dilli videolar oluşturun - internet bağlantısı gerektirmez (TTS hariç)!

</div>

---

## 🚀 Hızlı Başlangıç

Bu proje, hem Komut Satırı Arayüzü (CLI) hem de kullanıcı dostu bir Web Arayüzü sunar.

### Web Arayüzü ile Başlatma

Web arayüzü ile hızlıca başlamak için aşağıdaki adımları takip edin:

1.  **Sanal ortamınızı etkinleştirin** (eğer etkin değilse):
    ```bash
    source .venv/bin/activate
    ```
2.  **Flask uygulamasını başlatın**:
    ```bash
    python web_app.py
    ```
3.  Tarayıcınızda `http://127.0.0.1:5001/` adresine gidin.

Artık web arayüzü üzerinden dosyalarınızı yükleyebilir ve altyazı/TTS işlemlerini gerçekleştirebilirsiniz!

---

## ✨ Özellikler

### Temel Altyazı Oluşturma (CLI & Web)

*   🤖 **AI Destekli Transkripsiyon**: OpenAI Whisper ve faster-whisper desteği ile yüksek doğrulukta ses/video transkripsiyonu.
*   🌐 **Tamamen Çevrimdışı**: Temel transkripsiyon ve altyazı gömme işlemleri için internet bağlantısı gerektirmez.
*   🎨 **7 Profesyonel Altyazı Stili**: Cinema, YouTube, Netflix ve daha fazlası gibi özelleştirilebilir stil önayarları.
*   📄 **Çoklu Çıktı Formatları**: SRT, VTT, ASS, TXT ve videoya gömülü altyazı çıktıları.
*   🎯 **Yüksek Doğruluk**: Gelişmiş ses işleme algoritmaları ve gürültü azaltma.
*   ⚡ **Hızlı İşlem**: GPU desteği (uygun donanım ile) ve optimize edilmiş performans.
*   📁 **Dizin İşleme**: Klasördeki tüm medya dosyalarını toplu olarak işleme yeteneği.

### Çok Dilli Metin-Konuşma (TTS) & Video Oluşturma (Web)

*   🎤 **Metin-Konuşma (TTS)**: Oluşturulan altyazıları 12 farklı dilde yüksek kaliteli sesli konuşmaya dönüştürün.
*   🌍 **Çok Dilli Video Çıktısı**: Orijinal videoyu, seçilen dillerdeki TTS ses parçalarıyla birleştirin.
*   🔊 **Orijinal Ses Karıştırma**: TTS sesiyle orijinal video sesini ayarlanabilir bir oranda karıştırın.
*   🎬 **Altyazıları Gömmek**: Oluşturulan altyazıları doğrudan çok dilli videolara gömün.
*   ⚙️ **Birden Çok TTS Motoru**: Google TTS (gTTS) ve Edge TTS desteği (Edge TTS daha doğal sesler sunar ve internet bağlantısı gerektirir).

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

## 🛠️ Kurulum

### Ön Gereksinimler

*   **Python 3.7 veya üzeri**: `python3 --version` komutu ile kontrol edebilirsiniz.
*   **FFmpeg**: Video ve ses işleme için gereklidir. Sisteminizin PATH ortam değişkeninde bulunmalıdır. [FFmpeg resmi sitesinden](https://ffmpeg.org/download.html) indirebilirsiniz.
*   **GPU desteği için CUDA (İsteğe Bağlı)**: Eğer NVIDIA GPU'nuz varsa ve daha hızlı işlem yapmak istiyorsanız [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) kurmanız önerilir.

### Adım Adım Kurulum

1.  **Projeyi klonlayın**:
    ```bash
    git clone [https://github.com/username/offline-subtitle-tool.git](https://github.com/username/offline-subtitle-tool.git)
    cd offline-subtitle-tool
    ```
    *(GitHub reposu placeholder. Kendi repo URL'inizle değiştirin.)*

2.  **Sanal ortam oluşturun**:
    ```bash
    python3 -m venv .venv
    ```

3.  **Sanal ortamı etkinleştirin**:
    *   **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows**:
        ```bash
        .venv\Scripts\activate
        ```

4.  **Gerekli paketleri yükleyin**:
    ```bash
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    ```

---

## 🖥️ Kullanım

Projenin iki ana kullanım şekli vardır: Web Arayüzü ve Komut Satırı Arayüzü (CLI).

### 🌐 Web Arayüzü Kullanımı

Kullanıcı dostu web arayüzü ile işlemleri kolayca yapabilirsiniz.

1.  **Uygulamayı başlatın**:
    ```bash
    python web_app.py
    ```
    Uygulama varsayılan olarak `http://127.0.0.1:5001/` adresinde çalışacaktır.
2.  **Dosya Yükleme ve Ayarlar**:
    *   Web arayüzünde "Video veya Ses Dosyası Seçin" alanından medya dosyanızı yükleyin.
    *   İstediğiniz çıktı formatlarını (`video`, `srt`, `vtt`, `ass`, `txt`), dili, altyazı stilini ve Whisper model boyutunu seçin.
    *   Gelişmiş seçenekleri (GPU hızlandırma, ses geliştirme) etkinleştirebilirsiniz.
3.  **Temel Altyazı Oluşturma**:
    *   "Temel Altyazılar" sekmesini kullanarak tek dilde altyazı oluşturun ve videoya gömün.
    *   "Altyazıları Oluştur" düğmesine tıklayın. İşlem tamamlandığında, oluşturulan dosyaları web arayüzünde görüntüleyebilir veya indirebilirsiniz.
4.  **Çok Dilli TTS Video Oluşturma**:
    *   "Çok Dilli TTS" sekmesini kullanarak birden çok dilde TTS ses parçalarıyla videolar oluşturun.
    *   Hedef dilleri, TTS motorunu (Edge TTS veya Google TTS) ve orijinal ses karıştırma oranını seçin.
    *   "Çok Dilli Videolar Oluştur" düğmesine tıklayın.

### 命令行工具 (CLI) Kullanımı

Daha gelişmiş kullanım senaryoları ve betikleme için CLI'yi tercih edebilirsiniz. Ana CLI aracı `server.py` dosyasıdır.

```bash
python server.py -i <girdi_dosyasi_veya_klasoru> -o <cikti_klasoru> [SEÇENEKLER]
```

**Temel Parametreler:**

*   `-i`, `--input` (Zorunlu): İşlenecek video/ses dosyası yolu veya medya dosyalarını içeren klasör yolu.
*   `-o`, `--output` (Varsayılan: `output`): Çıktı dosyalarının kaydedileceği dizin.
*   `--formats` (Varsayılan: `srt,video`): Virgülle ayrılmış çıktı formatları (`video`, `srt`, `vtt`, `ass`, `txt`).
*   `--style` (Varsayılan: `default`): Altyazı stil önayarı (`default`, `bold`, `elegant`, `cinema`, `modern`, `minimal`, `terminal`).
*   `--language` (Varsayılan: `auto`): Transkripsiyon dili kodu (`auto`, `en`, `tr`, `es`, vb.) veya otomatik algılama için "auto".
*   `--model` (Varsayılan: `base`): Whisper model boyutu (`tiny`, `base`, `small`, `medium`, `large`).
*   `--gpu`: Varsa GPU hızlandırmasını etkinleştirir.
*   `--no-audio-enhance`: Ses geliştirme filtrelerini devre dışı bırakır.
*   `--batch`: Giriş klasöründeki tüm medya dosyalarını işler.
*   `--overwrite`: Mevcut çıktı dosyalarının üzerine yazar.
*   `--verbose`: Ayrıntılı çıktıyı etkinleştirir.

**Çok Dilli TTS Parametreleri (sadece `server.py`'de desteklenir, web arayüzünde ayrı bir sekmede bulunur):**

*   `--tts-languages`: Virgülle ayrılmış, konuşma sentezi (TTS) için hedef dil kodları (örn: `tr,en,fr`).
*   `--tts-engine` (Varsayılan: `edge_tts`): Kullanılacak TTS motoru (`gtts` veya `edge_tts`).
*   `--no-embed-subtitles`: Son videolara altyazıları gömmez.
*   `--original-audio-mix` (Varsayılan: `0.3`): TTS ile karıştırırken orijinal sesin ses oranı (0.0-1.0).

**Örnek CLI Kullanımı:**

1.  **Tek bir video dosyası için Türkçe altyazı ve videoya gömülü çıktı oluşturma**:
    ```bash
    python server.py -i video.mp4 -o output_folder --formats srt,video --style cinema --language tr --model large --gpu
    ```

2.  **Bir klasördeki tüm ses dosyaları için SRT ve TXT altyazıları oluşturma (toplu işlem)**:
    ```bash
    python server.py -i audio_files_folder -o output_transcriptions --formats srt,txt --language en --batch
    ```

3.  **Çok dilli TTS ile video oluşturma (Türkçe ve İngilizce ses parçaları)**:
    ```bash
    python server.py -i my_video.mp4 -o multilingual_output --tts-languages tr,en --tts-engine edge_tts --original-audio-mix 0.4 --formats video,srt
    ```
    *(Not: Bu örnek CLI komutu, `server.py`'nin `process_with_multilingual_tts` metodunu çağırır. Web arayüzünde bu, ayrı bir sekmeden kontrol edilir.)*

---

## 💡 Performans İpuçları

*   **Model Boyutu**: `tiny` veya `base` modelleri daha hızlıdır ancak daha düşük doğruluk sunar. `large` modeller en yüksek doğruluk için daha yavaş çalışır ve daha fazla kaynak tüketir.
*   **GPU Hızlandırma**: Uyumlu bir NVIDIA GPU'nuz varsa `--gpu` bayrağını kullanmak işlem süresini önemli ölçüde hızlandırır.
*   **Ses Geliştirme**: `--no-audio-enhance` bayrağını kullanarak ses geliştirme filtrelerini kapatmak, bazen çok düşük kaliteli seslerde veya çok uzun videolarda performansı artırabilir. Ancak genellikle açık bırakılması önerilir.
*   **TTS Motoru**: `edge_tts`, `gtts`'ye göre daha doğal ve yüksek kaliteli sesler sunar, ancak genellikle biraz daha yavaş olabilir ve internet bağlantısı gerektirir.

---

## 🤝 Katkıda Bulunma

Projenin geliştirilmesine katkıda bulunmak isterseniz, lütfen bir "pull request" (çekme isteği) gönderin veya bir "issue" (sorun) açın. Her türlü katkı memnuniyetle karşılanır!

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
