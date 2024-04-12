from pydispatch import dispatcher
from outil.Acquisition import AcquisitionThread
from Model.EventYolo import EventYolo
from Singleton.SingletonWindow import SingletonWindow
from constants.EventConstants import ACQUISITION_KEY
from constants.colors import *
from views.ViewFrame import ViewFrame
import tkinter as tk
from tkinter import ttk
from outil.drawbillard import DrawBillard


class GameFrame(ViewFrame):
    def set_frame(self):
        self.window.set_frame(self.frame)

    def event_loading_model(self):
        print("Loading model...")
        self.popup_loading_canvas.destroy()
    def draw_object_singleton(self,event_yolo:EventYolo):
        # close loading if exist
        self.popup_loading_canvas.destroy()


        self.billard_canvas.delete(DrawBillard.TAGS_TRAJECTOIR)
        self.billard_canvas.delete(DrawBillard.TAGS_QUEUE)
        self.billard_canvas.delete(DrawBillard.TAGS_BILLE)

        for bille in event_yolo.ball_list:
            DrawBillard.draw_bille_outline(self.billard_canvas, bille, self.homographie, "green")
            DrawBillard.draw_bille_trajectoire(self.billard_canvas, bille, self.homographie, "green")
        for queue in event_yolo.cue_stick_list:
            DrawBillard.draw_queue(self.billard_canvas, queue, self.homographie)
            DrawBillard.draw_queue_trajectoire(self.billard_canvas, queue, self.homographie, "purple")

        if event_yolo.white_ball!=None:
            DrawBillard.draw_bille_fill(self.billard_canvas, event_yolo.white_ball, self.homographie, "white")
            DrawBillard.draw_bille_trajectoire(self.billard_canvas, event_yolo.white_ball, self.homographie, "white")

    def __init__(self,home_frame:ViewFrame):

        self.homographie = DrawBillard.trouver_homographie()
        self.home_frame = home_frame
        self.window = SingletonWindow()
        self.frame = self.window.new_frame()
        self.frame.configure(bg=BACKGROUND)
        self.loading = "resources/loading.gif"

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.billard_canvas = tk.Canvas(self.frame, bg=BACKGROUND, highlightthickness=0)
        self.billard_canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")

        bt_Menu = tk.Button(self.frame, text="Menu", bg=LIGHT_BLUE, padx=20, pady=10,
                               command=self.onClickMenu)
        bt_Menu.grid(row=1, column=1)

        self.popup_loading_canvas = tk.Canvas(self.frame, bg=BACKGROUND)
        self.popup_loading_canvas.grid(row=0, column=0, columnspan=1, rowspan=1)

        title_loading = tk.Label(self.popup_loading_canvas, text="Chargement", bg=BACKGROUND, fg=FORGROUND)
        title_loading.grid(row=0, column=0, pady=10, padx=10)

        pb = ttk.Progressbar(
            self.popup_loading_canvas,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        pb.grid(row=1, column=0, pady=10, padx=10)
        pb.start()

        def on_click_button_cancel():
            self.acquisition_thread.stop()
            self.home_frame.set_frame()

        bouton_cancel = tk.Button(self.popup_loading_canvas, text="annuler", command=on_click_button_cancel, bg=GREY)
        bouton_cancel.grid(row=2, column=0, pady=10, padx=10)

        # Create the initial rectangle on the canvas
        DrawBillard().draw_billard(self.billard_canvas)
        # Connecter la callback au signal
        dispatcher.connect(self.draw_object_singleton, signal=ACQUISITION_KEY)

        self.acquisition_thread = AcquisitionThread()

        # Démarrer le thread
        self.acquisition_thread.start()

    def onClickMenu(self):
        self.display_popup_menu()

    def display_popup_menu(self):
        popup_menu = tk.Canvas(self.frame, bg=BACKGROUND)
        popup_menu.grid(row=0, column=0, columnspan=2, rowspan=2)

        label = tk.Label(popup_menu, text="Menu du jeux", bg=BACKGROUND, fg=FORGROUND)
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=50)

        def on_click_button_leave():
            # Arrêtez le thread en appelant la méthode stop
            self.acquisition_thread.stop()
            # Attendez que le thread se termine

            self.home_frame.set_frame()

        def on_click_button_continuer():
            popup_menu.destroy()

        bouton_continuer = tk.Button(popup_menu, text="Continuer", command=on_click_button_continuer, bg=GREY)
        bouton_continuer.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        bouton_leave = tk.Button(popup_menu, text="Quitter", command=on_click_button_leave, bg=LIGHT_BLUE)
        bouton_leave.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
