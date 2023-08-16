import os
import tkinter as tk
import keyboard
import subprocess
import customtkinter as ctk

class SimpleNotepadApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Simple Notepad App")
        self.run_threads = True

        self.new_count = 1
        self.tabs = [] # Used to store the names of all open tabs for checking preventing duplicate tabs when renaming
        self.tab_data = {} # Used for storing the content of tabs

        self.tab_view = ctk.CTkTabview(master=self.root)
        self.tab_view.pack(side="top", fill="both", expand=True)  # Fill and expand

        self.setup_gui()
        self.root.geometry("800x600")  # Set an initial size
        self.root.mainloop()

    def setup_gui(self):

        self.text_editor_tab = self.tab_view.add(f"Unlisted-{self.new_count}")

        self.text_editor_frame = ctk.CTkFrame(master=self.text_editor_tab)
        self.text_editor_frame.pack(fill="both", expand=True)

        self.setup_text_editor_gui()

    def setup_text_editor_gui(self):

        def optionmenu_function(value):
            if value == "Exit":
                self.run_threads = False
                self.root.destroy()
            elif value == "Open":
                self.open_file()
            elif value == "Save":
                self.save_file()
            elif value == "New":
                self.new_tab()
            elif value == "Rename Tab":
                new_name = self.user_input()
                if new_name:
                    self.rename_tab(rename=new_name)
            elif value == "Close Tab":
                self.close_current_tab()

        top_frame = ctk.CTkFrame(master=self.text_editor_frame)
        top_frame.pack(side="top", fill="x")

        self.optionmenu = ctk.CTkOptionMenu(top_frame, values=["New", "Open", "Save", "Exit", "Rename Tab", "Close Tab"], command=optionmenu_function)
        self.optionmenu.pack(side="left", padx=10)
        self.optionmenu.set("File")

        self.back_home_button = tk.Button(top_frame, text="Home", command=self.back_to_launcher, bg="#66FF66", activebackground="#33CC33", width=125, height=2)
        self.back_home_button.pack(side="left", padx=10)

        self.text = ctk.CTkTextbox(self.text_editor_frame, wrap="word")
        self.text.pack(fill="both", expand=True)  # Fill and expand

        self.tabs.append(self.text_editor_tab)


        def update_text():
            self.tab_data[self.tab_view.get()] = self.text.get(1.0, ctk.END)
            self.auto_save()
            self.root.after(1000, update_text)
        update_text()

    def user_input(self):
        dialog = ctk.CTkInputDialog(text="Type the new name: ", title="Rename Tab")
        return dialog.get_input()

    def new_tab(self):
        self.new_count += 1

        new_tab = self.tab_view.add(f"Unlisted-{self.new_count}")

        def optionmenu_function(value):
            if value == "Exit":
                self.run_threads = False
                self.root.destroy()
            elif value == "Open":
                self.open_file()
            elif value == "Save":
                self.save_file()
            elif value == "New":
                self.new_tab()
            elif value == "Rename Tab":
                new_name = self.user_input()
                if new_name:
                    self.rename_tab(rename=new_name)
            elif value == "Close Tab":
                self.close_current_tab()

        new_tab_frame = ctk.CTkFrame(master=new_tab)
        new_tab_frame.pack(fill="both", expand=True)

        top_frame = ctk.CTkFrame(master=new_tab_frame)
        top_frame.pack(side="top", fill="x")

        optionmenu = ctk.CTkOptionMenu(top_frame, values=["New", "Open", "Save", "Exit", "Rename Tab", "Close Tab"], command=optionmenu_function)
        optionmenu.pack(side="left", padx=10)
        optionmenu.set("File")

        back_home_button = tk.Button(top_frame, text="Home", command=self.back_to_launcher, bg="#66FF66", activebackground="#33CC33", width=125, height=2)
        back_home_button.pack(side="left", padx=10)

        text = ctk.CTkTextbox(new_tab_frame, wrap="word")
        text.pack(fill="both", expand=True)  # Fill and expand

        self.tabs.append(new_tab)  # Store the tab object in self.tabs

        def update_text():
            self.tab_data[self.tab_view.get()] = text.get(1.0, ctk.END)
            self.auto_save(new_tab)
            self.root.after(1000, update_text)
        update_text()

    def close_current_tab(self):
        if tk.messagebox.askyesno("Confirmation", f"Are you sure you would like to close {self.tab_view.get()}"):
            tab = self.tab_view.get()
            self.tabs.remove(tab)
            self.tab_data.remove(tab)
            print(self.tab_data)
            self.tab_view.delete(tab)

    def create_new_tab(self, name, content):
        if name:
            if type(name) == str:
                new_tab = self.tab_view.add(name)
            else:
                self.new_count += 1
                new_tab = self.tab_view.add(f"Unlisted-{self.new_count}")
        else:
            self.new_count += 1
            new_tab = self.tab_view.add(f"Unlisted-{self.new_count}")

        def optionmenu_function(value):
            if value == "Exit":
                self.run_threads = False
                self.root.destroy()
            elif value == "Open":
                self.open_file()
            elif value == "Save":
                self.save_file()
            elif value == "New":
                self.new_tab()
            elif value == "Rename Tab":
                new_name = self.user_input()
                if new_name:
                    self.rename_tab(rename=new_name)
            elif value == "Close Tab":
                self.close_current_tab()

        new_tab_frame = ctk.CTkFrame(master=new_tab)
        new_tab_frame.pack(fill="both", expand=True)

        top_frame = ctk.CTkFrame(master=new_tab_frame)
        top_frame.pack(side="top", fill="x")

        optionmenu = ctk.CTkOptionMenu(top_frame, values=["New", "Open", "Save", "Exit", "Rename Tab", "Close Tab"], command=optionmenu_function)
        optionmenu.pack(side="left", padx=10)
        optionmenu.set("File")

        back_home_button = tk.Button(top_frame, text="Home", command=self.back_to_launcher, bg="#66FF66", activebackground="#33CC33", width=125, height=2)
        back_home_button.pack(side="left", padx=10)

        text = ctk.CTkTextbox(new_tab_frame, wrap="word")
        text.pack(fill="both", expand=True)  # Fill and expand
        text.insert(tk.END, content)  # Insert the content into the text box

        self.tabs.append(self.tab_view.get())

        def update_text():
            self.tab_data[self.tab_view.get()] = text.get(1.0, ctk.END)
            self.auto_save(new_tab)
            self.root.after(1000, update_text)
        update_text()

    def rename_tab(self, rename):
        # Get the currently selected tab
        selected_tab = self.tab_view.get()

        if not rename in self.tabs:
            # Delete the old tab
            self.tab_view.delete(selected_tab)

            # Call the function to create the new tab with content
            self.create_new_tab(rename, self.text.get(1.0, ctk.END))
        else:
            tk.messagebox.showerror(title="Rename Error", message="Their is already a tab named that")
      
    def open_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text.delete(1.0, ctk.END)
                self.text.insert(ctk.END, file.read())
                
    def save_file(self):
        file_path = ctk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get(1.0, ctk.END))
    
    def auto_save(self, given_tab):
        tab = given_tab
        print(f"Given tab: {tab}")
        if tab in self.tabs:
            print("Tab is in tab list")
            if tab == self.tab_view.get():
                print("Tab is current tab")
                tab_content = self.tab_data.get(tab)
                if tab_content != "\n":
                    print(f"Tab content: {self.tab_data.get(tab)}")
                    raw_tab_data = tab_content.replace("\n", r"\n")
                    print(raw_tab_data)
                    with open(f"{tab}.txt", "w") as file:
                        file.write(raw_tab_data)
                        print("\n")
        self.root.after(1000, self.auto_save, given_tab)

    def back_to_launcher(self):
        self.root.destroy()
        subprocess.Popen(["python", "UltimatepythonGUI.py"])

    def on_closing(self):
        self.run_threads = False
        self.root.destroy()

if __name__ == "__main__":
    app = SimpleNotepadApp()
