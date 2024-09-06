import tkinter as tk
from tkinter import messagebox

# Ваши данные (примеры)
wallet_balance = {'RUB': 10000, 'USD': 150, 'EUR': 200}
exchange_rates = {'USD': 95.50, 'EUR': 105.75}

# Функция для конвертации валют
def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == to_currency:
        return amount
    elif from_currency == 'RUB':
        return amount / rates[to_currency]
    elif to_currency == 'RUB':
        return amount * rates[from_currency]
    else:
        return (amount / rates[to_currency]) * rates[from_currency]

# Функция для показа конвертированного значения
def show_conversion():
    amount = float(entry_amount.get())
    from_currency = var_from.get()
    to_currency = var_to.get()
    result = convert_currency(amount, from_currency, to_currency, exchange_rates)
    messagebox.showinfo("Конвертация", f"{amount} {from_currency} = {result:.2f} {to_currency}")

# Создание основного окна
root = tk.Tk()
root.title("Wallet App")

# Баланс
lbl_balance = tk.Label(root, text="Баланс")
lbl_balance.pack()

for currency, balance in wallet_balance.items():
    lbl = tk.Label(root, text=f"{currency}: {balance}")
    lbl.pack()

# Поле для ввода суммы
lbl_amount = tk.Label(root, text="Введите сумму:")
lbl_amount.pack()

entry_amount = tk.Entry(root)
entry_amount.pack()

# Выбор валюты для конвертации
var_from = tk.StringVar(root)
var_from.set("RUB")  # значение по умолчанию

var_to = tk.StringVar(root)
var_to.set("USD")  # значение по умолчанию

lbl_from = tk.Label(root, text="Из валюты:")
lbl_from.pack()

option_from = tk.OptionMenu(root, var_from, *wallet_balance.keys())
option_from.pack()

lbl_to = tk.Label(root, text="В валюту:")
lbl_to.pack()

option_to = tk.OptionMenu(root, var_to, *wallet_balance.keys())
option_to.pack()

# Кнопка для конвертации
btn_convert = tk.Button(root, text="Конвертировать", command=show_conversion)
btn_convert.pack()

# Запуск основного цикла приложения
root.mainloop()