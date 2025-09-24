import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class LoginView:
    def __init__(self, controller):
        self.controller = controller
        self.window = ttk.Window(themename="superhero")
        self.window.title("SIAT-Lite - Iniciar Sesión")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        """Configurar interfaz de login"""
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        # Logo/Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=X, pady=(0, 30))

        ttk.Label(title_frame, text="🚗", font=("Arial", 48)).pack()
        ttk.Label(title_frame, text="SIAT-Lite",
                  font=("Arial", 24, "bold"), bootstyle="primary").pack()
        ttk.Label(title_frame, text="Sistema de Información de Accidentes de Tránsito",
                  font=("Arial", 10), bootstyle="secondary").pack()

        # Formulario de login
        login_frame = ttk.LabelFrame(main_frame, text="🔐 Iniciar Sesión", bootstyle="primary")
        login_frame.pack(fill=X, pady=20)

        # Email
        ttk.Label(login_frame, text="Correo Electrónico:").pack(anchor=W, padx=15, pady=(15, 5))
        self.email_entry = ttk.Entry(login_frame, font=("Arial", 11))
        self.email_entry.pack(fill=X, padx=15, pady=(0, 10))

        # Contraseña
        ttk.Label(login_frame, text="Contraseña:").pack(anchor=W, padx=15, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", font=("Arial", 11))
        self.password_entry.pack(fill=X, padx=15, pady=(0, 15))

        # Recordar usuario
        self.recordar_var = ttk.BooleanVar()
        ttk.Checkbutton(login_frame, text="Recordar usuario",
                        variable=self.recordar_var, bootstyle="primary").pack(anchor=W, padx=15, pady=(0, 15))

        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=X, pady=20)

        ttk.Button(botones_frame, text="🔓 Iniciar Sesión",
                   bootstyle="primary", command=self.login).pack(fill=X, pady=(0, 10))

        ttk.Button(botones_frame, text="❓ ¿Olvidó su contraseña?",
                   bootstyle="link", command=self.recuperar_password).pack()

        # Información del sistema
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(side=BOTTOM, fill=X, pady=(30, 0))

        ttk.Label(info_frame, text="SIAT-Lite v1.0 - Desarrollado para Seguridad Vial",
                  font=("Arial", 8), bootstyle="secondary").pack()

        # Eventos
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        """Procesar inicio de sesión"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            Messagebox.show_warning("Advertencia", "Complete todos los campos")
            return

        # Enviar al controlador
        if self.controller.autenticar_usuario(email, password):
            self.window.destroy()
        else:
            Messagebox.show_error("Error", "Credenciales incorrectas")
            self.password_entry.delete(0, END)
            self.password_entry.focus()

    def recuperar_password(self):
        """Mostrar diálogo de recuperación de contraseña"""
        Messagebox.show_info("Recuperar Contraseña",
                             "Contacte al administrador del sistema para recuperar su contraseña.")

    def show(self):
        """Mostrar ventana de login"""
        self.window.mainloop()