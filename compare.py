# Note customtkinter has dependency on tkinter which can't be installed using
# pip but can be installed using `brew install python-tk`
# (tkinter is supposed to be part of Python standard library but some
# installs miss it out. Homebrew is guilty of this.)

import time
import json
import os
import webbrowser
import customtkinter
import difflib

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Comparison")
        self.geometry("340x274")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.fields = {}
        self.last_used_values = []

        # Heading
        title_label = customtkinter.CTkLabel(self, text="Choose Wisely")
        title_label.grid(sticky="new")  # new - north, east, west

        # Fields for selecting two files for comparing and report file for saving
        self.files_frame = customtkinter.CTkFrame(self)
        self.files_frame.grid(padx=4, sticky="ew")
        items = [
            {"type": "heading", "text": "🗂️ Files to Compare"},
            {"type": "filepick", "text": "First", "default": ""},
            {"type": "filepick", "text": "Second", "default": ""},
            {"type": "heading", "text": "📝 Results"},
            {"type": "filepick", "text": "Report", "default": "report.html"}
        ]
        self.add_file_items(items, self.files_frame)

        # Message text - used to disply outcome of button press
        self.message_frame = customtkinter.CTkFrame(self)
        self.message_frame.grid(pady=(4, 0))
        self.message = customtkinter.CTkLabel(self.message_frame, text="Nothing yet", text_color="blue")
        self.message.grid(padx=4)

        # Action button and view button
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(padx=4, pady=(4, 4), sticky="ew")

        self.button = customtkinter.CTkButton(self.button_frame, text="Do Thing!", width=280, command=self.button_callback)
        self.view_button = customtkinter.CTkButton(self.button_frame, text="👁️", width=16, command=self.view_html_file)
        self.button.grid(row=0, column=0, padx=(4, 4), pady=(4, 4), sticky="w")
        self.view_button.grid(row=0, column=1, padx=(4, 4), pady=(4, 4), sticky="w")

        # Load config from json file
        self.import_fields()

    def add_file_items(self, items, parent):
        for row, item in enumerate(items):
            if item["type"] == "heading":
                heading = customtkinter.CTkLabel(parent,
                                                 text=item.get("text"),
                                                 fg_color="transparent")
                heading.grid(row=row, padx=10, columnspan=3, sticky="w")
            if item["type"] == "filepick":
                fieldname = item.get("text")
                label = customtkinter.CTkLabel(parent,
                                               text=fieldname,
                                               fg_color="transparent")
                entry = customtkinter.CTkEntry(parent,
                                               width=200,
                                               placeholder_text="Hmm?")
                if item.get("default"):
                    entry.delete(0, customtkinter.END)
                    entry.insert(0, item["default"])

                # Need to use lambda to be able to pass argument to the callback method
                fs_button = customtkinter.CTkButton(parent, text="💾", width=12,
                                                    command=lambda x=fieldname: self.select_file(x))
                self.fields[fieldname] = entry
                label.grid(row=row, column=0, padx=10, pady=(4, 4), sticky="w")
                entry.grid(row=row, column=1, padx=10, pady=(4, 4), sticky="w")
                fs_button.grid(row=row, column=2, padx=10, pady=(4, 4), sticky="w")

    def select_file(self, field_name: str):
        filename = customtkinter.filedialog.askopenfilename()
        field = self.fields[field_name]
        field.delete(0, customtkinter.END)
        field.insert(0, filename)
        # Causes view to scroll to end of the text
        field.xview_moveto(1.0)

    def button_callback(self):
        try:
            file1 = self.fields["First"].get()
            file2 = self.fields["Second"].get()
            report_filename = self.fields["Report"].get()
            filename = file_compare(file1, file2, report_filename)
            now = time.strftime(' %H:%M:%S, %d/%m/%Y')
            self.message.configure(text=f"Saved report '{filename}': {now}", text_color="green")
        except Exception as err:
            print(f"Problem when button pressed: {err}")
            self.message.configure(text=f"Silly!\n{err}", text_color="red")

        # Export file details to json if we have new values
        current_values = [file1, file2, report_filename]
        if current_values != self.last_used_values:
            self.last_used_values = current_values
            self.export_fields()

    def export_fields(self):
        field_values = {k: v.get() for k, v in self.fields.items()}
        json_export(field_values)

    def import_fields(self):
        try:
            field_values = json_import()
        except FileNotFoundError:
            return
        for key, value in field_values.items():
            field = self.fields.get(key)
            field.delete(0, customtkinter.END)
            field.insert(0, value)
            field.xview_moveto(1.0)

    def view_html_file(self):
        filename = self.fields["Report"].get()
        file_path = os.path.join(os.getcwd(), filename)
        webbrowser.open(f'file://{file_path}')


def file_compare(file1: str, file2: str, report_filename: str = "report.html") -> str:
    with open(file1, "r") as f1, open(file2, "r") as f2:
        html_diff = difflib.HtmlDiff().make_file(f1.readlines(), f2.readlines())
    with open(report_filename, "w") as outfile:
        outfile.write(html_diff)
    return report_filename


def json_export(content, filename="settings.json"):
    json_str = json.dumps(content)
    with open(filename, "w") as outfile:
        outfile.write(json_str)


def json_import(filename="settings.json"):
    with open(filename, "r") as infile:
        data = json.load(infile)
    return data


app = App()
app.mainloop()
