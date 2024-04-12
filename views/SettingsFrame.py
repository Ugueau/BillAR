from tkinter import messagebox
from tkinter.ttk import Combobox
from pygrabber.dshow_graph import FilterGraph
from views.CalibrationCamFrame import *

class SettingsFrame(ViewFrame):
    def __init__(self, old_frame: ViewFrame):
        self.window = SingletonWindow()
        self.frame = self.window.new_frame()
        self.frame.configure(bg=BACKGROUND)
        self.old_frame = old_frame
        self.cameras = self.get_available_cameras()

    def update_frame(self):


        def generate_profil_canva(canva: tk.Canvas):

            profil_canva = tk.Canvas(canva)
            profil_canva.columnconfigure(1, weight=0)
            profil_canva.columnconfigure(2, weight=0)
            profil_canva.grid(row=0, column=3)

            title = tk.Label(profil_canva, text="Profil",padx=5, pady=5)
            title.grid(row=0, column=0, columnspan=3)

            # create the text widget
            text = tk.Text(profil_canva, height=10, width=20)
            text.grid(row=1, column=0, sticky=tk.EW)
            # create a scrollbar widget and set its command to the text widget
            scrollbar = tk.Scrollbar(profil_canva, orient='vertical', command=text.yview)
            scrollbar.grid(row=1, column=1, sticky=tk.NS)

            #  communicate back to the scrollbar
            text['yscrollcommand'] = scrollbar.set

            self.profils = Profil.charger_profils()

            # Ajout de texte au widget Text
            for i, profil in enumerate(self.profils, start=1):
                position = f'{i}.0'
                text.insert(position, f'{profil.nom}\n')
            text.configure(state='disabled')

            def on_button_add_profil():
                CalibrationCamFrame(self).set_frame()

            # Chargement de l'image de l'icône +
            image_plus = Image.open(
                "resources/add.png")  # Remplacez "plus_icon.png" par le chemin de votre propre image
            image_plus = image_plus.resize((50, 50), Image.ADAPTIVE)
            icon_plus = ImageTk.PhotoImage(image_plus)
            # Création du bouton avec l'icône +
            button_plus = tk.Button(profil_canva, image=icon_plus,bg=GREEN, command=on_button_add_profil)
            button_plus.image = icon_plus
            button_plus.grid(row=1, column=2)

            nom_profil=[]
            for profil in self.profils:
                nom_profil.append(profil.nom)
            # Création de la combobox avec les noms des webcams
            profil_del_combobox = Combobox(profil_canva, values=nom_profil, state="readonly")
            profil_del_combobox.grid(row=2, column=0,columnspan=2, padx=10, pady=10)
            profil_del_combobox.set("Sélectionnez un profil")

            def on_click_button_delete():
                index = profil_del_combobox.current()
                if index != -1:
                    Profil.delete_profils(index)
                    self.old_frame.set_frame()
                else:
                    messagebox.showerror("Erreur", "Veuillez sélectionner un profil")

            image_bin = Image.open(
                "resources/bin.png")  # Remplacez "plus_icon.png" par le chemin de votre propre image
            image_bin = image_bin.resize((50, 50), Image.ADAPTIVE)
            icon_bin = ImageTk.PhotoImage(image_bin)
            # Création du bouton avec l'icône +
            button_bin = tk.Button(profil_canva, image=icon_bin,bg=RED,command=on_click_button_delete)
            button_bin.image = icon_bin
            button_bin.grid(row=2, column=2)


        def generate_webcam_canva(canva: tk.Canvas):

            webcam_canva = tk.Canvas(canva)
            webcam_canva.grid(row=0, column=0)

            title = tk.Label(webcam_canva, text="WebCam",padx=5, pady=5)
            title.grid(row=0, column=0, columnspan=1)

            # Création de la combobox avec les noms des webcams
            camera_combobox = Combobox(webcam_canva, values=list(self.cameras.values()), state="readonly")
            camera_combobox.grid(row=1, column=0, padx=10, pady=10)
            camera_combobox.set("Sélectionnez une webcam")

            def on_camera_selected(event):
                SingletonCache().index_web_cam_choice = list(self.cameras.keys())[camera_combobox.current()]

            camera_combobox.bind("<<ComboboxSelected>>", on_camera_selected)

            if len(self.cameras) > 0:
                camera_combobox.current(SingletonCache().index_web_cam_choice)



        def on_bt_retour_click():
            self.old_frame.set_frame()

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Création du bouton "Annuler" avec des coins arrondis et placé sur le Canvas
        bt_retour = tk.Button(self.frame, text="Retour", bg=LIGHT_BLUE, padx=20, pady=10,
                            command=on_bt_retour_click)
        bt_retour.grid(row=1, column=0)

        canva_back = tk.Canvas(self.frame, bg=BACKGROUND)
        canva_back.grid(row=0, column=0)

        generate_webcam_canva(canva_back)

        generate_profil_canva(canva_back)
    def get_available_cameras(self):
        devices = FilterGraph().get_input_devices()

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_index] = device_name

        return available_cameras
    def set_frame(self):
        self.update_frame()
        self.cameras = self.get_available_cameras()
        self.window.set_frame(self.frame)
