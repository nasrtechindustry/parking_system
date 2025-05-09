import tkinter as tk
from tkinter import messagebox , ttk
from config import *
from models import User , Vehicle ,  Slot , ParkingSlot ,Response , Payment , Reservation
from config import *
from models import Session
from sqlalchemy.exc import SQLAlchemyError , NoResultFound
from datetime import datetime
from sqlalchemy import func


class Login:
    def __init__(self, root, switch_to_signup = None):
        self.root = root
        self.switch_to_signup = switch_to_signup
        
        # Creating the login frame
        self.frame = tk.Frame(root, padx=40, pady=30 ,relief=tk.RAISED , bd=2 )
        self.frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Intro label
        self.intro_label = tk.Label(
            self.frame,
            text="Smart Parking System\nLogin to continue",
            font=("monospace", 18, "bold"),
            fg=MAIN_COLOR,
        )
        self.intro_label.grid(row=0, columnspan=2, padx=20, pady=20)

        # Email field
        self.email_label = tk.Label(self.frame, text="Email", font=FONT)
        self.email_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=20, pady=20)

        # Password field
        self.password_label = tk.Label(self.frame, text="Password", font=FONT)
        self.password_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")
        self.password_entry = tk.Entry(self.frame, show='*', width=30)
        self.password_entry.grid(row=5, column=1, padx=20, pady=20)

        # Login button
        self.login_button = tk.Button(
            self.frame, text="Login", bg=MAIN_COLOR, fg="white", width=28,
            command=self.submit_form
        )
        self.login_button.grid(row=6, column=1, padx=20, pady=20)

        # Click to sign up view
        self.signup_btn = tk.Button(
            self.frame,
            text="Have no Account?",
            bg=MAIN_COLOR,
            fg="white",
            width=28,
            command=self.switch_to_signup if self.switch_to_signup else self.default_action,
        )
        self.signup_btn.grid(row=7, column=1, padx=20, pady=20 , )

    def hide_frame(self):
        """Hides the login frame"""
        self.frame.place_forget()

    def show_frame(self):
        """Shows the login frame"""
        self.frame.place(relx=0.5, rely=0.4, anchor="center")
        
    def submit_form(self):
        """Handles the login form submission"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not all([email , password]):
            return messagebox.showerror('WARNING' , "Please Fill in all credentials")

        
        result = User().login(email=email, password=password)
        
        if result['success']:
            messagebox.showinfo("LOGGED IN SOON" ,result['message'])
            Dashboard(self.root).show_dashboard()
            return self.hide_frame()
            
        return messagebox.showwarning("WARNING" , result['message'])    

class SignUp:
    def __init__(self, root,  switch_to_login=None):
        self.root = root
        self.switch_to_login = switch_to_login
        
        # Creating the sign-up frame
        self.frame = tk.Frame(root, padx=100, pady=30,relief=tk.RAISED , bd=2)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")   
        
        # Intro label
        self.intro_label = tk.Label(self.frame, text="Smart Parking System\nCreate Account", 
                                    font=("monospace", 18, "bold"), fg=MAIN_COLOR)
        self.intro_label.grid(row=0, columnspan=2, padx=20, pady=20)

        # Username field
        self.firstname_label = tk.Label(self.frame, text="First name", font=FONT)
        self.firstname_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.firstname_entry = tk.Entry(self.frame, width=30)
        self.firstname_entry.grid(row=1, column=1, padx=20, pady=20)
        
         # Username field
        self.lastname_label = tk.Label(self.frame, text="Last name", font=FONT)
        self.lastname_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.lastname_entry = tk.Entry(self.frame, width=30)
        self.lastname_entry.grid(row=2, column=1, padx=20, pady=20)
        # Email field
        self.email_label = tk.Label(self.frame, text="Email", font=FONT)
        self.email_label.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.grid(row=3, column=1, padx=20, pady=20)

        self.roles = ["customer", "operator"]
        self.role_var = tk.StringVar(value=self.roles[0])  

        # Label for the dropdown
        self.role_label = tk.Label(self.frame, text="Role", font=FONT)
        self.role_label.grid(row=4, column=0, padx=20, pady=20, sticky="w")

        # Dropdown menu
        self.role_menu = tk.OptionMenu(self.frame, self.role_var ,*self.roles)
        self.role_menu.grid(row=4, column=1, padx=20, pady=20)
        self.role_menu.config(width=26)
        
        # Password field
        self.password_label = tk.Label(self.frame, text="Password", font=FONT)
        self.password_label.grid(row=5, column=0, padx=20, pady=20, sticky="w")
        self.password_entry = tk.Entry(self.frame, show='*', width=30)
        self.password_entry.grid(row=5, column=1, padx=20, pady=20)
        
        # Sign-up button
        self.signup_button = tk.Button(self.frame, text="Sign Up", bg=MAIN_COLOR, fg="white", command=self.submit_form, width=28)
        self.signup_button.grid(row=6, column=1, padx=20, pady=20)
        
        # Click to sign in view
        self.sign_btn = tk.Button(self.frame, text="Have an Account?", bg=MAIN_COLOR, fg="white", width=28, command=self.switch_to_login)
        self.sign_btn.grid(row=7, column=1, padx=20, pady=20)

    def hide_frame(self):
        self.frame.place_forget()  # Hide the sign-up frame

    def show_frame(self):
        self.frame.place(relx=0.5, rely=0.4, anchor="center")  # Show the sign-up frame

    def go_to_login(self):
        self.hide_frame()  # Hide the sign-up frame
        self.switch_to_login()  # Switch to login

    def submit_form(self):
        """Calls the controller's sign-up method."""
        user_instance = User(
                self.firstname_entry.get(),
                self.lastname_entry.get(),
                self.email_entry.get(),
                self.role_var.get(),
                self.password_entry.get()
        )
        
        if msg := user_instance.register():
            messagebox.showinfo("SUCCESS" , f'{msg}')
            self.hide_frame()
            self.go_to_login()

class Dashboard(Response):
    """THIS IS DASHBOARD VIEW"""
    def __init__(self, root):
        self.root = root
        # self.root.title("Dashboard")
        self.root.configure(bg="#f0f0f5")

        self.menu = tk.Menu(self.root, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.root.config(menu=self.menu)

        # Home Menu
        self.home_menu = tk.Menu(self.menu, tearoff=0, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.home_menu.add_command(label="Dashboard", command=self.show_dashboard)
        self.home_menu.add_command(label="Logout", command=self.root.quit)
        self.menu.add_cascade(label="Home", menu=self.home_menu)

        # Vehicles Menu
        self.vehicles_menu = tk.Menu(self.menu, tearoff=0, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.vehicles_menu.add_command(label="Manage Vehicles", command=self.show_vehicles)
        self.menu.add_cascade(label="Vehicles", menu=self.vehicles_menu)

        # Parking Slots Menu
        self.parking_slots_menu = tk.Menu(self.menu, tearoff=0, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.parking_slots_menu.add_command(label="Manage Parking Slots", command=self.show_parking_slots)
        self.menu.add_cascade(label="Parking Slots", menu=self.parking_slots_menu)

        # Payments Menu
        self.payments_menu = tk.Menu(self.menu, tearoff=0, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.payments_menu.add_command(label="Manage Payments", command=self.show_payments)
        self.menu.add_cascade(label="Payments", menu=self.payments_menu)

        # Reservations Menu
        self.reservations_menu = tk.Menu(self.menu, tearoff=0, bg=MAIN_COLOR, fg="white", activebackground=MAIN_COLOR, activeforeground="white")
        self.reservations_menu.add_command(label="Manage Reservations", command=self.show_reservations)
        self.menu.add_cascade(label="Reservations", menu=self.reservations_menu)


        # Frames
        self.dashboard_frame = tk.Frame(self.root, bg="#e6e6e6", padx=20, pady=20)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        # Ensure the row and column in the root are configured to expand and fill the space
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def clear_frame(self):
        """Clears all widgets from the current frame."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.grid_forget()

    def show_frame(self, frame):
        """Displays the specified frame."""
        self.clear_frame()
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def show_dashboard(self):
        """Displays the Dashboard frame."""
        self.dashboard_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f2f2f2")
        
        # Set up the grid for the dashboard frame to expand
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1) 
        self.dashboard_frame.grid_rowconfigure(0, weight=0)  
        self.dashboard_frame.grid_rowconfigure(1, weight=0)
        
        # Configure columns for the cards to expand proportionally
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_frame.grid_columnconfigure(2, weight=1)

        # Label at the top of the dashboard
        label = tk.Label(self.dashboard_frame, text="Welcome To Seamless Smart Parking Management System", font=FONT, fg=MAIN_COLOR, pady=10)
        label.grid(row=0, column=0, columnspan=3, pady=10, sticky="we")

        # Card to display total vehicles
        card_frame_1 = tk.Frame(self.dashboard_frame, bg="#ffaacc", relief="raised", bd=3, padx=20, pady=20)
        card_frame_1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Only expand horizontally

        # Total vehicles label
        total_vehicles = Session().query(Vehicle).count()
        card_title_1 = tk.Label(card_frame_1, text="Total Vehicles", font=("Arial", 16, "bold"), bg="#ffaacc")
        card_title_1.grid(row=0, column=0, pady=(0, 10))

        vehicle_count_label = tk.Label(card_frame_1, text=str(total_vehicles), font=("Arial", 24, "bold"), fg="#4CAF50", bg="#ffaacc")
        vehicle_count_label.grid(row=1, column=0)

        # Card to display available parking slots
        card_frame_2 = tk.Frame(self.dashboard_frame, bg="#80ccff", relief="raised", bd=3, padx=20, pady=20)
        card_frame_2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # Only expand horizontally

        # Available parking slots label
        available_slots = Session().query(Slot).filter(Slot.is_occupied == False , Slot.is_reserved == False).count()
        card_title_2 = tk.Label(card_frame_2, text="Available Slots", font=("Arial", 16, "bold"), bg="#80ccff")
        card_title_2.grid(row=0, column=0, pady=(0, 10))

        available_slots_label = tk.Label(card_frame_2, text=str(available_slots), font=("Arial", 24, "bold"), fg="#4CAF50", bg="#80ccff")
        available_slots_label.grid(row=1, column=0)

        # Card to display total revenue
        card_frame_3 = tk.Frame(self.dashboard_frame, bg="#ffc107", relief="raised", bd=3, padx=20, pady=20)
        card_frame_3.grid(row=1, column=2, padx=10, pady=10, sticky="ew")  # Only expand horizontally

        # Calculate total revenue
        total_revenue = Session().query(func.sum(Payment.payment_amount)).filter(Payment.is_paid == True).scalar() or 0

        card_title_3 = tk.Label(card_frame_3, text="Total Revenue", font=("Arial", 16, "bold"), bg="#ffc107")
        card_title_3.grid(row=0, column=0, pady=(0, 10))

        total_revenue_label = tk.Label(card_frame_3, text=str(total_revenue) + " TZS", font=("Arial", 24, "bold"), fg="#4CAF50", bg="#ffc107")
        total_revenue_label.grid(row=1, column=0)

        self.show_frame(self.dashboard_frame)

    def hide_dashboard(self):
        """Hides the Dashboard frame."""
        self.dashboard_frame.grid_forget()

    def refresh_vehicle_treeview(self):
        """Refreshes the vehicles Treeview with updated data."""
        vehicles = self.get_all_vehicles()  # Fetch all vehicles from the database

        # Clear existing rows in the Treeview
        for item in self.vehicle_trees.get_children():
            self.vehicle_trees.delete(item)

        # Repopulate the Treeview with new data
        for idx, vehicle in enumerate(vehicles, start=1):
            full_name = f"{vehicle['first_name']} {vehicle['last_name']}"
            self.vehicle_trees.insert(
                "", "end", values=(str(idx), vehicle["plate_number"], full_name, vehicle["email"], "Delete")
            )

    def show_vehicles(self):
        """Displays the Vehicles management frame."""
        vehicles_frame = tk.Frame(self.root , padx=20, pady=20 ,bg="#f2f2f2")
        
        # Add vehicle form
        add_vehicle_form = tk.Frame(vehicles_frame, relief="raised", bd=3 , padx=10, pady=10 , bg='#fff' )
        add_vehicle_form.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        
        
        label = tk.Label(vehicles_frame, text="VEHICLES MANAGEMENT", font=FONT  , fg=MAIN_COLOR ,pady=10)
        label.grid(row=0, column=0, pady=10 , columnspan=2 , sticky='we' , padx=10 ,)

        label = tk.Label(add_vehicle_form, text="Manage vehicles", font=FONT , bg='#fff')
        label.grid(row=0, column=0, pady=10 , columnspan=3 , sticky='w' , padx=10)

        # Customer Email input
        self.email_label = tk.Label(add_vehicle_form, text="Customer Email:", font=("Arial", 12), bg="#ffffff")
        self.email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(add_vehicle_form, width=30)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5 , columnspan=2)

        # Car Plate Number input
        self.plate_number_label = tk.Label(add_vehicle_form, text="Car Plate Number:", font=("Arial", 12), bg="#ffffff")
        self.plate_number_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.plate_number_entry = tk.Entry(add_vehicle_form, width=30)
        self.plate_number_entry.grid(row=2, column=1, padx=10, pady=5 , columnspan=2)

        # Submit Button
        self.add_vehicle_button = tk.Button(
            add_vehicle_form, text="Add Vehicle", fg="white", font=FONT, 
            command=self.submit_vehicle_form, width=20 , bg=MAIN_COLOR
        )
        self.add_vehicle_button.grid(row=3, column=1, padx=10, pady=10 ,sticky='we')
        
        self.edit_vehicle_button = tk.Button(
            add_vehicle_form, text="Edit Vehicle", fg="white", font=FONT, bg=MAIN_COLOR ,
            command=self.submit_vehicle_form, width=20 
        )
        # self.edit_vehicle_button.grid(row=4, column=1, padx=10, pady=10 , sticky='we')
        
        self.delete_vehicle_button = tk.Button(
            add_vehicle_form, text="Delete Vehicle", fg="white", font=FONT, bg='red' ,
            command=self.delete_vehicle, width=20 
        )
        self.delete_vehicle_button.grid(row=4, column=1, padx=10, pady=10 , sticky='we')


        # Vehicles Table
        self.table_frame = tk.Frame(vehicles_frame, bg="#f2f2f2" , bd=3 , relief='raised')
        self.table_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

       

        # Create Treeview
        columns = ("#","plate_number", "full_name", "email")
        self.vehicle_trees = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)
        
        # Define Columns
        self.vehicle_trees.heading("#", text="#")
        self.vehicle_trees.column("#", anchor='center')
        self.vehicle_trees.heading("plate_number", text="Plate Number")
        self.vehicle_trees.column("plate_number", anchor="w")
        self.vehicle_trees.heading("full_name", text="Full Name")
        self.vehicle_trees.column("full_name", anchor="w")
        self.vehicle_trees.heading("email", text="Email")
        self.vehicle_trees.column("email", anchor="w")


        # Attach a Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.vehicle_trees.yview)
        self.vehicle_trees.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.vehicle_trees.pack(fill="both", expand=True)

        # Populate the Treeview
        vehicles = self.get_all_vehicles()  
        x = 0# Fetch all vehicles from the database
        for vehicle in vehicles:
            x = x + 1
            full_name = f"{vehicle['first_name']} {vehicle['last_name']}"
            self.vehicle_trees.insert(
                "", "end", values=(str(f'{x}'),vehicle["plate_number"], full_name, vehicle["email"], "Delete")
            )

       

                # Show the frame
        vehicles_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configure the parent frame to allow full width
        self.root.grid_rowconfigure(0, weight=1)  # Adjust row weight for full height if needed
        self.root.grid_columnconfigure(0, weight=1)  # Adjust column weight for full width

        vehicles_frame.grid_columnconfigure(0, weight=1)  # Ensure the form adjusts
        vehicles_frame.grid_columnconfigure(1, weight=1)  # Ensure the table adjusts

        self.show_frame(vehicles_frame)

    def get_all_vehicles(self):
        """Fetch all vehicles from the database."""
        session = Session()  # Assuming Session is already defined elsewhere
        try:
            vehicles = (
                session.query(Vehicle, User)
                .join(User, Vehicle.customer_id == User.user_id)
                .with_entities(
                    Vehicle.plate_number,
                    User.first_name,
                    User.last_name,
                    User.email,
                )
                .all()
            )
            return [
                {
                    "plate_number": plate_number,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                }
                for plate_number , first_name , last_name , email in vehicles
            ]
        finally:
            session.close()

    def delete_vehicle(self):
        """Handle deleting a vehicle."""
        vehicle = self.plate_number_entry.get()
        
        if not vehicle:
            return messagebox.showwarning("warning" , "Please supply plate number")
        
        isAllow = messagebox.askyesno("VEHICLE DELETION" , f'are you sure that you want to delete this vehicle "{vehicle}"')
        
        if isAllow:
            session = Session()
            try:
                vehicle_obj = session.query(Vehicle).filter_by(plate_number=vehicle).first()
                if vehicle_obj:
                    session.delete(vehicle_obj)
                    session.commit()
                    messagebox.showinfo("Success", f"Vehicle {vehicle} deleted successfully.")
                    self.show_vehicles()  # Refresh the vehicles list
                else:
                    messagebox.showerror("Error", "Vehicle not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                session.close()

    def submit_vehicle_form(self):
        """Handles the vehicle form submission."""
        customer_email = self.email_entry.get()
        plate_number = self.plate_number_entry.get()

        if not all([customer_email, plate_number]):
            return messagebox.showerror('WARNING', "Please Fill in all fields")

        new = Vehicle()
        result = new.add_vehicle(customer_email=customer_email,plate_number=plate_number)
        
        if result['success']:
            # Show success message
            messagebox.showinfo("Vehicle Added", result['message'])
            
            return self.refresh_vehicle_treeview()

        
        if not result['success']:
            return messagebox.showwarning('ERROR' , result['message'])

    def show_parking_slots(self):
        """Displays the Parking Slots management frame."""
        parking_slots_frame = tk.Frame(self.root, bg="#f2f2f2", padx=20, pady=20)

        # Header Label
        label = tk.Label(parking_slots_frame, text="PARKING SLOT MANAGEMENT", font=FONT, fg=MAIN_COLOR ,pady=10)
        label.grid(row=0, column=0, pady=10, columnspan=2, sticky="we", padx=10)

        # Left Column (Forms)
        forms_frame = tk.Frame(parking_slots_frame, relief="raised", bd=3, bg="#ffffff" ,padx=20 , pady=20)
        forms_frame.grid(row=1, column=0, padx=10, pady=20, sticky="n")

        # Create Parking Slot Form (Existing)
        slot_label = tk.Label(forms_frame, text="Create Parking Slot", font=FONT, bg="#ffffff", fg="#555555")
        slot_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        self.slot_name_label = tk.Label(forms_frame, text="Slot Name:", font=("Arial", 12), bg="#ffffff")
        self.slot_name_label.grid(row=1, column=0,  pady=5, sticky="w")
        self.slot_name_entry = tk.Entry(forms_frame, width=30)
        self.slot_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.create_slot_button = tk.Button(
            forms_frame, text="Create Slot", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.create_parking_slot, width=20
        )
        self.create_slot_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="we")

        # Assign Vehicle to Slot Form (Existing)
        assign_label = tk.Label(forms_frame, text="Assign Vehicle to Slot", font=FONT, bg="#ffffff", fg="#555555")
        assign_label.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")

        self.vehicle_plate_label = tk.Label(forms_frame, text="Vehicle Plate:", font=("Arial", 12), bg="#ffffff")
        self.vehicle_plate_label.grid(row=4, column=0,  pady=5, sticky="w")
        self.vehicle_plate_entry = tk.Entry(forms_frame, width=30)
        self.vehicle_plate_entry.grid(row=4, column=1, padx=10, pady=5)

        self.slot_select_label = tk.Label(forms_frame, text="Slot Name:", font=("Arial", 12), bg="#ffffff")
        self.slot_select_label.grid(row=5, column=0, pady=5, sticky="w")
        self.slots = self.get_available_slots()  # Fetch slots from the database
        self.slot_select_entry = ttk.Combobox(forms_frame, values=self.slots, state="readonly", width=30)
        self.slot_select_entry.grid(row=5, column=1, padx=10, pady=5)

        self.assign_vehicle_button = tk.Button(
            forms_frame, text="Assign Vehicle", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.assign_vehicle_to_slot, width=20
        )
        self.assign_vehicle_button.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="we")

        # Release Parking Slot Form (New)
        release_label = tk.Label(forms_frame, text="Release Vehicle from Slot", font=FONT, bg="#ffffff", fg="#555555")
        release_label.grid(row=7, column=0, columnspan=2, pady=(20, 10), sticky="w")

        self.release_vehicle_plate_label = tk.Label(forms_frame, text="Vehicle Plate:", font=("Arial", 12), bg="#ffffff")
        self.release_vehicle_plate_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.release_vehicle_plate_entry = tk.Entry(forms_frame, width=30)
        self.release_vehicle_plate_entry.grid(row=8, column=1, padx=10, pady=5)

        self.release_vehicle_button = tk.Button(
            forms_frame, text="Release Vehicle", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.release_vehicle_from_slot, width=20
        )
        self.release_vehicle_button.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky="we")

        # Table Frame for Displaying Assigned Vehicles (Existing)
        table_frame = tk.Frame(parking_slots_frame, bg="#f2f2f2", bd=3, relief="raised")
        table_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Table Header
        columns = ("#", "plate_number", "slot_name", "parking_time")
        self.assigned_vehicle_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.assigned_vehicle_tree.heading("#", text="#")
        self.assigned_vehicle_tree.column("#", anchor="center", width=30)
        self.assigned_vehicle_tree.heading("plate_number", text="Plate Number")
        self.assigned_vehicle_tree.column("plate_number", anchor="w")
        self.assigned_vehicle_tree.heading("slot_name", text="Slot Name")
        self.assigned_vehicle_tree.column("slot_name", anchor="w")
        self.assigned_vehicle_tree.heading("parking_time", text="Parking Time")
        self.assigned_vehicle_tree.column("parking_time", anchor="e")

        
        

        # Attach a Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.assigned_vehicle_tree.yview)
        self.assigned_vehicle_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.assigned_vehicle_tree.pack(fill="both", expand=True)

        # Populate the Table (Existing)
        assigned_vehicles = self.get_assigned_vehicles()  # Fetch all assigned vehicles from the database
        if assigned_vehicles:
            for idx, vehicle in enumerate(assigned_vehicles, start=1):
                self.assigned_vehicle_tree.insert("", "end", values=(
                    idx, vehicle["vehicle_plate_number"], vehicle["slot_name"] , vehicle['entry_time'] 
                ))

        # Configure the parent frame to allow full width
        parking_slots_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        parking_slots_frame.grid_columnconfigure(0, weight=1)  # Ensure the forms adjust
        parking_slots_frame.grid_columnconfigure(1, weight=1)  # Ensure the table adjusts

        self.show_frame(parking_slots_frame)

    def release_vehicle_from_slot(self):
        """Releases a vehicle from its assigned parking slot."""
        plate_number = self.release_vehicle_plate_entry.get().strip()

        if not plate_number:
            return messagebox.showwarning("WARNING", "Please enter a vehicle plate number.")

        session = Session()
        try:
            # Find the parking slot assignment for the vehicle
            parking_slot = session.query(ParkingSlot).join(Vehicle).filter(Vehicle.plate_number == plate_number).first()

            if not parking_slot:
                return messagebox.showerror("ERROR", f"No vehicle found with plate number {plate_number} in any slot.")

            # Update the corresponding slot to mark it as available
            slot = session.query(Slot).filter(Slot.slot_id == parking_slot.slot_id).first()
            if slot:
                slot.is_occupied = False

            # Update the exit_time to now and set slot_id to None
            session.query(ParkingSlot).filter(ParkingSlot.slot_id == parking_slot.slot_id).update({
                ParkingSlot.slot_id: None,
                ParkingSlot.exit_time: datetime.now()
            })
            session.commit()  # Commit the transaction
            self.refresh_assigned_vehicle_table()
            
            return messagebox.showinfo("SUCCESS", f"Vehicle with plate number {plate_number} has been released from the parking slot.")

        except Exception as e:
            session.rollback()  # Rollback in case of an error
            return messagebox.showerror("ERROR", f"Error: {str(e)}")
        finally:
            session.close()

    def create_parking_slot(self):
        slot_name = self.slot_name_entry.get()
        
        if not slot_name:
            return messagebox.showwarning("WARNING!" , "Please Provide precise name for slot")
        
        slot = Slot()
        result = slot.create_slot(slot_name=slot_name)
        
        if not result['success'] :
           
            return messagebox.showwarning("ERROR" , result['message'])
        self.get_available_slots()
        self.refresh_assigned_vehicle_table()
        return messagebox.showinfo('SUCCESS  ', result['message']) 

    def get_available_slots(self):
        """Fetch all available parking slots from the database."""
        session = Session() 
        try:
            slots = session.query(Slot.slot_name).filter(Slot.is_occupied == 0 , Slot.is_reserved == 0).all() 
            return [slot[0] for slot in slots]  
        except SQLAlchemyError as e:
            print(f"Error fetching slots: {str(e)}")
            return []
        finally:
            session.close() 
                
    def assign_vehicle_to_slot(self):
        slot_name = self.slot_select_entry.get()
        plate_number = self.vehicle_plate_entry.get()
        
        if not all([slot_name , plate_number]) :
            return messagebox.showwarning("WARNING" , "Please Slot name and plate number are mandatory")
        
        parking  = ParkingSlot()
        result = parking.assign_slot_to_vehicle(plate_number=plate_number , slot_name=slot_name)
        
        if not result['success']:
            return messagebox.showerror("ERROR" , result['message'])
        self.refresh_assigned_vehicle_table()
        return messagebox.showinfo('SUCCESS ', result['message'])
    
    def get_assigned_vehicles(self):
        
        slots = ParkingSlot()
        
        result = slots.get_assigned_vehicles()
        
        return result['data']
    
    def refresh_assigned_vehicle_table(self):
        """Refreshes the assigned vehicle table with the latest data."""
        # Clear the current rows in the table
        self.refresh_available_slots()
        for item in self.assigned_vehicle_tree.get_children():
            self.assigned_vehicle_tree.delete(item)
        
        assigned_vehicles = self.get_assigned_vehicles()
        
        # Repopulate the table with the latest data
        for idx, vehicle in enumerate(assigned_vehicles, start=1):
            self.assigned_vehicle_tree.insert(
                "", "end", values=(
                    idx,
                    vehicle["vehicle_plate_number"],
                    vehicle["slot_name"],
                    vehicle["entry_time"]
                )
            )

    def refresh_available_slots(self):
        """Refresh the list of available parking slots in the Combobox."""
        try:
            self.slots = self.get_available_slots()
            
            self.slot_select_entry['values'] = self.slots
            
            self.slot_select_entry.set('')
        except Exception as e:
            print(f"Error refreshing available slots: {str(e)}")

    def show_payments(self):
        """Displays the Payments management frame."""
        payments_frame = tk.Frame(self.root, bg="#f2f2f2", padx=20, pady=20)

        # Header Label
        label = tk.Label(payments_frame, text="PAYMENT MANAGEMENT", font=FONT, fg=MAIN_COLOR ,pady=10)
        label.grid(row=0, column=0, pady=10, columnspan=2, sticky="we", padx=10)

        # Left Column (Form)
        forms_frame = tk.Frame(payments_frame, relief="raised", bd=3, bg="#ffffff")
        forms_frame.grid(row=1, column=0, padx=10, pady=20, sticky="n")

        # Payment Form
        payment_label = tk.Label(forms_frame, text="Vehicle Payment", font=FONT, bg="#ffffff", fg="#555555")
        payment_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        
        # check payment
        self.payment_plate_label = tk.Label(forms_frame, text="Vehicle Plate :", font=("Arial", 12), bg="#ffffff")
        self.payment_plate_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.pay_check = tk.Entry(forms_frame, width=30)
        self.pay_check.grid(row=2, column=1, padx=10, pady=5)

        self.check_payment_button = tk.Button(
            forms_frame, text="Check Payment", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.check_vehicle_payment, width=20
        )
        self.check_payment_button.grid(row=3, column=1 ,  padx=10, pady=10, sticky="we")
        
        # make payment
        self.payment_plate_number_label = tk.Label(forms_frame, text="Vehicle Plate:", font=("Arial", 12), bg="#ffffff")
        self.payment_plate_number_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.payment_plate_number_entry = tk.Entry(forms_frame, width=30)
        self.payment_plate_number_entry.grid(row=4, column=1, padx=10, pady=5)
        
        self.payment_plate_label = tk.Label(forms_frame, text="Payment Amount:", font=("Arial", 12), bg="#ffffff")
        self.payment_plate_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.payment_amount = tk.Entry(forms_frame, width=30)
        self.payment_amount.grid(row=5, column=1, padx=10, pady=5)

        self.check_payment_button = tk.Button(
            forms_frame, text="Make Payment", fg="white", font=FONT, bg=MAIN_COLOR,
            command=self.make_payment, width=20
        )
        self.check_payment_button.grid(row=6, column=1 ,  padx=10, pady=10, sticky="we")

        # Table Frame for Displaying Payment Records
        table_frame = tk.Frame(payments_frame, bg="#f2f2f2", bd=3, relief="raised")
        table_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Table Header
        columns = ("#", "plate_number", "paid_amount", "payment_status")
        self.payment_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.payment_tree.heading("#", text="#")
        self.payment_tree.column("#", anchor="center", width=30)
        self.payment_tree.heading("plate_number", text="Plate Number")
        self.payment_tree.column("plate_number", anchor="w")
        self.payment_tree.heading("paid_amount", text="Paid Amount")
        self.payment_tree.column("paid_amount", anchor="e")
        self.payment_tree.heading("payment_status", text="Payment Status")
        self.payment_tree.column("payment_status", anchor="w")

        # Attach a Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.payment_tree.yview)
        self.payment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.payment_tree.pack(fill="both", expand=True)

        # Configure the parent frame to allow full width
        payments_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        payments_frame.grid_columnconfigure(0, weight=1)  # Ensure the forms adjust
        payments_frame.grid_columnconfigure(1, weight=1)  # Ensure the table adjusts
        
        self.populate_payment_table()

        self.show_frame(payments_frame)

    def check_vehicle_payment(self):
        """Checks if the entered vehicle has made a payment and calculates the total amount required."""
        plate_number = self.pay_check.get()

        if not plate_number:
            return messagebox.showwarning("WARNING", "Vehicle plate number is required")

        session = Session()
        try:
            # Fetch the parking slot and payment record for the vehicle
            parking_slot = session.query(ParkingSlot).join(Vehicle).filter(Vehicle.plate_number == plate_number).first()

            if not parking_slot:
                return messagebox.showinfo("INFO", f"No parking slot record found for {plate_number}")
            
            # Calculate the duration of parking in minutes
            if parking_slot.entry_time and parking_slot.exit_time:
                entry_time = parking_slot.entry_time
                exit_time = parking_slot.exit_time
                duration_in_minutes = (exit_time - entry_time).total_seconds() / 60  # Convert seconds to minutes
                
                # Calculate the total payment
                money_per_minute = 3000  # 3000 TZS per minute
                total_amount = duration_in_minutes * money_per_minute

                return total_amount , messagebox.showinfo("SUCCESS", f"Total payment required for {plate_number}: {total_amount:.0f} TZS")

            else:
                return messagebox.showinfo("INFO", f"Entry or Exit time missing for {plate_number}")

        except Exception as e:
            return messagebox.showerror("ERROR", f"Error checking payment: {str(e)}")

        finally:
            session.close()

    def make_payment(self):
        """Handles the payment process for a vehicle."""
        plate_number = self.payment_plate_number_entry.get().strip()
        payment_amount = self.payment_amount.get().strip()

        if not plate_number or not payment_amount:
            return messagebox.showwarning("WARNING", "Please enter both the vehicle plate number and payment amount.")

        try:
            try:
                payment_amount = float(payment_amount)
                if payment_amount <= 0:
                    raise ValueError("The payment amount must be greater than zero.")
            except ValueError as ve:
                return messagebox.showwarning("ERROR", f"Invalid payment amount entered. {str(ve)}")

            session = Session()

            parking_slot = session.query(ParkingSlot).join(Vehicle).filter(Vehicle.plate_number == plate_number).first()

            if not parking_slot or not parking_slot.entry_time or not parking_slot.exit_time:
                return messagebox.showwarning("ERROR", "Unable to retrieve required payment information. Ensure the vehicle is parked and has exit time recorded.")

            duration = parking_slot.exit_time - parking_slot.entry_time  
            total_minutes = duration.total_seconds() / 60  

            # Calculate required payment: rate * time in minutes
            parking_rate = 300  # Rate in TZS per minute
            required_payment = total_minutes * parking_rate

            # Verify if the entered payment amount matches or exceeds the required payment amount
            if payment_amount < required_payment and payment_amount > required_payment:
                return messagebox.showwarning("PAYMENT DISQUALIFIED", "required amount do not match. Try again.")
            
            # Check if the vehicle exists in the database
            vehicle = session.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
            if not vehicle:
                return messagebox.showwarning("ERROR", f"No vehicle found with plate number {plate_number}")

            # Create a new payment record
            new_payment = Payment(vehicle_id=vehicle.vehicle_id, payment_amount=payment_amount, is_paid=True)
            session.add(new_payment)
            
            # Commit the payment record to the database
            session.commit()

            # Check if the vehicle is assigned to a parking slot and delete the parking slot assignment
            if parking_slot:
                session.delete(parking_slot)  # Remove the parking slot assignment
                session.commit()

            # Refresh the payment table and show a success message
            self.refresh_payment_table()
            messagebox.showinfo("SUCCESS", f"Payment of {payment_amount} TZS has been successfully processed for vehicle {plate_number}.")
            
            # Clear the payment fields
            self.payment_plate_number_entry.delete(0, tk.END)
            self.payment_amount.delete(0, tk.END)

        except Exception as e:
            session.rollback()  # Rollback any changes in case of an error
            messagebox.showerror("ERROR", f"Error processing payment: {str(e)}")
        finally:
            session.close()

    def populate_payment_table(self):
        """Populates the payment details table with data from the database."""
        try:
            session = Session()
            
            # Query the Payment table and join with the Vehicle table to get plate numbers
            payment_records = session.query(Payment, Vehicle).join(Vehicle, Payment.vehicle_id == Vehicle.vehicle_id).all()

            # Clear existing rows in the treeview
            self.payment_tree.delete(*self.payment_tree.get_children())

            # Insert new rows into the treeview
            for idx, (payment, vehicle) in enumerate(payment_records, start=1):
                # Prepare data for each row
                payment_status = "Paid" if payment.is_paid else "Not Paid"
                self.payment_tree.insert("", "end", values=(
                    idx,
                    vehicle.plate_number,
                    payment.payment_amount,
                    payment_status
                ))

        except Exception as e:
            messagebox.showerror("ERROR", f"Error populating payment table: {str(e)}")
        finally:
            session.close()

    def refresh_payment_table(self):
        """Clears the table and repopulates it with fresh data."""
        self.payment_tree.delete(*self.payment_tree.get_children())  
        self.populate_payment_table()  
 
    def reserve_slot(self):
        """Reserves a parking slot for a customer."""
        email = self.reservation_email.get().strip()
        slot_name = self.reservation_slot.get().strip()

        if not email or not slot_name:
            return messagebox.showwarning("WARNING", "Please enter both the customer email and slot name.")

        try:
            session = Session()

            # Get the customer_id by querying the users table with email
            customer = session.query(User).filter(User.email == email).first()
            if not customer:
                return messagebox.showwarning("ERROR", f"No user found with email {email}. Please check and try again.")

            customer_id = customer.user_id

            # Get the slot_id by querying the ParkingSlot table with slot_name
            parking_slot = session.query(Slot).filter(Slot.slot_name == slot_name).first()
            if not parking_slot:
                return messagebox.showwarning("ERROR", f"No parking slot found with name {slot_name}. Please check and try again.")

            slot_id = parking_slot.slot_id
            session.query(Slot).filter(Slot.slot_id == slot_id).update({"is_reserved" :True})

            # Check if the customer already has a reservation for this slot
            existing_reservation = session.query(Reservation).filter(Reservation.customer_id == customer_id, Reservation.slot_id == slot_id).first()
            if existing_reservation:
                return messagebox.showwarning("ERROR", f"Slot {slot_name} is already reserved for {email}.")

            # Create a new reservation record
            reserved = session.query(Reservation).filter(Reservation.customer_id == customer_id).first()
            if reserved:
                session.delete(reserved)
                
            new_reservation = Reservation(customer_id=customer_id, slot_id=slot_id ,reservation_time= datetime.now())
            session.add(new_reservation)
            
            
            # Commit the reservation record
            session.commit()

            # Success message
            self.refresh_reservation_table()
            messagebox.showinfo("SUCCESS", f"Slot {slot_name} has been successfully reserved for {email}.")
            
            # Clear the form
            self.reservation_email.delete(0, tk.END)
            self.reservation_slot.delete(0, tk.END)

        except Exception as e:
            session.rollback()  # Rollback any changes in case of an error
            messagebox.showerror("ERROR", f"Error reserving slot: {str(e)}")
        finally:
            session.close()

    def populate_reservation_table(self):
        """Populates the reservation table with all existing reservations."""
        try:
            session = Session()
            reservations = session.query(Reservation).all()

            # Clear existing rows
            for row in self.reservation_tree.get_children():
                self.reservation_tree.delete(row)

            # Insert new rows for each reservation
            for idx, reservation in enumerate(reservations, start=1):
                user_id = reservation.customer_id  # Get user ID
                slot_id = reservation.slot_id  # Get parking slot ID

                # Query the User and ParkingSlot tables for their details
                user = session.query(User).filter(User.user_id == user_id).first()
                parking_slot = session.query(Slot).filter(Slot.slot_id == slot_id).first()

                if user and parking_slot:
                    user_email = user.email  # Get the user's email
                    slot_name = parking_slot.slot_name  # Get the slot name
                    self.reservation_tree.insert("", "end", values=(idx, user_email, slot_name))
                else:
                    # Handle cases where user or parking slot might be missing
                    self.reservation_tree.insert("", "end", values=(idx, "Unknown", "Unknown"))

        except Exception as e:
            messagebox.showerror("ERROR", f"Error loading reservations: {str(e)}")
        finally:
            session.close()

    def refresh_reservation_table(self):
        """Refreshes the reservation table with updated data."""
        try:
            # Query the database to get all reservation data
            session = Session()
            reservations = session.query(Reservation).all()

            # Clear existing rows in the reservation table
            for row in self.reservation_tree.get_children():
                self.reservation_tree.delete(row)

            # Insert new rows for each reservation record
            for idx, reservation in enumerate(reservations, start=1):
                user_id = reservation.customer_id  
                slot_id = reservation.slot_id  
                
                user = session.query(User).filter(User.user_id == user_id).first()
                parking_slot = session.query(Slot).filter(Slot.slot_id == slot_id).first()

                if user and parking_slot:
                    user_email = user.email 
                    slot_name = parking_slot.slot_name 
                    self.reservation_tree.insert("", "end", values=(idx, user_email, slot_name,))
                else:
                    self.reservation_tree.insert("", "end", values=(idx, "Unknown", "Unknown",))

        except Exception as e:
            messagebox.showerror("ERROR", f"Error refreshing reservation table: {str(e)}")
        finally:
            session.close()
    
    def release_reservation(self):
        session = Session()
        slot_name_field = self.reservation_check.get()
        
        if not slot_name_field:
            return messagebox.showwarning('WARNING' , 'Please provide the slot name')

        try:
            # Fetch the slot record
            slot = session.query(Slot).filter(Slot.slot_name == slot_name_field).first()

            if not slot:
                messagebox.showerror("Error", f"No slot found with name '{slot_name_field}'.")
                return

            reservation = (
                session.query(Reservation)
                .join(Slot, Reservation.slot_id == Slot.slot_id)
                .filter( Slot.slot_id == slot.slot_id)
                .first() 
            )

            if not reservation:
                messagebox.showerror("Error", f"No active reservation found for slot '{slot_name_field}'.")
                return

            # Fetch the slot record
            slot = session.query(Slot).filter(Slot.slot_name == slot_name_field).first()

            if not slot:
                messagebox.showerror("Error", f"No slot found with name '{slot_name_field}'.")
                return

            # Update the Slot table: set is_reserved to False
            slot.is_reserved = False

            # Update the Reservation table: set slot_id to None and update release_time
            reservation.slot_id = None
            reservation.released_time = datetime.now()

            # Commit changes to the database
            session.commit()
            self.refresh_reservation_table()
            messagebox.showinfo("SUCCESS", f"Reservation for slot '{slot_name_field}' released successfully.")

        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"An error occurred while releasing the reservation: {str(e)}")
        finally:
            session.close()

    def get_reserved_slots(self):
        """Fetches all the reserved parking slots."""
        try:
            session = Session()

            # Query the Slot table for reserved slots
            reserved_slots = session.query(Slot).filter(Slot.is_reserved == True).all()

            # Prepare a list of reserved slot names
            reserved_slot_names = [slot.slot_name for slot in reserved_slots]

            return reserved_slot_names

        except Exception as e:
            messagebox.showerror("ERROR", f"Error fetching reserved slots: {str(e)}")
            return []

        finally:
            session.close()
    
    def show_reservations(self):
        """Displays the Reservations management frame."""
        reservations_frame = tk.Frame(self.root, bg="#f2f2f2", padx=20, pady=20)
        
        # Configure the root window to allow the reservations frame to expand
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)  

        # Configure the reservations frame to fill the available space
        reservations_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure the frame's internal grid to make sure it stretches
        reservations_frame.grid_rowconfigure(0, weight=0) 
        reservations_frame.grid_rowconfigure(1, weight=1) 
        reservations_frame.grid_rowconfigure(2, weight=5)  
        reservations_frame.grid_columnconfigure(0, weight=1) 

        
        label = tk.Label(reservations_frame, text="Manage Reservations", font=FONT, fg=MAIN_COLOR ,pady=10)
        label.grid(row=0, column=0 , columnspan=2,  sticky="we" )
        
        # Reservation Form
        forms_frame = tk.Frame(reservations_frame, bg="#ffffff", bd=2 , relief="raised" ,padx=10 , pady=10)
        forms_frame.grid(row=1, column=0, padx=10, pady=20, sticky="n")

        # Reservation Form Label
        reservation_label = tk.Label(forms_frame, text="Reserve Parking Slot", font=FONT, bg="#ffffff", fg="#555555")
        reservation_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
         # Slot Name
        self.reservation=tk.Label(forms_frame, text="Slot Name:", font=("Arial", 12), bg="#ffffff")
        self.reservation.grid(row=1, column=0, pady=5, sticky="w")
        self.slots = self.get_reserved_slots()  
        self.reservation_check = ttk.Combobox(forms_frame, values=self.slots, state="readonly", width=30)
        self.reservation_check.grid(row=1, column=1, padx=10, pady=5)
        
        # Release Button
        self.reserve_button = tk.Button(
            forms_frame, text="Release Slot", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.release_reservation, width=20
        )
        self.reserve_button.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        # Customer Email
        self.reservation_email_label = tk.Label(forms_frame, text="Customer Email:", font=("Arial", 12), bg="#ffffff")
        self.reservation_email_label.grid(row=3, column=0,pady=5, sticky="w")
        self.reservation_email = tk.Entry(forms_frame, width=30)
        self.reservation_email.grid(row=3, column=1, padx=10, pady=5)

        
        # Slot Name
        self.reservation_slot_label = tk.Label(forms_frame, text="Slot Name:", font=("Arial", 12), bg="#ffffff")
        self.reservation_slot_label.grid(row=4, column=0, pady=5, sticky="w")
        self.slots = self.get_available_slots()  
        self.reservation_slot = ttk.Combobox(forms_frame, values=self.slots, state="readonly", width=30)
        self.reservation_slot.grid(row=4, column=1, padx=10, pady=5)
    

        # Reserve Button
        self.reserve_button = tk.Button(
            forms_frame, text="Reserve Slot", fg="white", font=("Arial", 12, "bold"), bg=MAIN_COLOR,
            command=self.reserve_slot, width=20
        )
        self.reserve_button.grid(row=5, column=1, padx=10, pady=10, sticky="we")
        
        # Table Frame for Displaying Reserved Slots
        table_frame = tk.Frame(reservations_frame, bg="#f2f2f2", bd=3, relief="raised" ,pady=10 ,padx=10)
        table_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure the row and column to expand and fill the available space
        reservations_frame.grid_rowconfigure(1, weight=1, uniform="equal")
        reservations_frame.grid_columnconfigure(1, weight=1, uniform="equal")

        # Ensure the table_frame covers the full available space
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
                # Table Header
        columns = ("#", "email", "slot_name")
        self.reservation_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.reservation_tree.heading("#", text="#")
        self.reservation_tree.column("#", anchor="center", width=30)
        self.reservation_tree.heading("email", text="Customer Email")
        self.reservation_tree.column("email", anchor="w")
        self.reservation_tree.heading("slot_name", text="Slot Name")
        self.reservation_tree.column("slot_name", anchor="w")


        # Attach a Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.reservation_tree.yview)
        self.reservation_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.reservation_tree.pack(fill="both", expand=True)

        # Configure the parent frame to allow full width
        reservations_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        reservations_frame.grid_rowconfigure(0, weight=1)
        reservations_frame.grid_columnconfigure(0, weight=1)

        reservations_frame.grid_columnconfigure(0, weight=1) 
        self.populate_reservation_table()          
        self.show_frame(reservations_frame)