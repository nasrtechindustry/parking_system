import tkinter as tk
from config import MAIN_COLOR
from datetime import datetime
from views import SignUp, Login ,Dashboard

class SmartParkingApp:
    '''
        The main application entry point 
        This will be used to route over the whole application.
        It will contain different methods and data attributes to work with.
        
        @ ===> made by Nasr the Software developer
        
        @ ===> Email : nasrkihagila@gmail.com
        
        @ ===> Phone : +255 620 656 604
    '''
    def __init__(self, root):
        self.root = root
        self.login_view = Login(root=root, switch_to_signup=self.switch_to_signup)
        self.sign_up_view = SignUp(root=root, switch_to_login=self.switch_to_login)

        # Start with Login view shown
        self.login_view.show_frame()
        self.sign_up_view.hide_frame()

    def switch_to_signup(self):
        '''Switch to the Sign Up View'''
        self.login_view.hide_frame()  
        self.sign_up_view.show_frame() 
         
    def switch_to_login(self):
        '''Switch to the login view '''
        self.sign_up_view.hide_frame()  
        self.login_view.show_frame() 
         

def main():
    root = tk.Tk()
    root.title("SMART PARKING MANAGEMENT SYSTEM")
    
    screen_width = root.winfo_screenwidth() 
    screen_height = root.winfo_screenheight() 
    
    root.geometry(f"{screen_width}x{screen_height}")
    root.config(bg=MAIN_COLOR)
    
    app = SmartParkingApp(root)
    
    footer = tk.Label(
        root, 
        text=f"Developed by Group number one \n copyright @ {datetime.now().year} | All rights are reserved",
        padx=20,
        pady=20,
        fg="white"
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()
