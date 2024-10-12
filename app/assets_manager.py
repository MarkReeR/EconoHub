import json
import os
import customtkinter as ctk

ASSETS_FILE = './data/user_assets.json'

class AssetManager:
    def __init__(self, master):
        self.master = master
        self.assets = self.load_assets()
        
        self.header_frame()
        self.create_table()
        
    def header_frame(self):
        header_frame = ctk.CTkFrame(self.master, fg_color=self.master.cget("background_corner_colors"))
        header_frame.pack(pady=10, fill="x")

        assets_label = ctk.CTkLabel(header_frame, text="Управление активами", font=ctk.CTkFont(size=16, weight="bold"))
        assets_label.pack(side="top", padx=(10, 0))
        
        add_button = ctk.CTkButton(header_frame, text="+", command=self.add_asset, width=2)
        add_button.pack(side="right", padx=(20, 0))
        
        self.secid_input = ctk.CTkEntry(header_frame, width=100)
        self.secid_input.pack(side="right", padx=(10, 0))

        

    def create_table(self):
        self.table = ctk.CTkFrame(self.master)
        self.table.pack(fill="both", expand=True, pady=10)
        
        # Отображение активов в таблице
        for widget in self.table.winfo_children():
            widget.destroy()
        
        # Добавляем активы в таблицу
        for asset in self.assets["assets"]:
            label = ctk.CTkLabel(self.table, text=f'{asset["SECID"]} - {asset["quantity"]}')
            label.pack()

    def load_assets(self):
        """Загружает активы из файла."""
        if not os.path.exists(ASSETS_FILE):
            return {"assets": []}
        with open(ASSETS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_assets(self):
        """Сохраняет активы в файл."""
        with open(ASSETS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.assets, file, ensure_ascii=False, indent=4)

    def add_asset(self):
        """Добавляет новый актив."""
        secid = self.secid_input.get()  # Получаем значение из поля ввода
        quantity = 1  # Добавляем один экземпляр

        if secid and not any(asset["SECID"] == secid for asset in self.assets["assets"]):
            new_asset = {"SECID": secid, "quantity": quantity}
            self.assets["assets"].append(new_asset)
            self.save_assets()
            self.create_table()
            self.secid_input.delete(0, 'end')  # Очищаем поле ввода после добавления