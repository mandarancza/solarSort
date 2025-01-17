import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class CelestialBody:
    def __init__(self, name, distance, mass, orbital_period):
        self.name = name
        self.distance = distance
        self.mass = mass
        self.orbital_period = orbital_period

    def __repr__(self):
        return f"{self.name} (Distance: {self.distance} AU, Mass: {self.mass} Me, Orbital Period: {self.orbital_period} days)"

    def to_dict(self):
        return {
            "name": self.name,
            "distance": self.distance,
            "mass": self.mass,
            "orbital_period": self.orbital_period
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["distance"], data["mass"], data["orbital_period"])

class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar Sort")
        self.root.geometry("800x400")
        self.data_file = "celestial_bodies.json"

        # Load objects from file or initialize with default data
        self.objects = self.load_objects()

        self.sorting_state = {
            'name': False,  # Default sorting state
            'distance': False,
            'mass': False,
            'orbital_period': False
        }

        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))
        #style.map("Treeview.Heading", background=[('active', 'green'), ('!active', 'lightblue')])

        self.tree = ttk.Treeview(root, columns=('name', 'distance', 'mass', 'orbital_period'), show='headings')
        self.tree.heading('name', text='Name', command=lambda: self.bucket_sort('name'))
        self.tree.heading('distance', text='Distance from Sun (AU)', command=lambda: self.bucket_sort('distance'))
        self.tree.heading('mass', text='Mass (Me)', command=lambda: self.bucket_sort('mass'))
        self.tree.heading('orbital_period', text='Orbital Period (days)', command=lambda: self.bucket_sort('orbital_period'))
        self.tree.pack(fill=tk.BOTH, expand=True)


        style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=5)
        style.map('TButton', background=[('active', 'lightblue'), ('!active', 'lightgray')])

        self.add_button = ttk.Button(root, text="Add Object", command=self.add_object, style='TButton')
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = ttk.Button(root, text="Edit Object", command=self.edit_object, style='TButton')
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_button = ttk.Button(root, text="Remove Object", command=self.remove_object, style='TButton')
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.root.bind('<Button-1>', self.deselect_item)

        self.update_treeview()

    def load_objects(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [CelestialBody.from_dict(obj) for obj in data]
        else:
            # Default objects if file doesn't exist
            return [
                CelestialBody("Mercury", 0.39, 0.0553, 88),
                CelestialBody("Venus", 0.72, 0.815, 225),
                CelestialBody("Earth", 1.00, 1, 365),
                CelestialBody("Mars", 1.52, 0.1075, 687),
                CelestialBody("Jupiter", 5.20, 317.8, 4333),
                CelestialBody("Saturn", 9.58, 95.2, 10759),
                CelestialBody("Uranus", 19.20, 14.6, 30687),
                CelestialBody("Neptune", 30.05, 17.2, 60190)
            ]

    def save_objects(self):
        with open(self.data_file, 'w') as f:
            json.dump([obj.to_dict() for obj in self.objects], f)
            

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)

    def deselect_item(self, event):
        widget = event.widget
        if widget not in [self.tree, self.add_button, self.edit_button, self.remove_button]:
            self.tree.selection_remove(self.tree.selection())
            self.update_button_states()

    def update_button_states(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)

    def add_object(self):
        def submit():
            name = name_entry.get()
            try:
                distance = float(distance_entry.get())
                mass = float(mass_entry.get())
                period = float(period_entry.get())
            except ValueError:
                tk.messagebox.showerror("Invalid input", "Please enter valid numbers for distance, mass, and orbital period.")
                return

            obj = CelestialBody(name, distance, mass, period)
            self.objects.append(obj)
            self.update_treeview()
            self.save_objects()  # Save objects to file
            popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Add New Object")

        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(popup, text="Distance from Sun (AU):").grid(row=1, column=0, padx=5, pady=5)
        distance_entry = tk.Entry(popup)
        distance_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(popup, text="Mass (Mw):").grid(row=2, column=0, padx=5, pady=5)
        mass_entry = tk.Entry(popup)
        mass_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(popup, text="Orbital Period (days):").grid(row=3, column=0, padx=5, pady=5)
        period_entry = tk.Entry(popup)
        period_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_button = ttk.Button(popup, text="Submit", command=submit, style='TButton')
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        popup.update_idletasks()
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()

        popup_x = main_x + (main_width // 2) - (popup_width // 2)
        popup_y = main_y + (main_height // 2) - (popup_height // 2)

        popup.geometry(f"+{popup_x}+{popup_y}")
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)

    def edit_object(self):
        # Ensure a selection exists
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an object to edit.")
            return
        
        selected_item = selected_item[0]  # Get the first selected item
        selected_obj = self.objects[self.tree.index(selected_item)]

        # Create a new popup window for editing
        def submit():
            name = name_entry.get()
            try:
                distance = float(distance_entry.get())
                mass = float(mass_entry.get())
                period = float(period_entry.get())
            except ValueError:
                tk.messagebox.showerror("Invalid input", "Please enter valid numbers for distance, mass, and orbital period.")
                return

            selected_obj.name = name
            selected_obj.distance = distance
            selected_obj.mass = mass
            selected_obj.orbital_period = period
            self.update_treeview()
            self.save_objects()  # Save updated objects to file
            popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("Edit Object")

        # Name input
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.insert(0, selected_obj.name)  # Populate with the current name
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Distance input
        tk.Label(popup, text="Distance from Sun (AU):").grid(row=1, column=0, padx=5, pady=5)
        distance_entry = tk.Entry(popup)
        distance_entry.insert(0, str(selected_obj.distance))  # Populate with the current distance
        distance_entry.grid(row=1, column=1, padx=5, pady=5)

        # Mass input
        tk.Label(popup, text="Mass (Me):").grid(row=2, column=0, padx=5, pady=5)
        mass_entry = tk.Entry(popup)
        mass_entry.insert(0, str(selected_obj.mass))  # Populate with the current mass
        mass_entry.grid(row=2, column=1, padx=5, pady=5)

        # Orbital Period input
        tk.Label(popup, text="Orbital Period (days):").grid(row=3, column=0, padx=5, pady=5)
        period_entry = tk.Entry(popup)
        period_entry.insert(0, str(selected_obj.orbital_period))  # Populate with the current orbital period
        period_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_button = ttk.Button(popup, text="Submit", command=submit, style='TButton')
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Center the popup window
        popup.update_idletasks()  # Update "requested size" from geometry manager
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()

        # Calculate the position for the popup to be centered
        popup_x = main_x + (main_width // 2) - (popup_width // 2)
        popup_y = main_y + (main_height // 2) - (popup_height // 2)

        popup.geometry(f"+{popup_x}+{popup_y}")  # Set the position of the popup

        popup.transient(self.root)  # Make the popup window stay on top
        popup.grab_set()            # Prevent interaction with the main window
        self.root.wait_window(popup)  # Wait for the popup window to be closed

    def remove_object(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an object to remove.")
            return
        
        selected_item = selected_item[0]
        selected_obj = self.objects[self.tree.index(selected_item)]

        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {selected_obj.name}?"):
            del self.objects[self.tree.index(selected_item)]
            self.update_treeview()
            self.save_objects()


    def bucket_sort(self, key):
        if self.sorting_state[key] == True:
            self.sorting_state[key] = False
        else:
            self.sorting_state[key] = True
        
        self.objects.sort(key=lambda obj: getattr(obj, key), reverse=self.sorting_state[key])
        self.update_treeview()
        #print(self.column_text(key))
        self.update_sorting_icons(key)


    def update_sorting_icons(self, sorted_key):
        # Update the column headers to display the sorting direction
        for col in self.tree["columns"]:
            lastchar = self.tree.heading(col, "text")[-1]
            if lastchar == '↑' or lastchar == '↓':
                    self.tree.heading(col, text=self.tree.heading(col, "text")[:-2])
            if col == sorted_key:
                # Add sorting icon based on current sorting direction
                if self.sorting_state[sorted_key] == False:
                    self.tree.heading(col, text=self.tree.heading(col, "text") + ' ↑')
                else:
                    self.tree.heading(col, text=self.tree.heading(col, "text") + ' ↓')
            

    def column_text(self, heading_name):
        # Iterate through the columns to find the heading that matches
        for column in self.tree["columns"]:
            # Get the text of the heading
            #heading_val = self.tree.heading(column, )
            print(self.tree.heading(column))
            #print(column)

            # Check if it matches the desired heading
            if column == self:
                return self.tree.heading(column, "text")  # Return the column ID if found
        
        return None

    def update_treeview(self):
        # Clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Define tags for alternating row colors
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#ebebeb')

        # Insert the objects with alternating row tags
        for idx, obj in enumerate(self.objects):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', tk.END, values=(obj.name, obj.distance, obj.mass, obj.orbital_period), tags=(tag,))


root = tk.Tk()
app = SolarSystemApp(root)
root.mainloop()