import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class CelestialBody:
    def __init__(self, name, distance_from_sun, mass, orbital_period):
        self.name = name
        self.distance_from_sun = distance_from_sun
        self.mass = mass
        self.orbital_period = orbital_period

    def __repr__(self):
        return f"{self.name} (Distance: {self.distance_from_sun} AU, Mass: {self.mass} kg, Orbital Period: {self.orbital_period} days)"


class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar System Objects Manager")

        # Lista obiektów
        self.objects = []

        # Interfejs użytkownika
        self.tree = ttk.Treeview(root, columns=('Name', 'Distance', 'Mass', 'Orbital Period'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Distance', text='Distance from Sun (AU)')
        self.tree.heading('Mass', text='Mass (kg)')
        self.tree.heading('Orbital Period', text='Orbital Period (days)')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Przycisk dodawania
        tk.Button(root, text="Add Object", command=self.add_object).pack(side=tk.LEFT, padx=5, pady=5)
        # Przycisk edytowania
        tk.Button(root, text="Edit Object", command=self.edit_object).pack(side=tk.LEFT, padx=5, pady=5)
        # Przycisk usuwania
        tk.Button(root, text="Remove Object", command=self.remove_object).pack(side=tk.LEFT, padx=5, pady=5)
        # Przycisk sortowania
        tk.Button(root, text="Sort by Distance", command=self.sort_by_distance).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(root, text="Sort by Mass", command=self.sort_by_mass).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(root, text="Sort by Orbital Period", command=self.sort_by_orbital_period).pack(side=tk.LEFT, padx=5, pady=5)

    def add_object(self):
        name = simpledialog.askstring("Input", "Enter the name of the object:")
        distance = float(simpledialog.askstring("Input", "Enter the distance from Sun (AU):"))
        mass = float(simpledialog.askstring("Input", "Enter the mass (kg):"))
        period = float(simpledialog.askstring("Input", "Enter the orbital period (days):"))

        obj = CelestialBody(name, distance, mass, period)
        self.objects.append(obj)
        self.update_treeview()

    def edit_object(self):
        selected_item = self.tree.selection()[0]
        selected_obj = self.objects[self.tree.index(selected_item)]

        name = simpledialog.askstring("Input", "Enter the new name of the object:", initialvalue=selected_obj.name)
        distance = float(simpledialog.askstring("Input", "Enter the new distance from Sun (AU):", initialvalue=selected_obj.distance_from_sun))
        mass = float(simpledialog.askstring("Input", "Enter the new mass (kg):", initialvalue=selected_obj.mass))
        period = float(simpledialog.askstring("Input", "Enter the new orbital period (days):", initialvalue=selected_obj.orbital_period))

        selected_obj.name = name
        selected_obj.distance_from_sun = distance
        selected_obj.mass = mass
        selected_obj.orbital_period = period
        self.update_treeview()

    def remove_object(self):
        selected_item = self.tree.selection()[0]
        del self.objects[self.tree.index(selected_item)]
        self.update_treeview()

    def sort_by_distance(self):
        self.objects.sort(key=lambda x: x.distance_from_sun)
        self.update_treeview()

    def sort_by_mass(self):
        self.objects.sort(key=lambda x: x.mass)
        self.update_treeview()

    def sort_by_orbital_period(self):
        self.objects.sort(key=lambda x: x.orbital_period)
        self.update_treeview()

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for obj in self.objects:
            self.tree.insert('', tk.END, values=(obj.name, obj.distance_from_sun, obj.mass, obj.orbital_period))

# Uruchomienie aplikacji
root = tk.Tk()
app = SolarSystemApp(root)
root.mainloop()
