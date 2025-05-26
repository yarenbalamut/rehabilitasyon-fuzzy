# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fuzzy_logic import evaluate_patient


def show_graphs(hr, rr, spo2, sbp, temp, urgency, stab_time):
    fig, axs = plt.subplots(2, 1, figsize=(6, 4))
    fig.tight_layout(pad=4.0)

    vital_names = ['HR', 'RR', 'SpO2', 'SBP', 'Temp']
    vital_values = [hr, rr, spo2, sbp, temp]
    axs[0].bar(vital_names, vital_values, color='skyblue')
    axs[0].set_title('Hasta Girdi Değerleri')
    axs[0].set_ylabel('Değer')

    axs[1].bar(['Aciliyet', 'Stabilizasyon Süresi'], [urgency, stab_time], color='salmon')
    axs[1].set_title('Çıkışlar')
    axs[1].set_ylabel('Skor / Zaman')

    for ax in axs:
        ax.set_ylim(0, 10)

    top = tk.Toplevel()
    top.title("Grafikler")

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack()


def calculate():
    try:
        hr_val = float(entry_hr.get())
        rr_val = float(entry_rr.get())
        spo2_val = float(entry_spo2.get())
        sbp_val = float(entry_sbp.get())
        temp_val = float(entry_temp.get())

        urgency, stab_time = evaluate_patient(hr_val, rr_val, spo2_val, sbp_val, temp_val)

        result_label.config(text=f"Acil Müdahale Seviyesi: {urgency:.2f} / Stabilizasyon Süresi: {stab_time:.2f}")

        show_graphs(hr_val, rr_val, spo2_val, sbp_val, temp_val, urgency, stab_time)

    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayılar girin.")


# UI kurulumu
root = tk.Tk()
root.title("Yoğun Bakım Stabilite Değerlendirme Sistemi")
root.geometry("500x500")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

fields = [
    ("Nabız (Heart Rate)", "hr"),
    ("Solunum Hızı (Respiratory Rate)", "rr"),
    ("Oksijen Doygunluğu (SpO2)", "spo2"),
    ("Sistolik Tansiyon (SBP)", "sbp"),
    ("Vücut Sıcaklığı (°C)", "temp")
]

entries = {}
for i, (label_text, var_name) in enumerate(fields):
    label = ttk.Label(root, text=label_text)
    label.pack(pady=(10 if i == 0 else 5, 0))
    entry = ttk.Entry(root, width=30)
    entry.pack()
    entries[var_name] = entry

entry_hr = entries['hr']
entry_rr = entries['rr']
entry_spo2 = entries['spo2']
entry_sbp = entries['sbp']
entry_temp = entries['temp']

calc_button = ttk.Button(root, text="Değerlendir ve Grafikleri Göster", command=calculate)
calc_button.pack(pady=20)

result_label = ttk.Label(root, text="Sonuçlar burada gösterilecek", foreground="blue")
result_label.pack(pady=10)

root.mainloop()