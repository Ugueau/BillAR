from tkinter import messagebox
from Model.Point import Point
from Model.Profil import Profil
from Singleton.SingletonWindow import SingletonWindow
from constants.colors import *
from views.ViewFrame import ViewFrame
import tkinter as tk

class CalibrationProjecteurFrame(ViewFrame):
    @staticmethod
    def get_size_drag_zone():
        return 20
    def set_frame(self):
        self.window.set_frame(self.frame)

    def __init__(self, old_frame: ViewFrame, home_frame: ViewFrame, profil: Profil):
        self.old_frame = old_frame
        self.home_frame = home_frame
        self.window = SingletonWindow()
        self.frame = self.window.new_frame()
        self.frame.configure(bg=BACKGROUND)
        self.profil = profil

        self.size_drag = 20
        self.corner_selected: Point | None = None

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.point_top_left = Point(0, 0)
        self.point_top_right = Point(150, 0)
        self.point_bot_left = Point(0, 150)
        self.point_bot_right = Point(150, 150)

        self.is_dragging = False
        self.is_dragging_top_left = False
        self.is_dragging_top_right = False
        self.is_dragging_bot_right = False
        self.is_dragging_bot_left = False

        self.projecteur_canvas = tk.Canvas(self.frame, bg=BACKGROUND, highlightthickness=0)
        self.projecteur_canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        self.projecteur_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.projecteur_canvas.bind("<B1-Motion>", self.drag)
        self.projecteur_canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.projecteur_canvas.bind('<KeyPress>', self.on_key_press)
        self.projecteur_canvas.focus_set()

        bt_annuler = tk.Button(self.frame, text="Annuler", bg=GREY, padx=20, pady=10,
                               command=self.cancel)
        bt_annuler.grid(row=1, column=0)

        bt_suivant = tk.Button(self.frame, text="Suivant", bg=LIGHT_BLUE, padx=20, pady=10,
                               command=self.next)
        bt_suivant.grid(row=1, column=1)

        # Create the initial rectangle on the canvas
        self.draw_rectangle()
    def on_key_press(self, event):
        if self.corner_selected is not None:
            if event.keysym == 'Up':
                self.move_corner(self.corner_selected, 0, -1)
            elif event.keysym == 'Down':
                self.move_corner(self.corner_selected, 0, 1)
            elif event.keysym == 'Left':
                self.move_corner(self.corner_selected, -1, 0)
            elif event.keysym == 'Right':
                self.move_corner(self.corner_selected, 1, 0)
            self.draw_rectangle()
    def draw_rectangle(self):
        self.projecteur_canvas.delete("rectangle")  # Clear previous rectangles

        self.projecteur_canvas.create_polygon(self.point_top_left.x, self.point_top_left.y,
                                              self.point_top_right.x, self.point_top_right.y,
                                              self.point_bot_right.x, self.point_bot_right.y,
                                              self.point_bot_left.x, self.point_bot_left.y,
                                              fill="blue", tags="rectangle")
        points = [self.point_top_left, self.point_top_right, self.point_bot_right, self.point_bot_left]

        for point in points:
            x = point.x
            y = point.y
            rect = (
                x,
                y,
                x + self.size_drag if point in [self.point_top_left, self.point_bot_left] else x - self.size_drag,
                y + self.size_drag if point in [self.point_top_left, self.point_top_right] else y - self.size_drag
            )

            outline_width = 5 if point == self.corner_selected else 0

            self.projecteur_canvas.create_rectangle(rect, fill="yellow", width=outline_width, tags="rectangle", outline="black")


    def start_drag(self, event):
        x, y = event.x, event.y
        if self.point_top_left.x < x < self.point_top_left.x + self.size_drag and self.point_top_left.y < y < self.point_top_left.y + self.size_drag:
            self.is_dragging_top_left = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_top_left
        elif self.point_top_right.x - self.size_drag < x < self.point_top_right.x and self.point_top_right.y < y < self.point_top_right.y + self.size_drag:
            self.is_dragging_top_right = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_top_right
        elif self.point_bot_right.x - self.size_drag < x < self.point_bot_right.x and self.point_bot_right.y - self.size_drag < y < self.point_bot_right.y:
            self.is_dragging_bot_right = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_bot_right
        elif self.point_bot_left.x < x < self.point_bot_left.x + self.size_drag and self.point_bot_left.y - self.size_drag < y < self.point_bot_left.y:
            self.is_dragging_bot_left = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_bot_left
        elif self.point_top_left.x < x < self.point_bot_right.x and self.point_top_left.y < y < self.point_bot_right.y:
            self.is_dragging = True
            self.start_x, self.start_y = x, y

        self.draw_rectangle()

    def drag(self, event):
        dx, dy = event.x - self.start_x, event.y - self.start_y
        self.start_x, self.start_y = event.x, event.y
        if self.is_dragging:
            self.move_rectangle(dx, dy)
        elif self.is_dragging_top_left:
            self.move_corner(self.point_top_left, dx, dy)
        elif self.is_dragging_top_right:
            self.move_corner(self.point_top_right, dx, dy)
        elif self.is_dragging_bot_right:
            self.move_corner(self.point_bot_right, dx, dy)
        elif self.is_dragging_bot_left:
            self.move_corner(self.point_bot_left, dx, dy)

        self.draw_rectangle()

    def end_drag(self, event):
        self.is_dragging = False
        self.is_dragging_top_left = False
        self.is_dragging_top_right = False
        self.is_dragging_bot_right = False
        self.is_dragging_bot_left = False

    def move_corner(self, corner: Point, dx, dy):
        new_dx = corner.x + dx
        new_dy = corner.y + dy
        if (new_dx < 0 or new_dy < 0 or new_dx > self.projecteur_canvas.winfo_width() or
                new_dy > self.projecteur_canvas.winfo_height()):
           return
        corner.x = new_dx
        corner.y = new_dy

    def move_rectangle(self, dx, dy):
        if (min(self.point_top_left.x + dx,self.point_bot_left.x + dx) < 0 or
                min(self.point_top_left.y + dy,self.point_top_right.y + dy) < 0 or
                max(self.point_bot_right.x + dx > self.projecteur_canvas.winfo_width(),self.point_top_right.x + dx > self.projecteur_canvas.winfo_width()) or
                max(self.point_bot_right.y + dy > self.projecteur_canvas.winfo_height(),self.point_bot_left.y + dy > self.projecteur_canvas.winfo_height())):
            return
        self.point_top_left.x += dx
        self.point_top_left.y += dy
        self.point_top_right.x += dx
        self.point_top_right.y += dy
        self.point_bot_right.x += dx
        self.point_bot_right.y += dy
        self.point_bot_left.x += dx
        self.point_bot_left.y += dy

    def cancel(self):
        self.old_frame.set_frame()

    def next(self):
        self.profil.projecteur_billard_coordonnees_top_left = self.point_top_left
        self.profil.projecteur_billard_coordonnees_top_right = self.point_top_right
        self.profil.projecteur_billard_coordonnees_bot_right = self.point_bot_right
        self.profil.projecteur_billard_coordonnees_bot_left = self.point_bot_left
        self.afficher_popup_choice_profil()

    def afficher_popup_choice_profil(self):
        popup_canvas = tk.Canvas(self.frame, bg=BACKGROUND)
        popup_canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

        label = tk.Label(popup_canvas, text="Choix du nom du Profil", bg=BACKGROUND, fg=FORGROUND)
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Création de la combobox avec les noms des webcams
        name_profil = tk.Entry(popup_canvas)
        name_profil.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        def on_click_button_enregistrer():
            name_ask = name_profil.get()
            if name_ask != "":
                popup_canvas.destroy()
                self.profil.nom = name_ask
                Profil.sauvegarder_profils(self.profil)
                self.home_frame.set_frame()
            else:
                messagebox.showerror("Erreur", "Veuillez entrer un nom de profil")

        def on_click_button_cancel():
            popup_canvas.destroy()

        bouton_cancel = tk.Button(popup_canvas, text="annuler", command=on_click_button_cancel, bg=GREY)
        bouton_cancel.grid(row=2, column=0, pady=10, padx=10)

        bouton_enregistrer = tk.Button(popup_canvas, text="Enregistrer", command=on_click_button_enregistrer,
                                       bg=LIGHT_BLUE)
        bouton_enregistrer.grid(row=2, column=1, pady=10, padx=10)
