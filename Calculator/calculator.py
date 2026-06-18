import customtkinter as ctk
import re
import os
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(SCRIPT_DIR, "history.json")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("380x600+700+100")
        self.resizable(False, False)
        self.expression = ""
        self.current_input = "0"
        self.last_result = None
        self.is_showing_result = False
        self.history = []
        self.load_history_from_file()
        self.history_visible = False

        self.colors = {
            "bg_dark": "#121214",
            "bg_light": "#F8F9FA",
            "display_bg_dark": "#1A1A1E",
            "display_bg_light": "#FFFFFF",
            "btn_num_dark": "#23232A",
            "btn_num_light": "#E9ECEF",
            "btn_num_hover_dark": "#2E2E38",
            "btn_num_hover_light": "#DEE2E6",
            "btn_num_text_dark": "#E2E2E2",
            "btn_num_text_light": "#212529",
            "btn_op_dark": "#7C4DFF",
            "btn_op_light": "#6200EE",
            "btn_op_hover_dark": "#9E7BFF",
            "btn_op_hover_light": "#7722FF",
            "btn_op_text": "#FFFFFF",
            "btn_util_dark": "#323545",
            "btn_util_light": "#CED4DA",
            "btn_util_hover_dark": "#43485E",
            "btn_util_hover_light": "#ADB5BD",
            "btn_util_text_dark": "#CFD2DC",
            "btn_util_text_light": "#495057",
            "btn_eq_dark": "#00E676",
            "btn_eq_light": "#00C853",
            "btn_eq_hover_dark": "#33F090",
            "btn_eq_hover_light": "#00E676",
            "btn_eq_text_dark": "#121214",
            "btn_eq_text_light": "#FFFFFF",
            "history_bg_dark": "#1A1A1E",
            "history_bg_light": "#FFFFFF"
        }

        self.update_theme_colors()


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌙 Dark",
            width=90,
            height=32,
            corner_radius=16,
            font=("Segoe UI", 12, "bold"),
            command=self.toggle_theme,
            fg_color=self.colors["btn_util_dark"],
            text_color=self.colors["btn_util_text_dark"],
            hover_color=self.colors["btn_util_hover_dark"]
        )
        self.theme_btn.grid(row=0, column=0, sticky="w")


        self.history_btn = ctk.CTkButton(
            self.header_frame,
            text="🕒 History",
            width=90,
            height=32,
            corner_radius=16,
            font=("Segoe UI", 12, "bold"),
            command=self.toggle_history_panel,
            fg_color=self.colors["btn_util_dark"],
            text_color=self.colors["btn_util_text_dark"],
            hover_color=self.colors["btn_util_hover_dark"]
        )
        self.history_btn.grid(row=0, column=2, sticky="e")


        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.calc_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
        self.calc_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.calc_frame.grid_rowconfigure(1, weight=1)
        self.calc_frame.grid_columnconfigure(0, weight=1)

        self.display_frame = ctk.CTkFrame(
            self.calc_frame, 
            height=130, 
            corner_radius=20, 
            fg_color=self.colors["display_bg_dark"]
        )
        self.display_frame.grid(row=0, column=0, sticky="new", pady=(0, 15))
        self.display_frame.grid_propagate(False)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(1, weight=1)


        self.formula_label = ctk.CTkLabel(
            self.display_frame,
            text="",
            font=("Segoe UI", 14),
            text_color="#888888",
            anchor="e"
        )
        self.formula_label.grid(row=0, column=0, sticky="sew", padx=20, pady=(15, 2))


        self.display_label = ctk.CTkLabel(
            self.display_frame,
            text="0",
            font=("Segoe UI", 36, "bold"),
            text_color="#FFFFFF",
            anchor="e"
        )
        self.display_label.grid(row=1, column=0, sticky="new", padx=20, pady=(2, 15))


        self.keypad_frame = ctk.CTkFrame(self.calc_frame, fg_color="transparent")
        self.keypad_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(5):
            self.keypad_frame.grid_rowconfigure(i, weight=1, uniform="equal")
        for j in range(4):
            self.keypad_frame.grid_columnconfigure(j, weight=1, uniform="equal")


        buttons = [
            ("C", 0, 0, "util"), ("±", 0, 1, "util"), ("%", 0, 2, "util"), ("÷", 0, 3, "op"),
            ("7", 1, 0, "num"),  ("8", 1, 1, "num"),  ("9", 1, 2, "num"),  ("×", 1, 3, "op"),
            ("4", 2, 0, "num"),  ("5", 2, 1, "num"),  ("6", 2, 2, "num"),  ("-", 2, 3, "op"),
            ("1", 3, 0, "num"),  ("2", 3, 1, "num"),  ("3", 3, 2, "num"),  ("+", 3, 3, "op"),
            ("0", 4, 0, "num"),  (".", 4, 1, "num"),  ("⌫", 4, 2, "util"), ("=", 4, 3, "eq")
        ]


        self.btn_objects = {}
        for text, r, c, b_type in buttons:
            btn = ctk.CTkButton(
                self.keypad_frame,
                text=text,
                font=("Segoe UI", 18, "bold" if b_type != "num" else "normal"),
                corner_radius=18,
                command=lambda val=text, t=b_type: self.on_button_press(val, t)
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            self.btn_objects[text] = (btn, b_type)


        self.history_panel = ctk.CTkFrame(self.content_frame, width=280, corner_radius=20, fg_color=self.colors["history_bg_dark"])
        self.history_panel.grid_propagate(False)
        self.history_panel.grid_columnconfigure(0, weight=1)
        self.history_panel.grid_rowconfigure(1, weight=1)


        self.history_header = ctk.CTkLabel(
            self.history_panel,
            text="Calculation History",
            font=("Segoe UI", 16, "bold"),
            text_color="#FFFFFF"
        )
        self.history_header.grid(row=0, column=0, sticky="w", padx=15, pady=15)


        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_panel,
            fg_color="transparent"
        )
        self.history_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))


        self.clear_history_btn = ctk.CTkButton(
            self.history_panel,
            text="Clear History",
            height=35,
            corner_radius=12,
            font=("Segoe UI", 12, "bold"),
            fg_color="transparent",
            border_width=1,
            border_color=self.colors["btn_util_dark"],
            command=self.clear_history
        )
        self.clear_history_btn.grid(row=2, column=0, sticky="ew", padx=15, pady=15)


        self.update_widget_styles()

        self.bind("<Key>", self.on_key_press)
        self.focus_set()


    def load_history_from_file(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []


    def save_history_to_file(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4)
        except Exception:
            pass

    def update_theme_colors(self):
        mode = ctk.get_appearance_mode().lower()
        if mode == "dark":
            self.configure(fg_color=self.colors["bg_dark"])
        else:
            self.configure(fg_color=self.colors["bg_light"])

    def update_widget_styles(self):
        mode = ctk.get_appearance_mode().lower()
        is_dark = mode == "dark"

        if is_dark:
            self.theme_btn.configure(
                text="☀️ Light",
                fg_color=self.colors["btn_util_dark"],
                text_color=self.colors["btn_util_text_dark"],
                hover_color=self.colors["btn_util_hover_dark"]
            )
            self.history_btn.configure(
                fg_color=self.colors["btn_util_dark"],
                text_color=self.colors["btn_util_text_dark"],
                hover_color=self.colors["btn_util_hover_dark"]
            )
            self.display_frame.configure(fg_color=self.colors["display_bg_dark"])
            self.display_label.configure(text_color="#FFFFFF")
            self.formula_label.configure(text_color="#888888")
            self.history_panel.configure(fg_color=self.colors["history_bg_dark"])
            self.history_scroll.configure(fg_color=self.colors["history_bg_dark"])
            self.history_header.configure(text_color="#FFFFFF")
            self.clear_history_btn.configure(
                border_color=self.colors["btn_util_dark"],
                text_color="#FFFFFF",
                hover_color=self.colors["btn_util_dark"]
            )
        else:
            self.theme_btn.configure(
                text="🌙 Dark",
                fg_color=self.colors["btn_util_light"],
                text_color=self.colors["btn_util_text_light"],
                hover_color=self.colors["btn_util_hover_light"]
            )
            self.history_btn.configure(
                fg_color=self.colors["btn_util_light"],
                text_color=self.colors["btn_util_text_light"],
                hover_color=self.colors["btn_util_hover_light"]
            )
            self.display_frame.configure(fg_color=self.colors["display_bg_light"])
            self.display_label.configure(text_color="#212529")
            self.formula_label.configure(text_color="#6C757D")
            self.history_panel.configure(fg_color=self.colors["history_bg_light"])
            self.history_scroll.configure(fg_color=self.colors["history_bg_light"])
            self.history_header.configure(text_color="#212529")
            self.clear_history_btn.configure(
                border_color=self.colors["btn_util_light"],
                text_color="#212529",
                hover_color=self.colors["btn_util_light"]
            )

        for text, (btn, b_type) in self.btn_objects.items():
            if b_type == "num":
                btn.configure(
                    fg_color=self.colors["btn_num_dark"] if is_dark else self.colors["btn_num_light"],
                    text_color=self.colors["btn_num_text_dark"] if is_dark else self.colors["btn_num_text_light"],
                    hover_color=self.colors["btn_num_hover_dark"] if is_dark else self.colors["btn_num_hover_light"]
                )
            elif b_type == "op":
                btn.configure(
                    fg_color=self.colors["btn_op_dark"] if is_dark else self.colors["btn_op_light"],
                    text_color=self.colors["btn_op_text"],
                    hover_color=self.colors["btn_op_hover_dark"] if is_dark else self.colors["btn_op_hover_light"]
                )
            elif b_type == "util":
                btn.configure(
                    fg_color=self.colors["btn_util_dark"] if is_dark else self.colors["btn_util_light"],
                    text_color=self.colors["btn_util_text_dark"] if is_dark else self.colors["btn_util_text_light"],
                    hover_color=self.colors["btn_util_hover_dark"] if is_dark else self.colors["btn_util_hover_light"]
                )
            elif b_type == "eq":
                btn.configure(
                    fg_color=self.colors["btn_eq_dark"] if is_dark else self.colors["btn_eq_light"],
                    text_color=self.colors["btn_eq_text_dark"] if is_dark else self.colors["btn_eq_text_light"],
                    hover_color=self.colors["btn_eq_hover_dark"] if is_dark else self.colors["btn_eq_hover_light"]
                )


        self.refresh_history_ui()



    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode().lower()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
        self.after(50, lambda: [self.update_theme_colors(), self.update_widget_styles()])



    def toggle_history_panel(self):
        if self.history_visible:
            self.history_panel.grid_forget()
            self.geometry("380x600")
            self.history_visible = False
        else:
            self.history_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=(0, 15))
            self.geometry("680x600")
            self.history_visible = True
            self.refresh_history_ui()


    def on_button_press(self, val, btn_type):
        if btn_type == "num":
            self.handle_number(val)
        elif btn_type == "op":
            self.handle_operator(val)
        elif btn_type == "util":
            if val == "C":
                self.clear_all()
            elif val == "±":
                self.toggle_sign()
            elif val == "%":
                self.apply_percentage()
            elif val == "⌫":
                self.backspace()
        elif btn_type == "eq":
            self.calculate_result()


    def handle_number(self, num):
        if self.is_showing_result:
            self.current_input = "0"
            self.is_showing_result = False

        if num == ".":
            if "." not in self.current_input:
                self.current_input += "."
        else:
            if self.current_input == "0":
                self.current_input = num
            else:
                self.current_input += num

        self.update_display()


    def handle_operator(self, op):
        if self.is_showing_result:
            self.expression = self.current_input + " " + op + " "
            self.is_showing_result = False
            self.current_input = "0"
        else:
            if self.current_input != "0" or (self.current_input == "0" and not self.expression):
                self.expression += self.current_input + " " + op + " "
                self.current_input = "0"
            elif self.expression:
                self.expression = self.expression.strip().rsplit(" ", 1)[0] + " " + op + " "

        self.update_display()

    def clear_all(self):
        self.expression = ""
        self.current_input = "0"
        self.is_showing_result = False
        self.update_display()


    def backspace(self):
        if self.is_showing_result:
            self.expression = ""
            self.is_showing_result = False
            return

        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()


    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display()


    def apply_percentage(self):
        try:
            val = float(self.current_input)
            val = val / 100.0
            if val.is_integer():
                self.current_input = str(int(val))
            else:
                self.current_input = f"{val:.6f}".rstrip('0').rstrip('.')
            self.update_display()
        except ValueError:
            pass


    def calculate_result(self):
        if not self.expression and not self.is_showing_result:
            return

        full_formula = self.expression + self.current_input
        
        eval_formula = full_formula.replace("×", "*").replace("÷", "/")
        
        if not re.match(r'^[\d\s.+\-*/()]+$', eval_formula):
            self.display_error("Error")
            return

        try:
            result = eval(eval_formula)

            if isinstance(result, float):
                if result.is_integer():
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.10f}".rstrip('0').rstrip('.')
            else:
                result_str = str(result)

            self.history.append([full_formula, result_str])
            self.save_history_to_file()
            
            self.formula_label.configure(text=full_formula + " =")
            self.display_label.configure(text=result_str)
            
            self.current_input = result_str
            self.expression = ""
            self.is_showing_result = True
            
            if self.history_visible:
                self.refresh_history_ui()

        except ZeroDivisionError:
            self.display_error("Zero Division")
        except Exception:
            self.display_error("Error")


    def display_error(self, err_msg):
        self.formula_label.configure(text="")
        self.display_label.configure(text=err_msg)
        self.current_input = "0"
        self.expression = ""
        self.is_showing_result = True


    def update_display(self):
        self.formula_label.configure(text=self.expression)
        
        display_val = self.current_input
        if display_val not in ["-", "Error", "Zero Division"]:
            try:
                if "." not in display_val:
                    display_val = f"{int(display_val):,}"
                else:
                    parts = display_val.split(".")
                    if len(parts) == 2:
                        integer_part = f"{int(parts[0]):,}"
                        display_val = integer_part + "." + parts[1]
            except ValueError:
                pass
                
        self.display_label.configure(text=display_val)


    def on_key_press(self, event):
        char = event.char
        keysym = event.keysym

        if char in "0123456789.":
            self.handle_number(char)
        elif char in "+-*/":
            op_map = {"+": "+", "-": "-", "*": "×", "/": "÷"}
            self.handle_operator(op_map[char])
        elif keysym in ["Return", "KP_Enter"]:
            self.calculate_result()
        elif keysym == "BackSpace":
            self.backspace()
        elif keysym == "Escape":
            self.clear_all()
        elif char == "%":
            self.apply_percentage()


    def refresh_history_ui(self):
        for child in self.history_scroll.winfo_children():
            child.destroy()

        if not self.history:
            empty_lbl = ctk.CTkLabel(
                self.history_scroll,
                text="No history yet",
                font=("Segoe UI", 12, "italic"),
                text_color="#888888"
            )
            empty_lbl.pack(pady=40)
            return

        is_dark = ctk.get_appearance_mode().lower() == "dark"
        item_hover = "#2A2B36" if is_dark else "#E9ECEF"
        item_fg = "#23232A" if is_dark else "#F1F3F5"
        text_color_expr = "#A0A0A0" if is_dark else "#6C757D"
        text_color_res = "#FFFFFF" if is_dark else "#212529"


        for formula, result in reversed(self.history):
            item_frame = ctk.CTkFrame(
                self.history_scroll,
                height=65,
                corner_radius=10,
                fg_color=item_fg
            )
            item_frame.pack(fill="x", pady=4, padx=5)
            item_frame.pack_propagate(False)
            
            click_cmd = lambda f=formula, r=result: self.load_history_item(f, r)
            
            def on_enter(e, f=item_frame):
                f.configure(fg_color=item_hover)
            def on_leave(e, f=item_frame, original=item_fg):
                f.configure(fg_color=original)
                
            item_frame.bind("<Enter>", on_enter)
            item_frame.bind("<Leave>", on_leave)
            item_frame.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())


            lbl_expr = ctk.CTkLabel(
                item_frame,
                text=formula,
                font=("Segoe UI", 11),
                text_color=text_color_expr,
                anchor="e"
            )
            lbl_expr.pack(fill="x", padx=10, pady=(6, 0))
            lbl_expr.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())
            lbl_expr.bind("<Enter>", on_enter)
            lbl_expr.bind("<Leave>", on_leave)


            lbl_res = ctk.CTkLabel(
                item_frame,
                text="= " + result,
                font=("Segoe UI", 14, "bold"),
                text_color=text_color_res,
                anchor="e"
            )
            lbl_res.pack(fill="x", padx=10, pady=(0, 6))
            lbl_res.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())
            lbl_res.bind("<Enter>", on_enter)
            lbl_res.bind("<Leave>", on_leave)


    def load_history_item(self, formula, result):
        self.expression = ""
        self.current_input = result
        self.is_showing_result = True
        self.update_display()
        self.formula_label.configure(text=f"Loaded: {formula}")


    def clear_history(self):
        self.history.clear()
        if os.path.exists(HISTORY_FILE):
            try:
                os.remove(HISTORY_FILE)
            except Exception:
                pass
        self.refresh_history_ui()


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()