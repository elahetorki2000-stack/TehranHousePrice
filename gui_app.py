import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests

# آدرس سرور جنگو شما
API_URL = "http://127.0.0.1:8000/api/predict/"

# لیست کامل تمام محله‌های موجود در دیتابیس پروژه (housePrice.csv) به همراه معادل انگلیسی آن‌ها
ADDRESS_MAP = {
    "پونک": "Punak", "نیاوران": "Niavaran", "سعادت آباد": "Saadat Abad", "شهرک غرب": "Shahrak-e Gharb",
    "تجریش": "Tajrish", "تهرانپارس": "Tehranpars", "پیروزی": "Piroozi", "جنت آباد": "Jannat Abad",
    "مرزداران": "Marzdaran", "فرشته": "Fereshteh", "زعفرانیه": "Zaferanieh", "الهیه": "Elahieh",
    "قلهک": "Gholhak", "ولنجک": "Velenjak", "ستارخان": "Sattarkhan", "یوسف آباد": "Yousef Abad",
    "پاسداران": "Pasdaran", "شریعتی": "Shariati", "امانیه": "Amaniyeh", "آجودانیه": "Ajudaniyeh",
    "فرمانیه": "Farmanieh", "قیطریه": "Gheytarieh", "کامرانیه": "Kamranieh", "محمودیه": "Mahmoudieh",
    "دروس": "Darous", "نارمک": "Narmak", "تهرانپارس غربی": "West Tehranpars", "تهرانپارس شرقی": "East Tehranpars",
    "جنت آباد شمالی": "North Jannat Abad", "جنت آباد جنوبی": "South Jannat Abad", "جنت آباد مرکزی": "Central Jannat Abad",
    "سهروردی": "Sohrevardi", "سیدخندان": "Seyed Khandan", "عباس آباد": "Abbas Abad", "گیشا": "Gisha",
    "شهرک ژاندارمری": "Shahrak-e Jandarmeri", "طرشت": "Tarasht", "جیحون": "Jeyhoun", "کارون": "Karoon",
    "سلسبیل": "Salsabil", "آذربایجان": "Azarbaijan", "امیرآباد": "Amirabad", "ونک": "Vanak",
    "جردن": "Jordan", "ظفر": "Zafar", "میرداماد": "Mirdamad",
    "پرند": "Parand", "پردیس": "Pardis", "اندیشه": "Andisheh", "پاکدشت": "Pakdadht",
    "ری": "Ray", "چیتگر": "Chitgar", "شهرک راه آهن": "Shahrak-e Rah-Ahan", "دهکده المپیک": "Dehkadeh-ye Olampik"
}

def predict_price():
    try:
        # ۱. گرفتن متراژ
        area_val = entry_area.get().strip()
        if not area_val:
            messagebox.showwarning("خطا", "لطفاً متراژ خانه را وارد کنید.")
            return
        area = int(area_val)

        # ۲. گرفتن تعداد اتاق
        room_val = entry_room.get().strip()
        if not room_val:
            messagebox.showwarning("خطا", "لطفاً تعداد اتاق خواب را وارد کنید.")
            return
        room = int(room_val)

        # ۳. گرفتن نام محله از منوی کشویی
        persian_address = combo_address.get()
        if not persian_address or persian_address == "انتخاب کنید...":
            messagebox.showwarning("خطا", "لطفاً یک محله را انتخاب کنید.")
            return
        
        # تبدیل خودکار به انگلیسی در پشت صحنه
        address = ADDRESS_MAP.get(persian_address)

        # ۴، ۵ و ۶. گرفتن وضعیت پارکینگ, انباری و آسانسور
        parking = var_parking.get()
        warehouse = var_warehouse.get()
        elevator = var_elevator.get()

        # بسته‌بندی اطلاعات برای فرستادن به بک‌اند جنگو
        payload = {
            "Area": area,
            "Room": room,
            "Parking": parking,
            "Warehouse": warehouse,
            "Elevator": elevator,
            "Address": address
        }

        # ارسال درخواست به سرور
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            formatted_price = result.get("formatted_price", "خطا در محاسبه")
            label_result.config(text=f"قیمت پیش‌بینی شده: {formatted_price} تومان", fg="#2E7D32")
        else:
            label_result.config(text="خطا: سرور جنگو روشن نیست یا آدرس اشتباه است.", fg="#C62828")

    except ValueError:
        messagebox.showerror("خطا", "لطفاً متراژ و تعداد اتاق را فقط به صورت عدد وارد کنید.")

# ساخت پنجره اصلی برنامه
root = tk.Tk()
root.title("پیش‌بینی قیمت مسکن تهران")
root.geometry("450x560")
root.configure(bg="#F5F5F5")
root.resizable(False, False)

font_label = ("Tahoma", 10, "bold")
font_entry = ("Arial", 11)

# کادر اصلی برای راست‌چین کردن کامل المان‌ها
main_frame = tk.Frame(root, bg="#F5F5F5")
main_frame.pack(pady=20, fill="both", expand=True, padx=30)
# متراژ (راست‌چین کامل و بدون دونقطه)
lbl_area = tk.Label(main_frame, text="متراژ خانه را وارد کنید (بر اساس متر مربع)", font=font_label, bg="#F5F5F5", anchor="e")
lbl_area.pack(fill="x", pady=(10, 2))

entry_area = tk.Entry(main_frame, width=35, font=font_entry, justify="right")
entry_area.pack(ipady=3)

# تعداد اتاق (راست‌چین کامل و بدون دونقطه)
lbl_room = tk.Label(main_frame, text="تعداد اتاق خواب را وارد کنید (به عدد)", font=font_label, bg="#F5F5F5", anchor="e")
lbl_room.pack(fill="x", pady=(10, 2))

entry_room = tk.Entry(main_frame, width=35, font=font_entry, justify="right")
entry_room.pack(ipady=3)

# نام محله (راست‌چین کامل و بدون دونقطه)
lbl_address = tk.Label(main_frame, text="محله مورد نظر را انتخاب کنید", font=font_label, bg="#F5F5F5", anchor="e")
lbl_address.pack(fill="x", pady=(10, 2))

# مرتب کردن لیست محله‌ها به ترتیب الفبا
sorted_neighborhoods = sorted(list(ADDRESS_MAP.keys()))
combo_address = ttk.Combobox(main_frame, values=sorted_neighborhoods, font=("Tahoma", 10), state="readonly", justify="right")
combo_address.set("انتخاب کنید...")
combo_address.pack(fill="x", ipady=3)

# امکانات خانه
tk.Label(main_frame, text="وضعیت امکانات خانه را مشخص کنید", font=font_label, bg="#F5F5F5", anchor="e").pack(fill="x", pady=(20, 5))

# چک‌باکس‌ها (راست‌چین کامل)
var_parking = tk.BooleanVar()
c1 = tk.Checkbutton(main_frame, text="خانه دارای پارکینگ است", variable=var_parking, font=("Tahoma", 9), bg="#F5F5F5", anchor="e", justify="right")
c1.pack(fill="x", padx=10, pady=2)

var_warehouse = tk.BooleanVar()
c2 = tk.Checkbutton(main_frame, text="خانه دارای انباری است", variable=var_warehouse, font=("Tahoma", 9), bg="#F5F5F5", anchor="e", justify="right")
c2.pack(fill="x", padx=10, pady=2)

var_elevator = tk.BooleanVar()
c3 = tk.Checkbutton(main_frame, text="خانه دارای آسانسور است", variable=var_elevator, font=("Tahoma", 9), bg="#F5F5F5", anchor="e", justify="right")
c3.pack(fill="x", padx=10, pady=2)

# دکمه نهایی پیش‌بینی قیمت
btn_calc = tk.Button(main_frame, text="پیش‌بینی قیمت", command=predict_price, bg="#1565C0", fg="white", font=("Tahoma", 11, "bold"), width=22, cursor="hand2")
btn_calc.pack(pady=25)

# محل نمایش قیمت نهایی خروجی
label_result = tk.Label(main_frame, text="", font=("Tahoma", 12, "bold"), bg="#F5F5F5")
label_result.pack(pady=5)

root.mainloop()