import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk

class CelestialBody:
    def __init__(self, name, distance, mass, orbital_period):
        self.name = name
        self.distance = distance
        self.mass = mass
        self.orbital_period = orbital_period

    def __repr__(self):
        return f"{self.name} (Distance: {self.distance} AU, Mass: {self.mass} kg, Orbital Period: {self.orbital_period} days)"


class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar System Objects Manager")

        # List of objects
        self.objects = [
            CelestialBody("Mercury", 0.39, 0.0553, 88),
            CelestialBody("Venus", 0.72, 0.815, 225),
            CelestialBody("Earth", 1.00, 1, 365),
            CelestialBody("Mars", 1.52, 0.1075, 687),
            CelestialBody("Jupiter", 5.20, 317.8, 4333),
            CelestialBody("Saturn", 9.58, 95.2, 10759),
            CelestialBody("Uranus", 19.20, 14.6, 30687),
            CelestialBody("Neptune", 30.05, 17.2, 60190)
        ]

        self.tree = ttk.Treeview(root, columns=('Name', 'Distance', 'Mass', 'Orbital Period'), show='headings')
        self.tree.heading('Name', text='Name', command=lambda: self.bucket_sort('name'))
        self.tree.heading('Distance', text='Distance from Sun (AU)', command=lambda: self.bucket_sort('distance'))
        self.tree.heading('Mass', text='Mass (kg)', command=lambda: self.bucket_sort('mass'))
        self.tree.heading('Orbital Period', text='Orbital Period (days)', command=lambda: self.bucket_sort('orbital_period'))
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(root, text="Add Object", command=self.add_object)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(root, text="Edit Object", command=self.edit_object, state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_button = tk.Button(root, text="Remove Object", command=self.remove_object, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.root.bind('<Button-1>', self.deselect_item)

        self.update_treeview()

    
    def on_treeview_select(self, event):
        # Check if there is a selection
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.remove_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)


    def deselect_item(self, event):
        # Deselect if the click is on the background (not the treeview or buttons)
        widget = event.widget
        if widget not in [self.tree, self.add_button, self.edit_button, self.remove_button]:
            # Only deselect if clicked outside of Treeview and buttons
            self.tree.selection_remove(self.tree.selection())  # Remove selection from treeview
            self.update_button_states()  # Update button states


    def update_button_states(self):
        # Update the state of the buttons based on the selection
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
            popup.destroy()

        # Create a new popup window
        popup = tk.Toplevel(self.root)
        popup.title("Add New Object")

        # Name input
        tk.Label(popup, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Distance input
        tk.Label(popup, text="Distance from Sun (AU):").grid(row=1, column=0, padx=5, pady=5)
        distance_entry = tk.Entry(popup)
        distance_entry.grid(row=1, column=1, padx=5, pady=5)

        # Mass input
        tk.Label(popup, text="Mass (kg):").grid(row=2, column=0, padx=5, pady=5)
        mass_entry = tk.Entry(popup)
        mass_entry.grid(row=2, column=1, padx=5, pady=5)

        # Orbital Period input
        tk.Label(popup, text="Orbital Period (days):").grid(row=3, column=0, padx=5, pady=5)
        period_entry = tk.Entry(popup)
        period_entry.grid(row=3, column=1, padx=5, pady=5)

        # Submit button
        tk.Button(popup, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

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


    def edit_object(self):
        # Ensure a selection exists
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an object to edit.")
            return
        
        selected_item = selected_item[0]  # Get the first selected item
        selected_obj = self.objects[self.tree.index(selected_item)]

        name = simpledialog.askstring("Input", "Enter the new name of the object:", initialvalue=selected_obj.name)
        distance = float(simpledialog.askstring("Input", "Enter the new distance from Sun (AU):", initialvalue=selected_obj.distance))
        mass = float(simpledialog.askstring("Input", "Enter the new mass (kg):", initialvalue=selected_obj.mass))
        period = float(simpledialog.askstring("Input", "Enter the new orbital period (days):", initialvalue=selected_obj.orbital_period))

        selected_obj.name = name
        selected_obj.distance = distance
        selected_obj.mass = mass
        selected_obj.orbital_period = period
        self.update_treeview()


    def remove_object(self):
        # Ensure a selection exists
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an object to remove.")
            return
        
        selected_item = selected_item[0]  # Get the first selected item
        selected_obj = self.objects[self.tree.index(selected_item)]

        # Confirm removal
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {selected_obj.name}?"):
            del self.objects[self.tree.index(selected_item)]
            self.update_treeview()


    def bucket_sort(self, key):
        # Determine the attribute to sort by
        key_function = lambda obj: getattr(obj, key)

        if key == 'name':
            # For sorting by name, create 26 buckets for each letter A-Z
            bucket_count = 26
            buckets = [[] for _ in range(bucket_count)]
            
            for obj in self.objects:
                # Use the first letter to determine the bucket, normalize to uppercase
                index = ord(key_function(obj)[0].upper()) - ord('A')
                index = max(0, min(index, bucket_count - 1))  # Ensure index is within bounds
                buckets[index].append(obj)

        else:
            # For numeric attributes like distance, mass, and orbital period
            max_value = max(self.objects, key=key_function).distance  # Find the max value for bucket range
            bucket_count = len(self.objects)
            buckets = [[] for _ in range(bucket_count)]
            
            for obj in self.objects:
                index = int((key_function(obj) / max_value) * (bucket_count - 1))
                index = min(index, bucket_count - 1)  # Ensure index is within bounds
                buckets[index].append(obj)

        # Sort each bucket and concatenate the results
        self.objects = []
        for bucket in buckets:
            self.objects.extend(sorted(bucket, key=key_function))

        self.update_treeview()


    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for obj in self.objects:
            self.tree.insert('', tk.END, values=(obj.name, obj.distance, obj.mass, obj.orbital_period))


root = tk.Tk()
app = SolarSystemApp(root)
root.mainloop()
