# 📸 Fotoğrafçılar İçin Polaroid Oluşturucu

**Python dili ile geliştirilmiş, fotoğraf stüdyoları ve fotoğrafçılar için tasarlanmış, seçilen fotoğrafları polaroid şablonlarda birleştiren masaüstü uygulamasıdır.**

Bu araç sayesinde, 6x8 cm boyutunda ve 300 px/cm çözünürlükte olan fotoğraflarınızı yatay veya dikey olarak seçerek 10x15 cm olarak 2’li polaroid fotoğraflar haline getirebilirsiniz.

---

## 📂 Yazılımın Çalıştırılması

- Yazılımı .zip olarak indirin.
- dist klasörü içinde bulunan 'PolaroidOlusturucu.exe' dosyasını çalıştırın.

---

## 🚀 Özellikler

- 🖼️ 2 fotoğrafı tek bir 10x15 cm polaroid şablonda birleştirir  
- 🔄 Dikey veya yatay yön seçimi yapılabilir  
- 🧠 Fotoğraf boyutları otomatik kontrol edilir (6x8 cm ve 300 px/cm)  
- 📂 İstenilen fotoğraflar tek tek seçilir  
- 📁 İşlem sonrası çıktılar klasörde otomatik olarak açılır  
- 🖥️ Sade ve anlaşılır grafik arayüz  
- 💾 Kurulumsuz `.exe` desteği (taşınabilir)

---

## 🧰 Kullanılan Teknolojiler

- Python 3
- Tkinter (arayüz)
- Pillow (görsel işleme)
- PyInstaller (exe oluşturmak için)

---

## 🔧 Gerekli Kurulumlar (Geliştirici Modu için)

- pip install pillow
- pip install pyinstaller

---

## 🔧 Exe Oluşturmak için (Aşağıdaki Komutu Terminalde Çalıştırın)

```plaintext
pyinstaller --onefile --noconsole --add-data "logo.png;." --add-data "arka_plan_dikey.png;." --add-data "arka_plan_yatay.png;." --add-data "dikey_bos.png;." --add-data "yatay_bos.png;." polaroidFotoEylul.py
```

---

## 📁 Dosya Yapısı

```plaintext
📂 PolaroidOlusturucu
├── PolaroidOlusturucu.py
├── logo.png
├── arka_plan_dikey.png
├── arka_plan_yatay.png
├── dikey_bos.png
├── yatay_bos.png
└── 📂 dist/
    └── PolaroidOlusturucu.exe
```


---

## 🤝 **Yazılım Geliştirici**

[Hakan Akınsu - Computer Engineer](https://github.com/hakanakinsu0)

