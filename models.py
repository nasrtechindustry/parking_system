import sqlalchemy as sm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker , relationship
import uuid
import os
from datetime import datetime

Base = declarative_base()
db = "pms.db"
db_name = f"sqlite:///{db}"
engine = sm.create_engine(db_name)

Session = sessionmaker(bind=engine)

class Response:
    def success_response(self, message , data = {}):
        return {
            'success' : True,
            'message' : message,
            'data' : data
        }
    def error_response(self, message , data = {}):
        return {
            'success' : False,
            'message' : message,
            'data' : data
        }
        
class User(Base , Response):
    __tablename__ = "users"
    user_id = sm.Column("user_id", sm.String(36), primary_key=True, default=lambda: str(uuid.uuid1()))
    first_name = sm.Column("first_name", sm.String(255), nullable=False)
    last_name = sm.Column("last_name", sm.String(255), nullable=False)
    email = sm.Column("email", sm.String(255), nullable=False, unique=True)
    role = sm.Column("role", sm.Enum("admin", "operator" , 'customer'), default="operator")
    password = sm.Column("password", sm.String(255), nullable=False)

    def __init__(self, first_name= None, last_name = None, email =None, role="operator" , password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower() if email else None
        self.role = role
        self.password = password
        self.session = Session()

    def __str__(self):
        return f"I am {self.first_name} {self.last_name}, my email is {self.email}"

    def register(self):
        """Registers a new user."""
        session = Session()
        try:
            user = session.query(User).filter_by(email=self.email).first()
            if user:
                return "Email Was found.. try again"
            self.session.add(self)
            self.session.commit()
            return "User created successfully."
        except Exception as e:
            self.session.rollback()
            return f"Error: {str(e)}"

    @classmethod
    def login(cls, email, password):
        """Validates user credentials and returns user data if valid."""
        session = Session()
        try:
            # Fetch the user from the database
            user = session.query(cls).filter_by(email=email).first()
            if user and user.password == password:
                # Return user data if credentials are valid
                data =  {
                    "id": user.user_id,
                    "email": user.email,
                    "role": user.role, 
                }
                
                return cls.success_response('logged in successully' , data=data)
            else:
                return {"error": "Invalid email or password."}
        except Exception as e:
            return {"error": str(e)}  # Return any exception message for debugging
        finally:
            session.close()


    def logout(self):
        """Logs out the user."""
        return "User logged out successfully."

    def view_profile(self, user_id):
        """Fetches the profile of the specified user."""
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            return {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
            }
        return "User not found."

    def add_slot(self, slot_name, created_by):
        """Adds a new parking slot."""
        slot = Slot(slot_name=slot_name, created_by=created_by)
        try:
            self.session.add(slot)
            self.session.commit()
            return "Slot added successfully."
        except Exception as e:
            self.session.rollback()
            return f"Error: {str(e)}"

    def reserve_slot(self, customer_id, slot_id):
        """Reserves a parking slot."""
        reservation = Reservation(customer_id=customer_id, slot_id=slot_id)
        try:
            self.session.add(reservation)
            self.session.commit()
            return "Slot reserved successfully."
        except Exception as e:
            self.session.rollback()
            return f"Error: {str(e)}"

    
    def make_payment(self, vehicle_id, payment_amount):
        """Records a payment."""
        payment = Payment(vehicle_id=vehicle_id, payment_amount=payment_amount)
        try:
            self.session.add(payment)
            self.session.commit()
            return "Payment recorded successfully."
        except Exception as e:
            self.session.rollback()
            return f"Error: {str(e)}"

class Slot(Base ,Response):
    __tablename__ = "slots"
    slot_id = sm.Column("slot_id" ,sm.String(36)  ,primary_key=True, default=lambda :str(uuid.uuid1()))
    slot_name = sm.Column('slot_name' , sm.String(100) ,nullable=False)
    is_occupied = sm.Column('is_occupied' , sm.Boolean() , default=False)
    is_reserved = sm.Column('is_reserved' , sm.Boolean() , default=False)
    created_by = sm.Column('created_by' , sm.String(36) , sm.ForeignKey(User.user_id) , nullable=True)
    
    def create_slot(self, slot_name):
        """Create a new parking slot in the database."""
        session = Session()  # Create a session for the database
        try:
            # Check if the slot already exists
            existing_slot = session.query(Slot).filter_by(slot_name=slot_name).first()
            if existing_slot:

                return  self.error_response(f"Slot '{slot_name}' already exists.")

            # Create a new slot
            new_slot = Slot(slot_name=slot_name)
            session.add(new_slot)  # Add to the database session
            session.commit()  # Commit the changes
            return self.success_response(f"Slot '{slot_name}' has been created successfully.")
        except SQLAlchemyError as e:
            session.rollback()  # Rollback in case of an error
            return  self.error_response(f"An error occurred: {str(e)}")
            
        finally:
            session.close() 

class Customer(Base):
    __tablename__ = "customers"
    customer_id  = sm.Column('customer_id' , sm.String(36) , primary_key=True  , default=uuid.uuid1())
    first_name = sm.Column("first_name" , sm.String(255) , nullable=False)
    last_name = sm.Column("last_name" , sm.String(255) , nullable=False)
    email = sm.Column("email" , sm.String(255) , nullable=False ,unique=True)
    phone = sm.Column("phone" , sm.Integer() , nullable=True)
    password = sm.Column("password" , sm.String(255) , nullable=False)

class Vehicle(Base , Response):
    __tablename__ = "vehicles"
    vehicle_id = sm.Column('vehicle_id', sm.String(36) , primary_key=True, default=lambda: str(uuid.uuid1()))
    customer_id = sm.Column('customer_id' , sm.String(36) , sm.ForeignKey(Customer.customer_id) ,nullable=True)
    plate_number = sm.Column('plate_number' , sm.String(50) ,nullable=False)
    join_date = sm.Column('join_date' ,sm.DateTime() , default=datetime.now())
    
    
        
    def add_vehicle(self, customer_email, plate_number):
        """Registers a new vehicle for a customer."""
        session = Session()  # Create a new session
        try:
            # Query the database for the user with the given email
            customer = session.query(User).filter_by(email=customer_email).first()
            
            # Check if the customer exists and has the role 'customer'
            if not customer:
                return self.error_response("No customer Found with that email")
            
            # Add the vehicle for the customer
            vehicle = Vehicle(customer_id=customer.user_id, plate_number=plate_number)
            session.add(vehicle)
            session.commit()
            return self.success_response(f"Vehicle with plate number {plate_number} added successfully for customer {customer.last_name}.")
        
        except Exception as e:
            session.rollback()
            return self.error_response(f"Error: {str(e)}")
        finally:
            session.close()

    @classmethod
    def show_vehicles(cls):
        return Session().query(Vehicle).all()
        
class ParkingSlot(Base ,Response):
    __tablename__ = "parking_slots"
    parking_slot_id = sm.Column('parking_slot_id', sm.String(36), primary_key=True, default=lambda: str(uuid.uuid1()))
    slot_id = sm.Column("slot_id", sm.String(36), sm.ForeignKey(Slot.slot_id), nullable=True)
    vehicle_id = sm.Column("vehicle_id", sm.String(36), sm.ForeignKey(Vehicle.vehicle_id), nullable=True)
    entry_time = sm.Column('entry_time', sm.DateTime(), default=datetime.now())
    exit_time = sm.Column('exit_time', sm.DateTime(), nullable=True)
    
    slot = relationship("Slot", backref="parking_slots")
    vehicle = relationship("Vehicle", backref="parking_slots")
    
    def assign_slot_to_vehicle(self, plate_number, slot_name):
        session = Session()  
        try:
            # Step 1: Check if the vehicle exists
            vehicle = session.query(Vehicle).filter_by(plate_number=plate_number).first()
            if not vehicle:
                return self.error_response(f"No vehicle found with plate number {plate_number}.")

            # Step 2: Check if the slot exists and is not occupied
            slot = session.query(Slot).filter_by(slot_name=slot_name).first()
            if not slot:
                return self.error_response(f"No slot found with name {slot_name}.")
            
            if slot.is_occupied:
                return self.error_response(f"Slot '{slot_name}' is already occupied.")

            # Step 3: Assign the slot to the vehicle by inserting into the ParkingSlot table
            parking_slot = ParkingSlot(slot_id=slot.slot_id, vehicle_id=vehicle.vehicle_id, entry_time=datetime.now())
            session.add(parking_slot)
            
            # Step 4: Mark the slot as occupied
            slot.is_occupied = True  # Update the slot to mark it as occupied
            session.commit()  # Commit changes to the database
            
            return self.success_response(f"Vehicle with plate number {plate_number} has been assigned to slot '{slot_name}' successfully.")
        
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            return self.error_response(f"Error: {str(e)}")
        finally:
            session.close()
            
    def get_assigned_vehicles(self):
        session = Session()  # Create a new session
        try:
            # Query to fetch assigned vehicles with details about the slot and vehicle
            assigned_vehicles = session.query(ParkingSlot, Vehicle, Slot) \
                .join(Vehicle, Vehicle.vehicle_id == ParkingSlot.vehicle_id) \
                .join(Slot, Slot.slot_id == ParkingSlot.slot_id).all()
            
            # Prepare the result with relevant details
            assigned_vehicle_list = []
            for parking_slot, vehicle, slot in assigned_vehicles:
                assigned_vehicle_list.append({
                    "vehicle_plate_number": vehicle.plate_number,
                    "slot_name": slot.slot_name,
                    "entry_time": parking_slot.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "exit_time": parking_slot.exit_time.strftime("%Y-%m-%d %H:%M:%S") if parking_slot.exit_time else ''

                })
            
            return self.success_response( "ALL VEHICLES ARE HERE",data=assigned_vehicle_list)
        
        except Exception as e:
            return self.error_response(f"Error: {str(e)}")
        finally:
            session.close()

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = sm.Column('reservation_id', sm.String(36) , primary_key=True, default=uuid.uuid1())
    customer_id = sm.Column("customer_id" , sm.String(36) , sm.ForeignKey(Customer.customer_id) , nullable=True)
    slot_id = sm.Column("slot_id" , sm.String(36) , sm.ForeignKey(Slot.slot_id) , nullable=True)
    reservation_time = sm.Column('reservation_time' ,sm.DateTime() , default=datetime.now())
    released_time = sm.Column('released_time' ,sm.DateTime() , nullable=True)

class Payment(Base):
    __tablename__ = "payments"
    payment_id = sm.Column('payment_id', sm.String(36) , primary_key=True, default=lambda: str(uuid.uuid1()))
    vehicle_id = sm.Column("vehicle_id" , sm.String(36) , sm.ForeignKey(Vehicle.vehicle_id) , nullable=True)
    payment_amount = sm.Column('payment_amount' , sm.String() ,nullable=True)
    is_paid = sm.Column('is_paid' ,sm.Boolean() , default=False)

if not os.path.exists(db):
    
    Base.metadata.create_all(engine)
    print("database created successfully")
   


# print(ParkingSlot().get_assigned_vehicles())