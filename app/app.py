import customtkinter as ctk

from scripts.load_currency_data import load_currency_data
from scripts.update_balance import update_balance


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("960x540")
        self.title("Econo hub")
        
        self.currency_data = load_currency_data()
        
        self.create_tabs()
        
    # меню навигации
    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self, width=800, height=600)
        self.tabview.pack(fill="both", expand=True)
        
        self.tabview.add("Главная")
        self.tabview.add("Активы")
        self.tabview.add("Дополнительно")
        
        self.setup_main_tab()
        self.setup_assets_tab()
        self.setup_additional_tab()
        
    def setup_main_tab(self):
        main_tab = self.tabview.tab("Главная")
        
        self.label_balance = ctk.CTkLabel(main_tab, text="$0", font=("Arial", 24))
        self.label_balance.pack(pady=20)
        
        usd_rate = self.currency_data["rates"]["USD"]["value"]
        eur_rate = self.currency_data["rates"]["EUR"]["value"]
        update_date = self.currency_data["date"]
        
        self.label_currency_info = ctk.CTkLabel(
            main_tab,
            text=f"Курс доллара США: {usd_rate} ₽\nКурс евро: {eur_rate} ₽",
            font=("Arial", 18),
            justify="left"
        )
        
        self.label_currency_info.pack(pady=10)
        
        self.label_update_date = ctk.CTkLabel(
            main_tab,
            text=f"Дата обновления: {update_date}",
            font=("Arial", 14),
            justify="left"
        )
        self.label_update_date.pack(pady=5)
        
        # Пример кнопки обновления баланса
        self.button_update = ctk.CTkButton(main_tab, text="O", command=self.update_balance)
        self.button_update.pack(pady=10)
        
    def setup_assets_tab(self):
        assets_tab = self.tabview.tab("Активы")
        
        # Заголовок таблицы
        header_frame = ctk.CTkFrame(assets_tab)
        header_frame.pack(pady=10, padx=20, fill="x")
        
        headers = ["Название", "Тип", "Количество", "Цена", "Стоимость"]
        for header in headers:
            label = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"))
            label.pack(side="left", padx=10)
        
        # Пример строки с активом
        asset_frame = ctk.CTkFrame(assets_tab)
        asset_frame.pack(pady=5, padx=20, fill="x")
        
        assets = ["Акция A", "Криптовалюта B", "Облигация C"]
        types = ["Акция", "Криптовалюта", "Облигация"]
        quantities = [10, 5, 20]
        prices = [100, 200, 50]
        
        for name, type_, qty, price in zip(assets, types, quantities, prices):
            asset_row = ctk.CTkFrame(assets_tab)
            asset_row.pack(pady=2, padx=20, fill="x")
            
            ctk.CTkLabel(asset_row, text=name).pack(side="left", padx=10)
            ctk.CTkLabel(asset_row, text=type_).pack(side="left", padx=10)
            ctk.CTkLabel(asset_row, text=str(qty)).pack(side="left", padx=10)
            ctk.CTkLabel(asset_row, text=f"${price}").pack(side="left", padx=10)
            ctk.CTkLabel(asset_row, text=f"${qty * price}").pack(side="left", padx=10)
        
    def setup_additional_tab(self):
        additional_tab = self.tabview.tab("Дополнительно")
        
        # Пример: график купонных выплат или другая аналитика
        self.label_additional = ctk.CTkLabel(additional_tab, text="Дополнительные функции будут здесь.", font=("Arial", 18))
        self.label_additional.pack(pady=20)
        
        # В будущем сюда можно добавить графики, отчёты и прочие аналитические инструменты
    
    def update_balance(self):
        update_balance(self.label_balance)

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()