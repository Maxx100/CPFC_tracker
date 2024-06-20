import customtkinter as ctk
import tkinter as tk
from data import data
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import shuffle


class MainApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("CPFC tracker")
		self.geometry("1000x600")  # as default, if zooming/moving
		# self.iconbitmap("ico.ico")
		# self.overrideredirect(True)  # hehe. alt+tab or alt+f4
		# self.resizable(False, False)

		ctk.set_default_color_theme("green")
		ctk.set_appearance_mode("light")
		self.font = tk.font.nametofont("TkDefaultFont")
		self.font.configure(family="HSE Sans")

		# -------------- grid for all windows --------------
		self.grid_columnconfigure(0, weight=100)
		self.grid_columnconfigure(1, weight=1)
		# self.grid_columnconfigure((2, 3), weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		# -------------- left win --------------
		self.main_win = ctk.CTkFrame(self, corner_radius=15)
		self.main_win.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=(10, 10), padx=(10, 10))
		self.main_win.grid_rowconfigure(4, weight=1)
		self.main_win.grid_propagate(False)

		# -------------- windows for left win --------------
		self.windows = {
			"Main Page": ctk.CTkFrame(self.main_win, corner_radius=15),
			"Graphics": ctk.CTkFrame(self.main_win, corner_radius=15),
			"Settings": ctk.CTkFrame(self.main_win, corner_radius=15)
		}

		# -------------- win1: Main win --------------
		self.add_label = ctk.CTkLabel(
			self.windows['Main Page'], text="Добавить запись:",
			font=ctk.CTkFont(size=20)
		)
		self.add_label.grid(row=0, column=0, padx=20, pady=(20, 20))

		self.add_place_label = ctk.CTkLabel(
			self.windows['Main Page'], text="продукт:",
			font=ctk.CTkFont(size=20)
		)
		self.add_place_label.grid(row=0, column=1, padx=20, pady=(20, 20))

		self.add_place = ctk.CTkOptionMenu(
			self.windows['Main Page'], values=sorted(list(data.products.keys()))
		)
		self.add_place.grid(row=0, column=2, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.add_label = ctk.CTkLabel(
			self.windows['Main Page'], text="грамм:",
			font=ctk.CTkFont(size=20)
		)
		self.add_label.grid(row=1, column=1, padx=20, pady=(20, 20))

		self.add_cal = ctk.CTkEntry(self.windows['Main Page'], placeholder_text="0 гр")
		# self.add_cal.insert(0, string="0")
		self.add_cal.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.add_button = ctk.CTkButton(
			master=self.windows['Main Page'], fg_color="transparent", command=self.add_to_history,
			border_width=2, text_color=("gray10", "#DCE4EE"), text="добавить"
		)
		self.add_button.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.history = ctk.CTkTextbox(self.windows["Main Page"], width=500, height=300)
		self.history.grid(row=4, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
		self.history.insert("0.0", "\n".join([i.beauty_str() for i in data.history]))

		# -------------- win2: Graphics --------------
		self.graphic_win = ctk.CTkFrame(self.windows['Graphics'], corner_radius=15)
		self.graphic_win.grid(row=0, column=0, pady=(10, 10), padx=(10, 10))
		# self.graphic_win.grid_rowconfigure(4, weight=1)
		# self.graphic_win.grid_propagate(False)

		self.info_graphic_win = ctk.CTkFrame(self.windows['Graphics'], corner_radius=15)
		self.info_graphic_win.grid(row=0, column=1, pady=(10, 10), padx=(10, 10))
		# self.graphic_win.grid_rowconfigure(4, weight=1)
		# self.info_graphic_win.grid_propagate(False)

		self.plot = None

		self.avg_k_info_label = ctk.CTkLabel(self.info_graphic_win, text="Среднее по калориям:", anchor="w")
		self.avg_k_info_label.grid(row=0, column=1, padx=10, pady=10)
		self.avg_p_info_label = ctk.CTkLabel(self.info_graphic_win, text="Среднее по белкам:", anchor="w")
		self.avg_p_info_label.grid(row=1, column=1, padx=10, pady=10)
		self.avg_f_info_label = ctk.CTkLabel(self.info_graphic_win, text="Среднее по жирам:", anchor="w")
		self.avg_f_info_label.grid(row=2, column=1, padx=10, pady=10)
		self.avg_c_info_label = ctk.CTkLabel(self.info_graphic_win, text="Среднее по\nуглеводам:", anchor="w")
		self.avg_c_info_label.grid(row=3, column=1, padx=10, pady=10)
		self.advice_info_label = ctk.CTkLabel(self.info_graphic_win, text="Предложения:", anchor="w")
		self.advice_info_label.grid(row=4, column=1, padx=10, pady=10)

		self.avg_k_label = ctk.CTkLabel(
			self.info_graphic_win,
			anchor="w"
		)
		self.avg_k_label.grid(row=0, column=2, padx=10, pady=10)

		self.avg_p_label = ctk.CTkLabel(
			self.info_graphic_win,
			anchor="w"
		)
		self.avg_p_label.grid(row=1, column=2, padx=10, pady=10)

		self.avg_f_label = ctk.CTkLabel(
			self.info_graphic_win,
			anchor="w"
		)
		self.avg_f_label.grid(row=2, column=2, padx=10, pady=10)

		self.avg_c_label = ctk.CTkLabel(
			self.info_graphic_win,
			anchor="w"
		)
		self.avg_c_label.grid(row=3, column=2, padx=10, pady=10)

		self.advice_label = ctk.CTkLabel(
			self.info_graphic_win,
			anchor="w"
		)
		self.advice_label.grid(row=4, column=2, padx=10, pady=10)

		self.summary_days = None
		self.days = None

		# -------------- win3: Settings (User Data) --------------
		self.name_settings_age = ctk.CTkLabel(
			self.windows['Settings'], text="возраст:",
			font=ctk.CTkFont(size=20)
		)
		self.name_settings_age.grid(row=0, column=0, padx=10, pady=(10, 10))
		self.age_place = ctk.CTkEntry(self.windows['Settings'], placeholder_text="Возраст")
		self.age_place.insert(0, string=str(data.age))
		self.age_place.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.name_settings_weight = ctk.CTkLabel(
			self.windows['Settings'], text="вес:",
			font=ctk.CTkFont(size=20)
		)
		self.name_settings_weight.grid(row=1, column=0, padx=10, pady=(10, 10))
		self.weight_place = ctk.CTkEntry(self.windows['Settings'], placeholder_text="")
		self.weight_place.insert(0, string=str(data.weight))
		self.weight_place.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.name_settings_height = ctk.CTkLabel(
			self.windows['Settings'], text="рост:",
			font=ctk.CTkFont(size=20)
		)
		self.name_settings_height.grid(row=2, column=0, padx=10, pady=(10, 10))
		self.height_place = ctk.CTkEntry(self.windows['Settings'], placeholder_text="")
		self.height_place.insert(0, string=str(data.height))
		self.height_place.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.name_settings_sex = ctk.CTkLabel(
			self.windows['Settings'], text="пол:",
			font=ctk.CTkFont(size=20)
		)
		self.name_settings_sex.grid(row=3, column=0, padx=10, pady=(10, 10))
		self.sex_place = ctk.CTkOptionMenu(
			self.windows['Settings'], values=["Мужской", "Женский"], command=self.set_sex
		)
		self.sex_place.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
		self.sex_place.set({"man": "Мужской", "woman": "Женский"}[data.sex])

		self.name_settings_rate = ctk.CTkLabel(
			self.windows['Settings'], text="образ жизни:",
			font=ctk.CTkFont(size=20)
		)
		self.name_settings_rate.grid(row=4, column=0, padx=10, pady=(10, 10))
		self.rate_place = ctk.CTkOptionMenu(
			self.windows['Settings'], values=["Сидячий", "Средний", "Активный"], command=self.set_rate
		)
		self.rate_place.grid(row=4, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
		self.rate_place.set({1.2: "Сидячий", 1.5: "Средний", 1.7: "Активный"}[data.rate])

		self.save_button = ctk.CTkButton(
			master=self.windows['Settings'], fg_color="transparent", command=self.data_save,
			border_width=2, text_color=("gray10", "#DCE4EE"), text="Сохранить"
		)
		self.save_button.grid(row=5, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

		self.need_cal = ctk.CTkLabel(
			self.windows['Settings'], text="калории:",
			font=ctk.CTkFont(size=20)
		)
		self.need_cal.grid(row=0, column=3, padx=10, pady=(10, 10))
		self.need_cal_value = ctk.CTkLabel(
			self.windows['Settings'], text=str(data.get_normal_cpfc()[0]),
			font=ctk.CTkFont(size=20)
		)
		self.need_cal_value.grid(row=0, column=4, padx=10, pady=(10, 10))

		self.need_p = ctk.CTkLabel(
			self.windows['Settings'], text="белки:",
			font=ctk.CTkFont(size=20)
		)
		self.need_p.grid(row=1, column=3, padx=10, pady=(10, 10))
		self.need_p_value = ctk.CTkLabel(
			self.windows['Settings'], text=str(data.get_normal_cpfc()[1]),
			font=ctk.CTkFont(size=20)
		)
		self.need_p_value.grid(row=1, column=4, padx=10, pady=(10, 10))

		self.need_f = ctk.CTkLabel(
			self.windows['Settings'], text="жиры:",
			font=ctk.CTkFont(size=20)
		)
		self.need_f.grid(row=2, column=3, padx=10, pady=(10, 10))
		self.need_f_value = ctk.CTkLabel(
			self.windows['Settings'], text=str(data.get_normal_cpfc()[2]),
			font=ctk.CTkFont(size=20)
		)
		self.need_f_value.grid(row=2, column=4, padx=10, pady=(10, 10))

		self.need_c = ctk.CTkLabel(
			self.windows['Settings'], text="углеводы:",
			font=ctk.CTkFont(size=20)
		)
		self.need_c.grid(row=3, column=3, padx=10, pady=(10, 10))
		self.need_c_value = ctk.CTkLabel(
			self.windows['Settings'], text=str(data.get_normal_cpfc()[3]),
			font=ctk.CTkFont(size=20)
		)
		self.need_c_value.grid(row=3, column=4, padx=10, pady=(10, 10))

		# -------------- right win (Menu) --------------
		self.settings = ctk.CTkFrame(self, width=200, corner_radius=15)
		self.settings.grid(row=0, column=3, rowspan=4, sticky="nsew", pady=(10, 10), padx=(10, 10))
		self.settings.grid_rowconfigure(4, weight=1)
		self.settings.grid_propagate(False)

		self.name_as_logo = ctk.CTkLabel(
			self.settings, text="Трекер КБЖУ",
			font=ctk.CTkFont(size=20, weight="bold")
		)
		self.name_as_logo.grid(row=0, column=3, padx=10, pady=(15, 10))

		# -------------- win changer --------------
		self.selected_win = tk.StringVar(value="Main Page")
		self.win1 = ctk.CTkRadioButton(
			master=self.settings, variable=self.selected_win, value="Main Page",
			command=self.win_change, text="Главное меню"
		)
		self.win1.grid(row=1, column=3, pady=10, padx=20, sticky="w")
		self.win2 = ctk.CTkRadioButton(
			master=self.settings, variable=self.selected_win, value="Graphics",
			command=self.win_change, text="Статистика"
		)
		self.win2.grid(row=2, column=3, pady=10, padx=20, sticky="w")
		self.win3 = ctk.CTkRadioButton(
			master=self.settings, variable=self.selected_win, value="Settings",
			command=self.win_change, text="Данные"
		)
		self.win3.grid(row=3, column=3, pady=10, padx=20, sticky="w")

		# -------------- Theme settings (Light as default, system for MacOS?) --------------
		self.theme_label = ctk.CTkLabel(self.settings, text="Тема:", anchor="w")
		self.theme_label.grid(row=5, column=3, padx=20, pady=(10, 0))
		self.theme_mode = ctk.CTkOptionMenu(self.settings, values=["Светлая", "Темная"], command=self.theme_change)
		self.theme_mode.grid(row=6, column=3, padx=20, pady=(10, 10))

		# -------------- Last settings (after init) --------------
		self.after(0, lambda: self.state('zoomed'))
		self.win_change()

	@staticmethod
	def theme_change(mode: str):
		if mode == "Светлая":
			ctk.set_appearance_mode("light")
		else:
			ctk.set_appearance_mode("dark")

	def add_to_history(self):
		data.add(self.add_place.get(), self.add_cal.get())
		self.history.insert("0.0", data.history[-1].beauty_str() + "\n")

	@staticmethod
	def set_sex(sex: str):
		if sex == "Мужской":
			data.sex = "man"
		else:
			data.sex = "woman"

	@staticmethod
	def set_rate(rate: str):
		if rate == "Сидячий":
			data.rate = 1.2
		elif rate == "Средний":
			data.rate = 1.5
		else:
			data.rate = 1.7

	def data_save(self):
		data.save(new_data={
				"age": self.age_place.get(),
				"weight": self.weight_place.get(),
				"sex": data.sex,
				"height": self.height_place.get(),
				"rate": data.rate
			}
		)
		temp = data.get_normal_cpfc()
		self.need_cal_value.configure(text=str(temp[0]))
		self.need_p_value.configure(text=str(temp[1]))
		self.need_f_value.configure(text=str(temp[2]))
		self.need_c_value.configure(text=str(temp[3]))

	def statistics(self):
		self.days = {_: [] for _ in range(0, 7)}
		self.summary_days = [[0, 0, 0, 0] for _ in range(7)]
		for i in data.history:
			temp = (datetime.now() - i.datetime).days
			if 0 <= temp < 7:
				self.days[temp].append(i)
				for _ in range(4):
					self.summary_days[temp][_] += round(data.products[i.name][_] * (i.cal / 100), 3)

		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(7, 7), dpi=90)
		ax1.set_title('Калории')
		ax2.set_title('Белки')
		ax3.set_title('Жиры')
		ax4.set_title('Углеводы')

		ax1.plot(list(self.days.keys()), [i[3] for i in self.summary_days[::]], label="Ваша статистика")
		ax2.plot(list(self.days.keys()), [i[0] for i in self.summary_days[::]], label="Ваша статистика")
		ax3.plot(list(self.days.keys()), [i[1] for i in self.summary_days[::]], label="Ваша статистика")
		ax4.plot(list(self.days.keys()), [i[2] for i in self.summary_days[::]], label="Ваша статистика")

		ax1.plot(list(self.days.keys()), [data.get_normal_cpfc()[0]] * 7, label="Ваша норма")
		ax2.plot(list(self.days.keys()), [data.get_normal_cpfc()[1]] * 7, label="Ваша норма")
		ax3.plot(list(self.days.keys()), [data.get_normal_cpfc()[2]] * 7, label="Ваша норма")
		ax4.plot(list(self.days.keys()), [data.get_normal_cpfc()[3]] * 7, label="Ваша норма")

		ax1.legend()
		ax2.legend()
		ax3.legend()
		ax4.legend()

		# plt.legend()
		self.graphic_win.grid_forget()
		self.graphic_win.grid(row=0, column=0, pady=(10, 10), padx=(10, 10))
		self.info_graphic_win.grid(row=0, column=1, pady=(10, 10), padx=(10, 10))
		if self.plot:
			self.plot.get_tk_widget().grid_forget()
		self.plot = FigureCanvasTkAgg(fig, self.graphic_win)
		self.plot.get_tk_widget().grid()

		self.avg_k_label.configure(
			text=str(int(sum([i[3] for i in self.summary_days[::-1]]) // 7))
		)

		self.avg_p_label.configure(
			text=str(int(sum([i[0] for i in self.summary_days[::-1]]) // 7))
		)

		self.avg_f_label.configure(
			text=str(int(sum([i[1] for i in self.summary_days[::-1]]) // 7))
		)

		self.avg_c_label.configure(
			text=str(int(sum([i[2] for i in self.summary_days[::-1]]) // 7))
		)

		temp = [
			self.summary_days[0][3] / data.get_normal_cpfc()[0] * 100,
			self.summary_days[0][0] / data.get_normal_cpfc()[1] * 100,
			self.summary_days[0][1] / data.get_normal_cpfc()[2] * 100,
			self.summary_days[0][2] / data.get_normal_cpfc()[3] * 100
		]
		mid_temp = sum(temp) / 4
		target = [False, False, False, False]
		for i in range(4):
			if temp[i] > 1:
				continue
			if mid_temp - temp[i] > 20:
				target[i] = True
		advices = []
		avg_by_products = [0.0646658760749548, 0.027321294296638796, 0.14091622481143773]
		for i in data.products:
			temp = [
				data.products[i][0] / data.products[i][3],
				data.products[i][1] / data.products[i][3],
				data.products[i][2] / data.products[i][3],
			]
			flag = True
			for j in range(3):
				if temp[j] < avg_by_products[j] and target[j]:
					flag = False
					break
			if flag:
				advices.append(i)
		shuffle(advices)
		advice = "\n".join(advices[:min(len(advices), 3)])

		self.advice_label.configure(text=advice)
		# plot.get_tk_widget().pack()
		# plt.show()

	def win_change(self):
		# for _ in self.main_win.winfo_children():
		# 	_.destroy()
		for _ in self.windows:
			# self.windows[_].grid_forget()
			self.windows[_].pack_forget()
		if self.selected_win.get() == "Main Page":
			self.windows["Main Page"].pack(in_=self.main_win, padx=10, pady=10)
		elif self.selected_win.get() == "Graphics":
			self.windows["Graphics"].pack(in_=self.main_win, padx=10, pady=10)
			self.statistics()
		elif self.selected_win.get() == "Settings":
			self.windows["Settings"].pack(in_=self.main_win, padx=10, pady=10)
		# print(f"win changed: {self.selected_win.get()}")
