import tkinter as tk
from tkinter import ttk
import math
from tkinter import *
import codecs
from datetime import date
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import sqlite3
import webbrowser

root = Tk()
root.resizable(width=False, height=False)
selected_options = tk.StringVar()
selected_option = tk.StringVar()
combo = ttk.Combobox(root, textvariable=selected_options, width=17)
combo.grid(column=1, row=3)
combo.set("Выберите марку сплава")
#добавь вкладку о программе tkinter
menu = tk.Menu(root)
root.config(menu=menu)

def open_web(event):
    webbrowser.open_new(event.widget.cget("text"))

def about():
    about_window = tk.Toplevel(root)
    about_window.title("О программе")

    link1 = tk.Label(about_window, text="https://github.com/teslaproduuction", fg="blue", cursor="hand2")
    link1.pack()
    link1.bind("<Button-1>", open_web)

    link2 = tk.Label(about_window, text="https://t.me/T_e_s_I_a", fg="blue", cursor="hand2")
    link2.pack()
    link2.bind("<Button-1>", open_web)

    link3 = tk.Label(about_window, text="https://github.com/capitansogo", fg="blue", cursor="hand2")
    link3.pack()
    link3.bind("<Button-1>", open_web)

    link4 = tk.Label(about_window, text="https://t.me/capitansogo", fg="blue", cursor="hand2")
    link4.pack()
    link4.bind("<Button-1>", open_web)

menu = tk.Menu(root)
root.config(menu=menu)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Помощь", menu=helpmenu)
helpmenu.add_command(label="О программе", command=about)





def update_combobox():
    try:
        conn = sqlite3.connect('baza.sl3')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT марка_сплава FROM Отливки ORDER BY марка_сплава")
        result = cursor.fetchall()
        alloys = [row[0] for row in result]
        combo['values'] = alloys
        conn.close()
    except:
        messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
        return
update_combobox()


def handle_combobox_selection(event):
    selected_alloy = combo.get()
    if not selected_alloy:
        return

    conn = sqlite3.connect('baza.sl3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Отливки WHERE марка_сплава=?", (selected_alloy,))
    result = cursor.fetchone()
    conn.close()

    if result:
        # Создайте список полей ввода, которые нужно обновить
        entry_fields = [
            entry_g1, entry_g2, entry_f1, entry_s2, entry_s3, entry_s4, entry_c0, entry_c1,
            entry_r0, entry_t0, entry_t1, entry_t2, entry_t3, entry_t4, entry_t5, entry_c2,
            entry_l2, entry_a2, entry_x3, entry_l3
        ]

        # Получите индексы полей ввода в базе данных
        field_indices = list(range(2, 22))

        # Обновите поля ввода данными из базы данных
        for entry_field, field_index in zip(entry_fields, field_indices):
            field_value = result[field_index]
            if field_value is not None:
                if isinstance(field_value, str) and field_value.strip() != "":
                    entry_field.delete(0, tk.END)
                    entry_field.insert(0, field_value)
                elif isinstance(field_value, (int, float)):
                    # Если значение числовое, преобразуйте его в строку и обновите поле ввода
                    entry_field.delete(0, tk.END)
                    entry_field.insert(0, str(field_value))

            # Продолжайте так для остальных полей ввода


combo.bind("<<ComboboxSelected>>", handle_combobox_selection)
o1, o2, o3, o4, o5 = 9.81, 15.06e-6, 3.4e-3, 2.15e-5, 2.68e-2
c4, l, k0, k1 = 4178.5, 3.0, 15.0, 40.0
m_list = []
tm_list = []
entry_u = None
entry_w = None
entry_r = None
u_label = None
w_label = None
r_label = None
flag = False

try:
    def Select():
        global entry_u, entry_w, entry_r, u_label, w_label, r_label
        selected_value = selected_option.get()

        # Удаляем Entry виджеты предыдущего режима
        if entry_u:
            entry_u.destroy()
        if entry_w:
            entry_w.destroy()
        if entry_r:
            entry_r.destroy()

        # Удаляем Label виджеты предыдущего режима
        if u_label:
            u_label.destroy()
        if w_label:
            w_label.destroy()
        if r_label:
            r_label.destroy()

        if selected_value == "Heating":
            u_label = ttk.Label(root, text="Введите значение напряжения")
            u_label.grid(row=5, column=2, padx=10, columnspan=2, sticky=tk.W)
            entry_u = ttk.Entry(root)
            entry_u.grid(row=5, column=3, sticky=tk.E, padx=10)

            w_label = ttk.Label(root, text="Уд. поверхн. мощность нагревателя")
            w_label.grid(row=6, column=2, padx=10, columnspan=2,sticky=tk.W)
            entry_w = ttk.Entry(root)
            entry_w.grid(row=6, column=3, sticky=tk.E, padx=10)

            r_label = ttk.Label(root, text="Уд. электросопротивление нихрома")
            r_label.grid(row=7, column=2, padx=10, columnspan=2, sticky=tk.W)
            entry_r = ttk.Entry(root)
            entry_r.grid(row=7, column=3, sticky=tk.E, padx=10)


    def check_input():
        # Проверьте, что все поля ввода имеют значения
        if (
                not entry_a.get()
                or not entry_b.get()
                or not entry_d.get()
                or not entry_m.get()
                or not entry_g1.get()
                or not entry_g2.get()
                or not entry_f1.get()
                or not entry_s2.get()
                or not entry_s3.get()
                or not entry_s4.get()
                or not entry_c0.get()
                or not entry_c1.get()
                or not entry_r0.get()
                or not entry_t0.get()
                or not entry_t1.get()
                or not entry_t2.get()
                or not entry_t3.get()
                or not entry_t4.get()
                or not entry_t5.get()
                or not entry_c2.get()
                or not entry_l2.get()
                or not entry_a2.get()
                or not entry_x3.get()
                or not entry_l3.get()
                or not entry_n.get()
                # Добавь проверку что все эти значения не отрицательные



                or not is_positive(entry_g1.get())
                or not is_positive(entry_g2.get())
                or not is_positive(entry_f1.get())
                or not is_positive(entry_s2.get())
                or not is_positive(entry_s3.get())
                or not is_positive(entry_s4.get())
                or not is_positive(entry_c0.get())
                or not is_positive(entry_c1.get())
                or not is_positive(entry_r0.get())
                or not is_positive(entry_t0.get())
                or not is_positive(entry_t1.get())
                or not is_positive(entry_t2.get())
                or not is_positive(entry_t3.get())
                or not is_positive(entry_t4.get())
                or not is_positive(entry_t5.get())
                or not is_positive(entry_c2.get())
                or not is_positive(entry_l2.get())
                or not is_positive(entry_a2.get())
                or not is_positive(entry_x3.get())
                or not is_positive(entry_l3.get())
                or not is_positive(entry_n.get())

                or float(entry_x3.get()) > 5
                or float(entry_r0.get()) > 9999999
        ):
            messagebox.showerror("Ошибка",
                                 "Пожалуйста, заполните все поля ввода и убедитесь, что значения неотрицательные")
        else:
            # Если все поля заполнены и х3 не больше 5, выполните расчет
            calculate_heat_transfer()


    def is_positive(value):
        try:
            float_value = float(value)

            return float_value >= 0
        except ValueError:
            return False


    def generate_plot():
        root2 = Tk()
        root2.resizable(width=False, height=False)
        root2.title("График")
        plt.clf()
        # Create a plot
        fig, ax = plt.subplots(dpi=150)
        ax.grid()
        ax.plot(m_list, tm_list, marker='o', linestyle='-')
        ax.set_xlabel('Время (сек)')
        ax.set_ylabel('Температура (град)')
        ax.set_title('Изменение температуры отливки во времени')

        canvas = FigureCanvasTkAgg(fig, master=root2)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0)
        fig.savefig("график.png")


    def update_text_widget():
        # text_widget.grid(row=5, column=2, columnspan=3, rowspan=18, padx=10)
        with codecs.open("Данные.txt", "r", "utf-8") as f:
            file_contents = f.read()
            text_widget.delete(1.0, "end")  # Clear the current contents
            text_widget.insert("end", file_contents)  # Insert the file contents
        f.close()


    def calculate_heat_transfer():
        m_list.clear()
        tm_list.clear()

        try:
            a = entry_a.get()
            b = entry_b.get()
            d = entry_d.get()
            m = entry_m.get()
            # Добавьте базовые значения в поля ввода

            g1 = float(entry_g1.get())
            g2 = float(entry_g2.get())
            f1 = float(entry_f1.get())

            s2 = float(entry_s2.get())
            s3 = float(entry_s3.get())
            s4 = float(entry_s4.get())

            c0 = float(entry_c0.get())
            c1 = float(entry_c1.get())
            r0 = float(entry_r0.get())

            t0 = float(entry_t0.get())
            t1 = float(entry_t1.get())
            t2 = float(entry_t2.get())
            t3 = float(entry_t3.get())
            t4 = float(entry_t4.get())
            t5 = float(entry_t5.get())

            c2 = float(entry_c2.get())
            l2 = float(entry_l2.get())
            a2 = float(entry_a2.get())

            x3 = float(entry_x3.get())
            l3 = float(entry_l3.get())
            n0 = float(entry_n.get())
        except:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.1")
            with codecs.open("Данные.txt", "w", "utf-8") as f:
                print(f"Ошибка", file=f)
                print(f"Введены неверные данные", file=f)
                f.close()
            m_list.clear()
            tm_list.clear()
            update_text_widget()
            return
        #рассчет времени охлаждения отливки
        try:
            flag = False
            c3 = ((c0 + c1) / 2) + (r0 / (t3 - t2))
            t6 = (t4 + r0 / c0 + t1 * (g2 / g1) * (c2 / c1)) / (1 + (g2 * c2) / (g1 * c1))
            a1 = l3 / x3 * (t4 - t1) / (t4 - t6)
            n1 = -((g1 * c0) / (f1 * a1)) * math.log((t3 - t6) / (t4 - t6))
            n2 = -((g1 * c3) / (f1 * a1)) * math.log((t2 - t6) / (t3 - t6))
            #лютый костыль с логарифмом
            try:
                n3 = -((g1 * c1) / (f1 * a1)) * math.log((t5 - t6) / (t2 - t6))
            except:
                n3 = -((g1 * c1) / (f1 * a1)) * -1
                flag = True
            n4 = n1 + n2 + n3

            n = int(round(n4))
            if n <= 0:
                     raise ValueError("Значение переменной должно быть неотрицательным.")
        except:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.2")
            with codecs.open("Данные.txt", "w", "utf-8") as f:
                print(f"Ошибка", file=f)
                print(f"Введены неверные данные", file=f)
                f.close()
            m_list.clear()
            tm_list.clear()
            update_text_widget()
            return

        with codecs.open("Данные.txt", "w", "utf-8") as f:
            try:
                print(f"РАСЧЕТ ТЕПЛОВОГО БАЛАНСА ПРЕСС-ФОРМЫ", file=f)
                print(f"{a} группа: {b} {date.today()}", file=f)
                print(f"{d} {m}", file=f)
                print(file=f)
                print("Результаты расчета", file=f)
                print(" " + "=" * 18, file=f)
                print(file=f)
                if flag == True:    #проверка на лютый костыль
                    print(f"1. Время охлаждения отливки = {n:3d} c (условно)", file=f)
                else:
                    print(f"1. Время охлаждения отливки = {n:3d} c", file=f)

                # расчет температуры отливки и рабочей поверхности пресс-формы

                print("2. Изменение температ. отливки во времени", file=f)
                print(" " * 4 + "| ВРЕМЯ (сек) | ТЕМПЕРАТУРА (град) |", file=f)
                print(" " * 4 + "|" + "-" * 34 + "|", file=f)
            except:
                messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.3")
                with codecs.open("Данные.txt", "w", "utf-8") as f:
                    print(f"Ошибка", file=f)
                    print(f"Введены неверные данные", file=f)
                    f.close()
                m_list.clear()
                tm_list.clear()
                update_text_widget()

                with codecs.open("Данные.txt", "w", "utf-8") as f:
                    print(f"Ошибка", file=f)
                    print(f"Введены неверные данные", file=f)
                    f.close()
                return
            try:
                b1 = (t4 - t3) / n1
                b2 = (t3 - t2) / n2
                b3 = (t2 - t5) / n3
                y2 = t3 + b2 * n1
                y3 = t2 + b3 * (n1 + n2)
                t = [0] * (n + 1)
                for m in range(n + 1):
                    if m < n1:
                        t[m] = t4 - b1 * m
                    elif m < (n1 + n2):
                        t[m] = y2 - b2 * m
                    else:
                        t[m] = y3 - b3 * m

                    print(f" " * 4 + f"| {m: <11d} | {t[m]: <15.0f} |", file=f)
                    m_list.append(m)
                    tm_list.append(t[m])

                print(" " * 4 + "|" + "-" * 34 + "|", file=f)

                m = n
                t8 = t[m]
                print(f"3. Темп.раб.поверхности в момент раскрытия пресс-формы = {t8:3.0f} град", file=f)

                q1 = g1 * (c0 * (t4 - t3) + c3 * (t3 - t2) + c1 * (t2 - t5))
                t8 = t1
                a9 = heat_transfer_coef(t8, t0, s3)
                q3 = a9 * 2 * (s2 * s4 + s3 * s4) * (n + n0) + (t1 - t0)
                print(f"4. Коэфф.теплоотдачи с наружной поверх. = {a9:7.2f}", file=f)

                m = n
                t8 = t[m]
                a0 = heat_transfer_coef(t8, t0, s3)
                q4 = a0 * 1.5 * s2 * s3 * n0 * (t8 - t0)
                print(f"5. Коэфф.теплоотдачи с рабочей поверхн. = {a0:7.2f}", file=f)

                q2 = q3 + q4

                print(f"6. Кол. подводимой теплоты = {q1:9.1f}", file=f)
                print(f"7. Кол. отводимой  теплоты = {q2:9.1f}", file=f)

                f.close()
                handle_option_selection(n, n0, q1, q2,entry_u, entry_w, entry_r)
                update_text_widget()
            except:
                messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.4")
                with codecs.open("Данные.txt", "w", "utf-8") as f:
                    print(f"Ошибка", file=f)
                    print(f"Введены неверные данные", file=f)
                    f.close()
                m_list.clear()
                tm_list.clear()
                update_text_widget()

                return
        return s3


    # Function to handle the selection of radio buttons

    def handle_option_selection(n, n0, q1, q2,entry_u, entry_w, entry_r):
        with codecs.open("Данные.txt", "a", "utf-8") as f:
            selected_value = selected_option.get()
            if selected_value == "Cooling":
                try:
                    if q1 >= q2:

                        # entry_e.delete(0, tk.END)
                        # entry_e.insert(0, "С наружной поверхности")
                        print("8. Пресс-форма имеет систему водоохлаждения.", file=f)
                        g3 = 3.6 * (q1 - q2) / (c4 * (k1 - k0) * (n + n0))
                        d = (math.sqrt(2 * g3 / (3.14 * l)) * 1000) / 60
                        print(f"9. Объемный расход воды = {g3:7.2f} куб.м/ч", file=f)
                        print(f"10. Диаметр трубки       = {d:7.2f} мм", file=f)
                    else:
                        messagebox.showerror("Ошибка", "Опция выбрана неправильно")
                except:
                    messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.5")
                    with codecs.open("Данные.txt", "w", "utf-8") as f:
                        print(f"Ошибка", file=f)
                        print(f"Введены неверные данные", file=f)
                        f.close()
                    m_list.clear()
                    tm_list.clear()
                    update_text_widget()
                    return


            elif selected_value == "Heating":
                if q1 <= q2:

                    try:
                        u = float(entry_u.get())
                        w = float(entry_w.get())
                        r = float(entry_r.get())

                    except:
                        messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.6")
                        with codecs.open("Данные.txt", "w", "utf-8") as f:
                            print(f"Ошибка", file=f)
                            print(f"Введены неверные данные", file=f)
                            f.close()
                        m_list.clear()
                        tm_list.clear()
                        update_text_widget()
                        return
                    p1 = 1.5 * (q2 - q1) / 1000 * (n + n0)
                    d1 = (4 * 1e11 + 11 * p1 ** 2 * r / 3.14 ** 2 * u ** 2 * w) ** 0.33
                    l1 = u ** 2 * 3.14 * d1 ** 2 / 4 * r * 1e9 * p1
                    print(f"9. Мощность нагревателя = {p1:7.2f} ВТ", file=f)
                    print(f"10. Диаметр проволоки нагревателя = {d1:7.2f} мм", file=f)
                    print(f"11. Длина   проволоки нагревателя = {l1:7.2f} м", file=f)
                else:
                    messagebox.showerror("Ошибка", "Опция выбрана неправильно")

            elif selected_value == "Balance":
                if abs(q1 - q2) < 0.2 * max(q1, q2):
                    # entry_e.delete(0, tk.END)
                    # entry_e.insert(0, "Баланс")

                    print("\nВерно, пресс-форма на требует системы охлаждения или нагрева.")
                    print("8. Пресс-форма на требует системы охлаждения или нагрева.", file=f)
                    # else:
                    # entry_e.delete(0, tk.END)
                    # entry_e.insert(0, "")
                else:
                    messagebox.showerror("Ошибка", "Опция выбрана неправильно")
        f.close()


    # Теплоотдача
    def heat_transfer_coef(t8, t0, s3):
        g = (o1 * s3 ** 3 * o3 * (t8 - t0)) / o2 ** 2
        p = o2 / o4
        z = g * p

        if z == 1e9:
            a = (.388 * z ** 0.3) * (o5 / s3)
        elif z < 1e9:
            a = (.695 * z ** 0.25) * (o5 / s3)
        else:
            a = (.133 * z ** 0.33) * (o5 / s3)

        return a


    # Тепловой баланс

    root.title("РАСЧЕТ ТЕПЛОВОГО БАЛАНСА ПРЕСС-ФОРМЫ")


    # Ввод данных
    ttk.Label(root, text="Фамилия, И., О.", anchor='w').grid(row=0, column=0, padx=10, sticky=tk.W)
    entry_a = ttk.Entry(root)
    entry_a.grid(row=0, column=1)

    ttk.Label(root, text="Шифр группы").grid(row=1, column=0, padx=10, sticky=tk.W)
    entry_b = ttk.Entry(root)
    entry_b.grid(row=1, column=1)

    ttk.Label(root, text="Наименование отливки").grid(row=2, column=0, padx=10, sticky=tk.W)
    entry_d = ttk.Entry(root)
    entry_d.grid(row=2, column=1)

    ttk.Label(root, text="Выбрать готовый вариант из БД").grid(row=3, column=0, padx=10, sticky=tk.W)

    ttk.Label(root, text="Марка сплава").grid(row=4, column=0, padx=10, sticky=tk.W)
    entry_m = ttk.Entry(root)
    entry_m.grid(row=4, column=1)

    ttk.Label(root, text="Вес отливки").grid(row=5, column=0, padx=10, sticky=tk.W)
    entry_g1 = ttk.Entry(root)
    entry_g1.grid(row=5, column=1)

    ttk.Label(root, text="Вес пресс-формы").grid(row=6, column=0, padx=10, sticky=tk.W)
    entry_g2 = ttk.Entry(root)
    entry_g2.grid(row=6, column=1)

    ttk.Label(root, text="Площадь поверхности отливки по плоскости разъема").grid(row=7, column=0, padx=10,
                                                                                   sticky=tk.W)
    entry_f1 = ttk.Entry(root)
    entry_f1.grid(row=7, column=1)

    ttk.Label(root, text="Ширина  пресс-формы").grid(row=8, column=0, padx=10, sticky=tk.W)
    entry_s2 = ttk.Entry(root)
    entry_s2.grid(row=8, column=1)

    ttk.Label(root, text="Высота  пресс-формы").grid(row=9, column=0, padx=10, sticky=tk.W)
    entry_s3 = ttk.Entry(root)
    entry_s3.grid(row=9, column=1)

    ttk.Label(root, text="Толщина пресс-формы").grid(row=10, column=0, padx=10, sticky=tk.W)
    entry_s4 = ttk.Entry(root)
    entry_s4.grid(row=10, column=1)

    ttk.Label(root, text="Теплоемкость жидкого сплава").grid(row=11, column=0, padx=10, sticky=tk.W)
    entry_c0 = ttk.Entry(root)
    entry_c0.grid(row=11, column=1)

    ttk.Label(root, text="Теплоемкость твердого сплава").grid(row=12, column=0, padx=10, sticky=tk.W)
    entry_c1 = ttk.Entry(root)
    entry_c1.grid(row=12, column=1)

    ttk.Label(root, text="Скрытая теплота кристаллизации").grid(row=13, column=0, padx=10, sticky=tk.W)
    entry_r0 = ttk.Entry(root)
    entry_r0.grid(row=13, column=1)

    ttk.Label(root, text="Температура окружающей среды").grid(row=14, column=0, padx=10, sticky=tk.W)
    entry_t0 = ttk.Entry(root)
    entry_t0.grid(row=14, column=1)

    ttk.Label(root, text="Начальная температура пресс-формы").grid(row=15, column=0, padx=10, sticky=tk.W)
    entry_t1 = ttk.Entry(root)
    entry_t1.grid(row=15, column=1)

    ttk.Label(root, text="Температура солидуса").grid(row=16, column=0, padx=10, sticky=tk.W)
    entry_t2 = ttk.Entry(root)
    entry_t2.grid(row=16, column=1)

    ttk.Label(root, text="Температура ликвидуса").grid(row=17, column=0, padx=10, sticky=tk.W)
    entry_t3 = ttk.Entry(root)
    entry_t3.grid(row=17, column=1)

    ttk.Label(root, text="Температура заливки").grid(row=18, column=0, padx=10, sticky=tk.W)
    entry_t4 = ttk.Entry(root)
    entry_t4.grid(row=18, column=1)

    ttk.Label(root, text="Температура удаления отливки").grid(row=19, column=0, padx=10, sticky=tk.W)
    entry_t5 = ttk.Entry(root)
    entry_t5.grid(row=19, column=1)

    ttk.Label(root, text="Теплоемкость материала пресс-формы").grid(row=20, column=0, padx=10, sticky=tk.W)
    entry_c2 = ttk.Entry(root)
    entry_c2.grid(row=20, column=1)

    ttk.Label(root, text="Теплопроводность материала пресс-формы").grid(row=21, column=0, padx=10, sticky=tk.W)
    entry_l2 = ttk.Entry(root)
    entry_l2.grid(row=21, column=1)

    ttk.Label(root, text="Температуропроводность").grid(row=22, column=0, padx=10, sticky=tk.W)
    entry_a2 = ttk.Entry(root)
    entry_a2.grid(row=22, column=1)

    ttk.Label(root, text="Толщина слоя краски").grid(row=23, column=0, padx=10, sticky=tk.W)
    entry_x3 = ttk.Entry(root)
    entry_x3.grid(row=23, column=1)

    ttk.Label(root, text="Теплопроводность слоя краски").grid(row=24, column=0, padx=10, sticky=tk.W)
    entry_l3 = ttk.Entry(root)
    entry_l3.grid(row=24, column=1)

    # Ввод времени охлаждения отливки
    ttk.Label(root, text="Длительность раскрытия пресс-формы").grid(row=25, column=0, padx=10, sticky=tk.W)
    entry_n = ttk.Entry(root)
    entry_n.grid(row=25, column=1)

    # Ввод температуры окружающей среды

    # Кнопка для расчета
    ttk.Button(root, text="Рассчитать", command=check_input,width=25).grid(row=0, column=2,
                                                                   sticky=tk.W, padx=10)

    # Вопрос о системе охлаждения или нагрева
    # Create radio buttons
    ttk.Label(root, text="Выберите опцию:").grid(row=1, column=2, columnspan=3, sticky=tk.W, padx=10)
    cooling_radio = ttk.Radiobutton(root, text="Охлаждение", variable=selected_option, value="Cooling", command=Select)
    heating_radio = ttk.Radiobutton(root, text="Нагрев", variable=selected_option, value="Heating", command=Select)
    balance_radio = ttk.Radiobutton(root, text="Баланс", variable=selected_option, value="Balance", command=Select)

    cooling_radio.grid(row=2, column=2, columnspan=3, sticky=tk.W, padx=10)
    heating_radio.grid(row=3, column=2, columnspan=3, sticky=tk.W, padx=10)
    balance_radio.grid(row=4, column=2, columnspan=3, sticky=tk.W, padx=10)

    # Add a text widget to display the file contents
    text_widget = Text(root, wrap=tk.WORD, width=60, height=23, padx=10)
    text_widget.grid(row=8, column=2, columnspan=3, rowspan=18, padx=10)

    # Add a button to update the text widget
    update_button = ttk.Button(root, text="Данные", command=update_text_widget,width=25)
    update_button.grid(row=0, column=3, sticky=tk.W, padx=10)

    plot_button = ttk.Button(root, text="График", command=generate_plot,width=25)
    plot_button.grid(row=0, column=4, sticky=tk.W, padx=10)

    entry_a.insert(0, "Фамилия, И., О.")
    entry_b.insert(0, "Шифр группы")
    entry_d.insert(0, "Наименование отливки")
    entry_m.insert(0, "Марка сплава")
    entry_n.insert(0, "90")




except:
    messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение.7")
    with codecs.open("Данные.txt", "w", "utf-8") as f:
        print(f"Ошибка", file=f)
        print(f"Введены неверные данные", file=f)
        f.close()
    m_list.clear()
    tm_list.clear()
    update_text_widget()


root.mainloop()