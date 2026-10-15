# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fuzzy_logic import evaluate_patient


def show_graphs(hr, rr, spo2, sbp, temp, urgency, stab_index):
    """Present different-unit inputs in a table and both indices on a 0-100 plot."""
    fig, (ax_inputs, ax_output) = plt.subplots(2, 1, figsize=(8.5, 6.5))
    ax_inputs.axis('off')
    rows = [
        ['Nabız', f'{hr:g}', 'atım/dk'],
        ['Solunum', f'{rr:g}', 'soluk/dk'],
        ['SpO₂', f'{spo2:g}', '%'],
        ['Sistolik tansiyon', f'{sbp:g}', 'mmHg'],
        ['Sıcaklık', f'{temp:g}', '°C'],
    ]
    table = ax_inputs.table(
        cellText=rows, colLabels=['Girdi', 'Değer', 'Birim'],
        loc='center', cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax_inputs.set_title('Hayati belirti girdileri (farklı birimler)')
    labels = ['Aciliyet endeksi', 'Stabilizasyon endeksi']
    bars = ax_output.bar(labels, [urgency, stab_index],
                         color=['#cc735b', '#4c83ac'], width=0.55)
    ax_output.set_ylim(0, 100)
    ax_output.set_ylabel('Model endeksi (0-100)')
    for bar, value in zip(bars, [urgency, stab_index]):
        ax_output.text(bar.get_x() + bar.get_width() / 2,
                       min(99, value + 2), f'{value:.1f}', ha='center')
    fig.tight_layout(pad=2.5)
    top = tk.Toplevel()
    top.title('Bulanık model çıktıları - klinik amaçlı değildir')
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    top.protocol('WM_DELETE_WINDOW', lambda: (plt.close(fig), top.destroy()))


def calculate():
    try:
        hr_val = float(entry_hr.get())
        rr_val = float(entry_rr.get())
        spo2_val = float(entry_spo2.get())
        sbp_val = float(entry_sbp.get())
        temp_val = float(entry_temp.get())

        urgency, stab_index = evaluate_patient(
            hr_val, rr_val, spo2_val, sbp_val, temp_val
        )
        result_label.config(
            text=f'Aciliyet endeksi: {urgency:.2f}/100 | '
                 f'Stabilizasyon endeksi: {stab_index:.2f}/100'
        )
        show_graphs(hr_val, rr_val, spo2_val, sbp_val, temp_val,
                    urgency, stab_index)
    except ValueError as exc:
        messagebox.showerror('Geçersiz girdi / hesaplama', str(exc))


# UI kurulumu
root = tk.Tk()
root.title("Bulanık Mantık - Hayati Belirti Değerlendirme Prototipi")
root.geometry("620x570")
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

warning_label = ttk.Label(root, text="Eğitim amaçlı prototip; klinik karar ve tedavi için kullanılamaz.", foreground="red")
warning_label.pack(pady=6)

calc_button = ttk.Button(root, text="Endeksleri Hesapla ve Grafikleri Göster", command=calculate)
calc_button.pack(pady=20)

result_label = ttk.Label(root, text="Endeksler burada gösterilecek (süre tahmini değildir).", foreground="blue")
result_label.pack(pady=10)

root.mainloop()