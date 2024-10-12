import customtkinter as ctk

from scripts.load_currency_data import get_currency_value, get_currency_data
from scripts.update_balance import update_balance
from app.assets_manager import AssetManager



class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("450x540")
        self.title("Econo hub")
        
        self.create_tabs()
        
    # меню навигации
    def create_tabs(self):
        tabs_frame = ctk.CTkFrame(self)
        tabs_frame.pack(side="top", fill="x")
        
        self.tabview = ctk.CTkTabview(tabs_frame)
        self.tabview.pack(fill="x", padx=10, pady=10)
        
        self.tabview.add("Главная")
        self.tabview.add("Активы")
        # self.tabview.add("Дополнительно")
        
        self.setup_main_tab()
        self.setup_assets_tab()
        # self.setup_additional_tab()

        
    def setup_main_tab(self):
        main_tab = self.tabview.tab("Главная")
        
        self.label_balance = ctk.CTkLabel(main_tab, text="0₽", font=("Arial", 24))
        self.label_balance.pack(pady=20)
        
        usd_rate = get_currency_value("USD")
        eur_rate = get_currency_value("EUR")
        
        self.label_currency_info = ctk.CTkLabel(
            main_tab,
            text=f"$: {usd_rate} ₽\t€: {eur_rate} ₽",
            font=("Arial", 18),
            justify="left"
        )
        self.label_currency_info.pack(pady=10)
        
        self.label_update_date = ctk.CTkLabel(
            main_tab,
            text=f"Дата обновления: {get_currency_data()}",
            font=("Arial", 12),
            justify="left"
        )
        self.label_update_date.pack(pady=5)
        
        #Кнопка обновления не робит
        self.button_update = ctk.CTkButton(main_tab, text="Обновить", command=update_balance(self))
        self.button_update.pack(pady=10)
        
    def setup_assets_tab(self):
        assets_tab = self.tabview.tab("Активы")
        asset_manager = AssetManager(assets_tab)
        
    # def setup_additional_tab(self):
    #     additional_tab = self.tabview.tab("Дополнительно")
        
    #     # Пример: график купонных выплат или другая аналитика
    #     self.label_additional = ctk.CTkLabel(additional_tab, text="Дополнительные функции будут здесь.", font=("Arial", 18))
    #     self.label_additional.pack(pady=20)
        
    #     # В будущем сюда можно добавить графики, отчёты и прочие аналитические инструменты
    
    def update_balance(self):
        update_balance(self.label_balance)

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()