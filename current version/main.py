import customtkinter as ctk
import csv
import json
from pathlib import Path

icon_path = Path(__file__).parent / "icon.ico"
app = ctk.CTk()
app.geometry("1280x720")
app.title("To Do List")
app.iconbitmap(icon_path)

works = []

class UI:
    def __init__(self):
        self.entry = ctk.CTkEntry(app, placeholder_text="Type your works...", width=250)
        self.priority = []
        self.scroll_frame = ctk.CTkScrollableFrame(app, width=330, height=320)

        self.count_item = 0
        self.button = ctk.CTkButton(
            master=app, text="Start", corner_radius=45, width=200, height=60, font=("Arial", 20),
            fg_color="#049EFD", hover_color="#0086C4", border_color="#07A1D4", border_width=2, command=self.hide_button
        )

        self.add_button = ctk.CTkButton(app,text="Add",command=self.add_item)

    def start_button(self):
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def hide_button(self):
        self.button.place_forget()
        self.entry.place(x=150, y=145)
        self.scroll_frame.place(x=150, y=185)
        self.add_button.place(x=420, y=145)

        self.entry.bind("<Return>", self.add_item)

    def delete_item(self, frame):
        frame.destroy()

    def add_item(self, event=None):
        text = self.entry.get().strip()

        if text == "":
            return

        works.append(text)

        item = ctk.CTkFrame(self.scroll_frame)
        item.pack(fill="x", pady=4, padx=2)

        label = ctk.CTkLabel(item, text=text, anchor="w")
        label.pack(side="left", padx=10, pady=5, expand=True, fill="x")

        delete_button = ctk.CTkButton(
            item, text="✕", width=28, height=28, fg_color="red", hover_color="darkred", command=lambda: self.delete_item(item)
        )
        delete_button.pack(side="right", padx=5, pady=5)

        self.entry.delete(0, "end")
        
        

        
        if self.count_item == 0:
            self.count_item += 1            
            self.finish_button = ctk.CTkButton(
                master=app, text="finish", corner_radius=12, width=60, height=40, font=("Arial", 20),
                fg_color="#2ED400", hover_color="#006605", border_color="#2ED400", border_width=2, command=self.finish_type
            )
            self.finish_button.place(relx=0.365, rely=0.76, anchor="center")
        
        
    def finish_type (self):
        self.entry.place_forget()
        self.scroll_frame.place_forget()
        self.add_button.place_forget()
        self.finish_button.place_forget()
        self.select_works()
        
    def select_works(self):
        self.combo_box = ctk.CTkComboBox(master=app,values=works,fg_color="#FFFFFF",border_color="#0962F1",
        dropdown_fg_color="#FCFEFF",dropdown_hover_color="#4CADFC",command=self.selected)
        self.combo_box.place(relx = 0.5 , rely = 0.2, anchor = "center")

        
    def selected(self , choice):
        self.priority.append(choice)
        works.remove(choice)
        if len(works) == 0 :
            self.combo_box.place_forget()
            return self.export()
        self.combo_box.destroy()
        self.select_works()

    def export(self) :
        self.export_as_json_button = ctk.CTkButton(
            master=app, text="Export json", corner_radius=45, width=200, height=60, font=("Arial", 20),
            fg_color="#8904FD", hover_color="#4F007D", border_color="#8904FD", border_width=2, command=self.export_json_button
        )
        self.export_as_json_button.place(relx=0.8, rely=0.4, anchor="center")
                
        self.export_as_csv_button = ctk.CTkButton(
            master=app, text="Export csv", corner_radius=45, width=200, height=60, font=("Arial", 20),
            fg_color="#00A205", hover_color="#00610A", border_color="#00A205", border_width=2, command=self.export_csv_button
        )
        self.export_as_csv_button.place(relx=0.8, rely=0.6, anchor="center")
        
        
    def export_json_button (self):
        with open("to do list.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            for i, item in enumerate(self.priority):
                writer.writerow([i+1, item])
                
    def export_csv_button (self):
        data = []

        for i, item in enumerate(self.priority):
            data.append({
                "id": i + 1,
                "task": item
            })

        with open("to_do_list.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


object_UI = UI()
object_UI.start_button()

app.mainloop()
