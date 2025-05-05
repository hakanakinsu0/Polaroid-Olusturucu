import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
from PIL import ImageTk

# Mevcut çalıştırma klasörünü belirle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Fotoğrafın 6x8 cm boyutunda ve 300 DPI olup olmadığını kontrol eder
def check_photo_dimensions(photo_path):
    with Image.open(photo_path) as img:
        width, height = img.size
        cm_width, cm_height = width / 300, height / 300
        return ((round(cm_width, 1) == 6 and round(cm_height, 1) == 8) or
                (round(cm_width, 1) == 8 and round(cm_height, 1) == 6))

# Fotoğrafların işlendiği çıktı klasörünü otomatik olarak açar
def open_output_folder(path):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif sys.platform == 'darwin':  # macOS
            subprocess.call(['open', path])
        else:  # Linux ve diğerleri
            subprocess.call(['xdg-open', path])
    except Exception as e:
        messagebox.showwarning("Klasör Açılamadı", f"Çıktı klasörü açılamadı: {e}")

# Kullanıcıya "Dikey" veya "Yatay" yön seçimi yaptırır ve ekranın ortasında dialog gösterir
def choose_orientation():
    dialog = tk.Toplevel(root)
    dialog.title("Polaroid Yön Seçimi")
    dialog.resizable(False, False)
    result = {'orientation': None}
    tk.Label(dialog, text="Lütfen palorid fotoğrafların yönünü seçiniz", font=("Arial", 10)).pack(padx=10, pady=10)
    frame = tk.Frame(dialog)
    frame.pack(pady=5)
    def select(o):
        result['orientation'] = o
        dialog.destroy()
    tk.Button(frame, text="Dikey", width=10, command=lambda: select('Dikey')).pack(side='left', padx=10)
    tk.Button(frame, text="Yatay", width=10, command=lambda: select('Yatay')).pack(side='right', padx=10)

    # Dialog'u ana pencerenin ortasında konumlandır
    dialog.update_idletasks()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_w = root.winfo_width()
    root_h = root.winfo_height()
    dlg_w = dialog.winfo_width()
    dlg_h = dialog.winfo_height()
    pos_x = root_x + (root_w - dlg_w) // 2
    pos_y = root_y + (root_h - dlg_h) // 2
    dialog.geometry(f"{dlg_w}x{dlg_h}+{pos_x}+{pos_y}")
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    return result['orientation']

# Seçilen fotoğrafları ikili ikili işleyip polaroid formatında birleştirir
def process_photos(input_folder, orientation, selected_files):
    output_folder = os.path.join(input_folder, f"Foto Eylül - {os.path.basename(input_folder)}")
    os.makedirs(output_folder, exist_ok=True)

    # Yön bilgisine göre kullanılacak arka plan ve boş resim dosyalarını belirle
    if orientation == "Dikey":
        background_path = os.path.join(BASE_DIR, "arka_plan_dikey.png")
        empty_path = os.path.join(BASE_DIR, "dikey_bos.png")
    else:
        background_path = os.path.join(BASE_DIR, "arka_plan_yatay.png")
        empty_path = os.path.join(BASE_DIR, "yatay_bos.png")

    if not os.path.exists(background_path) or not os.path.exists(empty_path):
        messagebox.showerror("Hata", "Arka plan veya boş resim dosyası bulunamıyor! Lütfen kontrol edin.")
        return

    background = Image.open(background_path)
    empty_image = Image.open(empty_path)

    processed_count = 0
    invalid_count = 0

    # Her 2 fotoğrafı birleştirerek tek polaroid oluşturur
    for i in range(0, len(selected_files), 2):
        output_image = background.copy()
        draw = ImageDraw.Draw(output_image)

        for j in range(2):
            if i + j >= len(selected_files):
                photo = empty_image.copy()
            else:
                photo_path = selected_files[i + j]
                if not check_photo_dimensions(photo_path):
                    invalid_count += 1
                    messagebox.showwarning(
                        "Hatalı Fotoğraf",
                        f"{os.path.basename(photo_path)} fotoğrafının boyutları uygun değil (6x8 cm). Atlanıyor."
                    )
                    continue
                photo = Image.open(photo_path).convert("RGBA")

            # Fotoğrafı doğru konuma yerleştir ve ortasına siyah çizgi ekle
            if orientation == "Dikey":
                if j == 0:
                    x_offset = (background.width // 2 - photo.width) // 2
                    y_offset = int(0.5 * 300)
                else:
                    x_offset = background.width // 2 + (background.width // 2 - photo.width) // 2
                    y_offset = int(0.5 * 300)
                if j == 1:
                    line_width = int(0.02 * 300)
                    line_x = background.width // 2
                    draw.rectangle(
                        [line_x - line_width // 2, 0, line_x + line_width // 2, background.height],
                        fill="black"
                    )
            else:
                x_offset = (background.width - photo.width) // 2
                if j == 0:
                    y_offset = int(0.5 * 300)
                else:
                    y_offset = background.height // 2 + int(0.5 * 300)
                if j == 1:
                    line_width = int(0.02 * 300)
                    line_y = background.height // 2
                    draw.rectangle(
                        [0, line_y - line_width // 2, background.width, line_y + line_width // 2],
                        fill="black"
                    )

            output_image.paste(photo.convert("RGB"), (x_offset, y_offset))

        output_file = os.path.join(
            output_folder,
            f"Foto Eylül - {os.path.basename(input_folder)} {processed_count + 1}.jpg"
        )
        output_image.save(output_file, "JPEG")
        processed_count += 1

    # İşlem tamamlandığında bilgi ver ve klasörü aç
    messagebox.showinfo(
        "İşlem Tamamlandı",
        f"Toplam {processed_count} adet polaroid fotoğraf oluşturuldu. {invalid_count} adet hatalı fotoğraf atlandı."
    )
    open_output_folder(output_folder)
    root.quit()

# Kullanıcıdan fotoğrafları seçmesini isteyen ana işlem fonksiyonu
def start_process():
    selected_files = filedialog.askopenfilenames(
        title="Polaroid Yapılacak Fotoğrafları Seçin",
        filetypes=[("JPEG ve PNG", "*.jpg;*.jpeg;*.png")]
    )
    if not selected_files:
        return

    input_folder = os.path.dirname(selected_files[0])
    orientation = choose_orientation()
    if not orientation:
        return

    process_photos(input_folder, orientation, selected_files)

# Ana Tkinter arayüzünü başlat
root = tk.Tk()
root.title("Polaroid Oluşturucu v.2.2.6")
root.geometry("600x300")

# Logo yükle ve göster (varsa)
logo_path = os.path.join(BASE_DIR, "logo.png")
if os.path.exists(logo_path):
    pil_logo = Image.open(logo_path).resize((100, 100), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(pil_logo)
    logo_label = tk.Label(root, image=logo_img)
    logo_label.image = logo_img
    logo_label.pack(pady=10)
else:
    tk.Label(root, text="Foto Eylül", font=("Arial Black", 24)).pack(pady=10)

# Başlık
tk.Label(root, text="Polaroid Oluşturucu", font=("Arial Black", 18)).pack(pady=10)

# Fotoğraf seçme butonu
btn_select = tk.Button(
    root,
    text="Polaroid Yapılacak Fotoğrafları Seç",
    command=start_process
)
btn_select.pack(pady=20)

# Geliştirici bilgisi
tk.Label(root, text="Developer: Hakan Akınsu", font=("Arial", 10)).pack(pady=10)

# Uygulama döngüsünü başlat
root.mainloop()
