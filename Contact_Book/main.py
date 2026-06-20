import json
import os
import re
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk


class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Contact Book")
        self.geometry("1000x700+300+40")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=("#F5F7FB", "#000000"))

        self.contacts_file = "contact.json"
        self.contacts = []
        self.selected_contact = None
        self.load_contacts()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=5)
        self.create_left_panel()
        self.create_right_panel()
        self.refresh_contact_list()
        self.focus()


    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, "r", encoding="utf-8") as file:
                    self.contacts = json.load(file)
            except Exception:
                self.contacts = []
        else:
            self.contacts = []


    def save_contacts(self):
        try:
            with open(self.contacts_file, "w", encoding="utf-8") as file:
                json.dump(self.contacts, file, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {e}")

    def set_fields_state(self, state):
        self.name_entry.configure(state=state)
        self.phone_entry.configure(state=state)
        self.email_entry.configure(state=state)
        self.address_entry.configure(state=state)

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="🌙")

    def create_left_panel(self):
        self.left_panel = ctk.CTkFrame(
            self, 
            corner_radius=16,
            fg_color=("#FFFFFF", "#121212"),
            border_width=1,
            border_color=("#E5E7EB", "#262626")
        )
        self.left_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=25)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="👤 Contact Details", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color=("#111827", "#FFFFFF")
        )
        title_label.pack(side="left")
        
        self.theme_btn = ctk.CTkButton(
            header_frame,
            text="🌙",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=("#ECECEC", "#2A2A2A"),
            text_color=("#333333", "#FFFFFF"),
            hover_color=("#D1D1D1", "#3A3A3A"),
            font=ctk.CTkFont(size=14),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right")
        
        divider = ctk.CTkFrame(self.left_panel, height=2, fg_color=("#E5E7EB", "#262626"))
        divider.pack(fill="x", padx=25, pady=(0, 15))
        
        def create_input_field(parent, label_text, placeholder):
            label = ctk.CTkLabel(
                parent, 
                text=label_text, 
                font=ctk.CTkFont(family="Helvetica", size=13, weight="bold"),
                text_color=("#374151", "#9CA3AF")
            )
            label.pack(anchor="w", padx=25, pady=(8, 2))
            
            entry = ctk.CTkEntry(
                parent, 
                placeholder_text=placeholder, 
                height=38,
                corner_radius=8,
                border_width=1,
                border_color=("#D1D5DB", "#262626"),
                fg_color=("#F9FAFB", "#1C1C1C"),
                text_color=("#111827", "#FFFFFF")
            )
            entry.pack(fill="x", padx=25, pady=(0, 10))
            return entry
            
        self.name_entry = create_input_field(self.left_panel, "Name *", "e.g. Piyush Barod")
        self.phone_entry = create_input_field(self.left_panel, "Phone Number *", "e.g. +91 1234567890")
        self.email_entry = create_input_field(self.left_panel, "Email Address", "e.g. piyush@example.com")
        self.address_entry = create_input_field(self.left_panel, "Address", "e.g. Ujjain, Madhya Pradesh, India")
        
        btn_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(15, 10))
        
        self.save_btn = ctk.CTkButton(
            btn_frame, 
            text="Save Contact", 
            fg_color="#10B981", 
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            command=self.save_contact
        )
        self.save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            btn_frame, 
            text="Clear", 
            fg_color="#6B7280", 
            hover_color="#4B5563",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8,
            command=self.clear_form
        )
        clear_btn.pack(side="right", fill="x", expand=True)

    def create_right_panel(self):
        self.right_panel = ctk.CTkFrame(
            self, 
            corner_radius=16,
            fg_color=("#FFFFFF", "#121212"),
            border_width=1,
            border_color=("#E5E7EB", "#262626")
        )
        self.right_panel.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        right_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        right_header.pack(fill="x", pady=(20, 10), padx=25)
        
        right_title = ctk.CTkLabel(
            right_header,
            text="🗂️ Contacts Directory",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color=("#111827", "#FFFFFF")
        )
        right_title.pack(anchor="w")
        
        divider = ctk.CTkFrame(self.right_panel, height=2, fg_color=("#E5E7EB", "#262626"))
        divider.pack(fill="x", padx=25, pady=(0, 15))
        
        search_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        search_frame.pack(fill="x", padx=25, pady=(0, 15))
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="🔍 Search contacts by name or phone...", 
            height=42,
            corner_radius=8,
            border_width=1,
            border_color=("#D1D5DB", "#262626"),
            fg_color=("#F9FAFB", "#1C1C1C"),
            text_color=("#111827", "#FFFFFF"),
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_contacts)
        
        self.list_frame = ctk.CTkScrollableFrame(
            self.right_panel, 
            corner_radius=12,
            fg_color=("#F8FAFC", "#000000"),
            border_width=1,
            border_color=("#E5E7EB", "#262626")
        )
        self.list_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    def refresh_contact_list(self, query=""):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        query = query.strip().lower()
        filtered_contacts = []
        for c in self.contacts:
            name = c.get("name", "").lower()
            phone = c.get("phone", "").lower()
            if query in name or query in phone:
                filtered_contacts.append(c)
                
        if not filtered_contacts:
            msg = "No contacts found." if query else "Contact directory is empty.\nFill the form to add a contact!"
            no_contacts_label = ctk.CTkLabel(
                self.list_frame, 
                text=msg, 
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color="gray"
            )
            no_contacts_label.pack(pady=40)
            return
            
        for contact in filtered_contacts:
            self.create_contact_row(contact)

    def filter_contacts(self, event):
        query = self.search_entry.get()
        self.refresh_contact_list(query)

    def create_contact_row(self, contact):
        row_card = ctk.CTkFrame(
            self.list_frame, 
            corner_radius=10, 
            height=64, 
            fg_color=("#FFFFFF", "#121212"),
            border_width=1,
            border_color=("#E5E7EB", "#262626")
        )
        row_card.pack(fill="x", pady=6, padx=8)
        row_card.pack_propagate(False)
        row_card.configure(cursor="hand2")
        
        def on_click(event):
            self.select_contact(contact)
            
        row_card.bind("<Button-1>", on_click)
        
        def on_enter(event):
            row_card.configure(fg_color=("#F3F4F6", "#1C1C1C"))
        def on_leave(event):
            row_card.configure(fg_color=("#FFFFFF", "#121212"))
            
        row_card.bind("<Enter>", on_enter)
        row_card.bind("<Leave>", on_leave)
        
        text_frame = ctk.CTkFrame(row_card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(16, 8), pady=8)
        text_frame.bind("<Button-1>", on_click)
        text_frame.bind("<Enter>", on_enter)
        text_frame.bind("<Leave>", on_leave)
        
        name_label = ctk.CTkLabel(
            text_frame, 
            text=contact.get("name", ""), 
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=("#111827", "#FFFFFF"),
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(2, 0))
        name_label.bind("<Button-1>", on_click)
        name_label.bind("<Enter>", on_enter)
        name_label.bind("<Leave>", on_leave)
        name_label.configure(cursor="hand2")
        
        phone_label = ctk.CTkLabel(
            text_frame, 
            text=contact.get("phone", ""), 
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=("#6B7280", "#A3A3A3"),
            anchor="w"
        )
        phone_label.pack(anchor="w")
        phone_label.bind("<Button-1>", on_click)
        phone_label.bind("<Enter>", on_enter)
        phone_label.bind("<Leave>", on_leave)
        phone_label.configure(cursor="hand2")
        
        delete_btn = ctk.CTkButton(
            row_card, 
            text="🗑", 
            width=36, 
            height=36, 
            corner_radius=18,
            fg_color="#EF4444", 
            hover_color="#DC2626",
            font=ctk.CTkFont(size=15),
            command=lambda: self.delete_contact(contact)
        )
        delete_btn.pack(side="right", padx=15, pady=14)

    def select_contact(self, contact):
        self.selected_contact = contact
        
        self.set_fields_state("normal")
        
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, contact.get("name", ""))
        
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, contact.get("phone", ""))
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, contact.get("email", ""))
        
        self.address_entry.delete(0, "end")
        self.address_entry.insert(0, contact.get("address", ""))
        
        self.set_fields_state("readonly")
        
        self.save_btn.configure(text="Edit Contact", fg_color="#3B82F6", hover_color="#2563EB")
        
        self.focus()

    def clear_form(self):
        self.selected_contact = None
        
        self.set_fields_state("normal")
        
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        
        self.save_btn.configure(text="Save Contact", fg_color="#10B981", hover_color="#059669")
        
        self.focus()

    def delete_contact(self, contact):
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete {contact.get('name')}?"
        )
        if confirm:
            self.contacts.remove(contact)
            self.save_contacts()
            self.refresh_contact_list(self.search_entry.get())
            
            if self.selected_contact == contact:
                self.clear_form()

    def save_contact(self):
        if self.save_btn.cget("text") == "Edit Contact":
            self.set_fields_state("normal")
            self.save_btn.configure(text="Update Contact", fg_color="#10B981", hover_color="#059669")
            self.name_entry.focus()
            return
            
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Validation Error", "Name field cannot be empty.")
            return
        if not phone:
            messagebox.showwarning("Validation Error", "Phone number cannot be empty.")
            return
            
        clean_phone = phone.replace(" ", "").replace("-", "")
        if clean_phone.startswith("+"):
            clean_phone = clean_phone[1:]
        if not clean_phone.isdigit() or not (10 <= len(clean_phone) <= 15):
            messagebox.showwarning(
                "Validation Error", 
                "Please enter a valid phone number (10 to 15 digits)."
            )
            return
            
        if email:
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                messagebox.showwarning("Validation Error", "Please enter a valid email address.")
                return
                
        if self.selected_contact is None:
            new_contact = {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            }
            self.contacts.insert(0, new_contact)
        else:
            if self.selected_contact in self.contacts:
                idx = self.contacts.index(self.selected_contact)
                self.contacts[idx] = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "address": address
                }
            else:
                messagebox.showerror("Error", "Selected contact not found in database.")
                return
                
        self.save_contacts()
        self.refresh_contact_list(self.search_entry.get())
        self.clear_form()

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()