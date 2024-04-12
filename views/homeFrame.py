from tkinter import messagebox
from tkinter.ttk import Combobox
from Model.Profil import Profil
from Singleton.SingletonCache import SingletonCache
from Singleton.SingletonWindow import SingletonWindow
from constants.colors import *
from views.CalibrationCamFrame import CalibrationCamFrame
from views.GameFrame import GameFrame
from views.SettingsFrame import SettingsFrame
import tkinter as tk
from views.ViewFrame import ViewFrame
from PIL import Image, ImageTk
from pygrabber.dshow_graph import FilterGraph

class HomeFrame(ViewFrame):
    def __init__(self):
        self.window = SingletonWindow()
        self.frame = self.window.new_frame()
        self.frame.configure(bg=BACKGROUND)
        self.pictureSrc = "resources/app_logo.png"

        # Fonctions pour gérer les événements de clic
        def on_bt_jouer_click():
            print("Bouton jouer cliqué")
            afficher_popup_choice_profil()

        def on_bt_leave_click():
            self.window.quit_application()
        def on_bt_options_click():
            SettingsFrame(self).set_frame()

        def afficher_popup_choice_profil():
            self.cameras = self.get_available_cameras()
            popup_canvas = tk.Canvas(self.frame, bg=BACKGROUND)
            popup_canvas.grid(row=0, column=0, columnspan=12, rowspan=3)

            title = tk.Label(popup_canvas, text="WebCam", padx=5, pady=5, bg=BACKGROUND, fg=FORGROUND)
            title.grid(row=0, column=0, columnspan=4)

            # Création de la combobox avec les noms des webcams
            camera_combobox = Combobox(popup_canvas, values=list(self.cameras.values()), state="readonly")
            camera_combobox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
            camera_combobox.set("Sélectionnez une webcam")

            def on_camera_selected(event):
                SingletonCache().index_web_cam_choice = list(self.cameras.keys())[camera_combobox.current()]

            camera_combobox.bind("<<ComboboxSelected>>", on_camera_selected)

            if len(self.cameras) > 0:
                camera_combobox.current(SingletonCache().index_web_cam_choice)

            label = tk.Label(popup_canvas, text="Choix du Profil", bg=BACKGROUND, fg=FORGROUND)
            label.grid(row=2, column=0, columnspan=4, pady=10, padx=10)
            profils = Profil.charger_profils()

            # Création de la combobox avec les noms des webcams
            profils_combobox = Combobox(popup_canvas, values=[profil.nom for profil in profils], state="readonly")
            profils_combobox.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
            profils_combobox.set("Sélectionnez un profil")

            def on_button_add_profil():
                CalibrationCamFrame(self).set_frame()
                popup_canvas.destroy()

            # Chargement de l'image de l'icône +
            image_plus = Image.open(
                "resources/add.png")  # Remplacez "plus_icon.png" par le chemin de votre propre image
            image_plus = image_plus.resize((20, 20), Image.ADAPTIVE)
            icon_plus = ImageTk.PhotoImage(image_plus)
            # Création du bouton avec l'icône +
            button_plus = tk.Button(popup_canvas, image=icon_plus,bg=GREEN, command=on_button_add_profil)
            button_plus.image = icon_plus
            button_plus.grid(row=3, column=3, pady=10, padx=10)

            def on_click_button_ok():
                index = profils_combobox.current()
                if index != -1:
                    SingletonCache().profil = profils[index]
                    popup_canvas.destroy()
                    GameFrame(self).set_frame()
                else:
                    messagebox.showerror("Erreur", "Veuillez sélectionner un profil")

            def on_click_button_cancel():
                popup_canvas.destroy()

            bouton_cancel = tk.Button(popup_canvas, text="annuler", command=on_click_button_cancel, bg=GREY)
            bouton_cancel.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

            bouton_ok = tk.Button(popup_canvas, text="OK", command=on_click_button_ok, bg=LIGHT_BLUE)
            bouton_ok.grid(row=4, column=2, columnspan=2, pady=10, padx=10)

        # Configurer la grille pour occuper toute la fenêtre avec 12 colonnes
        for i in range(12):
            self.frame.grid_columnconfigure(i, weight=1)

        # Configurer la grille pour occuper toute la fenêtre avec 3 lignes
        self.frame.grid_rowconfigure(0, weight=1)  # Pour l'image
        self.frame.grid_rowconfigure(1, weight=0)  # Pour les boutons (taille fixe)
        self.frame.grid_rowconfigure(2, weight=0)  # Pour les boutons (taille fixe)

        # Ajouter une image avec une marge supérieure en utilisant grid
        # image = Image.open(self.pictureSrc)
        # image = image.resize((500, 500), Image.ADAPTIVE)
        # image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.frame, width=500, height=500, bg=BACKGROUND)
        self.image_label.grid(row=0, column=0, columnspan=12, pady=50, sticky="nsew")
        self.update_image_label()

        self.image_label.bind("<Configure>", self.update_image_label)

        # Ajouter les boutons avec espace entre eux en utilisant grid
        bt_jouer = tk.Button(self.frame, text="Jouer", bg=LIGHT_BLUE, padx=20, pady=10, command=on_bt_jouer_click)
        bt_jouer.grid(row=1, column=5, sticky="nsew", pady=(0, 10))  # Utiliser pady pour ajouter de l'espace en bas
        bt_options = tk.Button(self.frame, text="Options", bg=LIGHT_BLUE, padx=20, pady=10, command=on_bt_options_click)
        bt_options.grid(row=1, column=6, sticky="nsew", pady=(0, 10))  # Utiliser pady pour ajouter de l'espace en bas
        bt_leave = tk.Button(self.frame, text="Quitter", bg=LIGHT_BLUE, padx=20, pady=10, command=on_bt_leave_click)
        bt_leave.grid(row=2, column=5, columnspan=2, sticky="nsew")

    def update_image_label(self, event=None):
        image = Image.open(self.pictureSrc)

        width = image.width
        height = image.height
        display_webcam_width = width
        display_webcam_height = height

        # Redimensionnez l'image tout en conservant l'aspect ratio
        aspect_ratio = width / height
        if self.image_label.winfo_width() / aspect_ratio < self.image_label.winfo_height():
            display_webcam_width = self.image_label.winfo_width()
            display_webcam_height = int(self.image_label.winfo_width() / aspect_ratio)

        else:
            display_webcam_width = int(self.image_label.winfo_height() * aspect_ratio)
            display_webcam_height = self.image_label.winfo_height()


        image = image.resize((display_webcam_width, display_webcam_height), Image.ADAPTIVE)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def get_available_cameras(self):
        devices = FilterGraph().get_input_devices()

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name

        return available_cameras

    def set_frame(self):
        self.window.set_frame(self.frame)
