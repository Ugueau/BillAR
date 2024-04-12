import cv2
import tkinter as tk
from PIL import Image, ImageTk
from Singleton.SingletonCache import SingletonCache
from Singleton.SingletonWindow import SingletonWindow
from constants.colors import *
from Model.Profil import Profil
from Model.Point import Point
from views.CalibrationProjecteurFrame import CalibrationProjecteurFrame
from views.ViewFrame import ViewFrame


class CalibrationCamFrame(ViewFrame):
    def __init__(self, old_frame: ViewFrame):
        self.window = SingletonWindow()
        self.frame = self.window.new_frame()
        self.frame.configure(bg=BACKGROUND)

        self.old_frame = old_frame
        self.size_drag = 20

        self.back_webcam_canvas = tk.Canvas(self.frame, bg=BACKGROUND, borderwidth=0, highlightthickness=0)
        self.back_webcam_canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.webcam_canvas = tk.Canvas(self.back_webcam_canvas, borderwidth=0, highlightthickness=0)
        self.webcam_canvas.pack()

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

        self.corner_selected: Point | None = None

        self.webcam_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.webcam_canvas.bind("<B1-Motion>", self.drag)
        self.webcam_canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.webcam_canvas.bind('<KeyPress>', self.on_key_press)
        self.webcam_canvas.focus_set()

        bt_annuler = tk.Button(self.frame, text="Annuler", bg=GREY, padx=20, pady=10,
                               command=self.cancel)
        bt_annuler.grid(row=1, column=0)

        bt_suivant = tk.Button(self.frame, text="Suivant", bg=LIGHT_BLUE, padx=20, pady=10,
                               command=self.next)
        bt_suivant.grid(row=1, column=1)

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

    def start_drag(self, event):
        ration_height = self.display_webcam_height / self.real_quality_webcam_height
        ration_width = self.display_webcam_width / self.real_quality_webcam_width
        x, y = event.x, event.y
        if self.point_top_left.x * ration_width < x < self.point_top_left.x * ration_width + self.size_drag and self.point_top_left.y * ration_height < y < self.point_top_left.y * ration_height + self.size_drag:
            self.is_dragging_top_left = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_top_left
        elif self.point_top_right.x * ration_width - self.size_drag < x < self.point_top_right.x * ration_width and self.point_top_right.y * ration_height < y < self.point_top_right.y * ration_height + self.size_drag:
            self.is_dragging_top_right = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_top_right
        elif self.point_bot_right.x * ration_width - self.size_drag < x < self.point_bot_right.x * ration_width and self.point_bot_right.y * ration_height - self.size_drag < y < self.point_bot_right.y * ration_height:
            self.is_dragging_bot_right = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_bot_right
        elif self.point_bot_left.x * ration_width < x < self.point_bot_left.x * ration_width + self.size_drag and self.point_bot_left.y * ration_height - self.size_drag < y < self.point_bot_left.y * ration_height:
            self.is_dragging_bot_left = True
            self.start_x, self.start_y = x, y
            self.corner_selected = self.point_bot_left
        elif self.point_top_left.x * ration_width < x < self.point_bot_right.x * ration_width and self.point_top_left.y * ration_height < y < self.point_bot_right.y * ration_height:
            self.is_dragging = True
            self.start_x, self.start_y = x, y

    def drag(self, event):
        ration_height = self.real_quality_webcam_height / self.display_webcam_height
        ration_width = self.real_quality_webcam_width / self.display_webcam_width
        dx, dy = event.x - self.start_x, event.y - self.start_y
        self.start_x, self.start_y = event.x, event.y
        dx = dx * ration_width
        dy = dy * ration_height

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

    def end_drag(self, event):
        self.is_dragging = False
        self.is_dragging_top_left = False
        self.is_dragging_top_right = False
        self.is_dragging_bot_right = False
        self.is_dragging_bot_left = False

    def move_corner(self, corner: Point, dx, dy):
        new_dx = corner.x + dx
        new_dy = corner.y + dy
        if (new_dx < 0 or new_dy < 0 or new_dx > self.real_quality_webcam_width or
                new_dy > self.real_quality_webcam_height):
            return
        corner.x = new_dx
        corner.y = new_dy
        self.draw_frame()

    def move_rectangle(self, dx, dy):
        if (min(self.point_top_left.x + dx, self.point_bot_left.x + dx) < 0 or
                min(self.point_top_left.y + dy, self.point_top_right.y + dy) < 0 or
                max(self.point_bot_right.x + dx > self.real_quality_webcam_width,
                    self.point_top_right.x + dx > self.real_quality_webcam_width) or
                max(self.point_bot_right.y + dy > self.real_quality_webcam_height,
                    self.point_bot_left.y + dy > self.real_quality_webcam_height)):
            return
        self.point_top_left.x += dx
        self.point_top_left.y += dy
        self.point_top_right.x += dx
        self.point_top_right.y += dy
        self.point_bot_right.x += dx
        self.point_bot_right.y += dy
        self.point_bot_left.x += dx
        self.point_bot_left.y += dy
        self.draw_frame()

    def draw_frame(self):
        ret, frame = self.vid.read()
        if ret:
            self.webcam_canvas.delete("all")

            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Redimensionnez l'image tout en conservant l'aspect ratio
            aspect_ratio = self.real_quality_webcam_width / self.real_quality_webcam_height
            if self.back_webcam_canvas.winfo_width() == 1 or self.back_webcam_canvas.winfo_height() == 1:
                return
            elif self.back_webcam_canvas.winfo_width() / aspect_ratio < self.back_webcam_canvas.winfo_height():
                self.display_webcam_width = self.back_webcam_canvas.winfo_width()
                self.display_webcam_height = int(self.back_webcam_canvas.winfo_width() / aspect_ratio)

            else:
                self.display_webcam_width = int(self.back_webcam_canvas.winfo_height() * aspect_ratio)
                self.display_webcam_height = self.back_webcam_canvas.winfo_height()

            resized_image = image.resize((self.display_webcam_width, self.display_webcam_height))
            self.webcam_canvas.config(width=self.display_webcam_width, height=self.display_webcam_height)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.webcam_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            ration_height = self.display_webcam_height / self.real_quality_webcam_height
            ration_width = self.display_webcam_width / self.real_quality_webcam_width

            self.webcam_canvas.create_polygon(self.point_top_left.x * ration_width,
                                              self.point_top_left.y * ration_height,
                                              self.point_top_right.x * ration_width,
                                              self.point_top_right.y * ration_height,
                                              self.point_bot_right.x * ration_width,
                                              self.point_bot_right.y * ration_height,
                                              self.point_bot_left.x * ration_width,
                                              self.point_bot_left.y * ration_height,
                                              outline="red", fill='', tags="rectangle", width=5)

            points = [self.point_top_left, self.point_top_right, self.point_bot_right, self.point_bot_left]

            for point in points:
                x = point.x * ration_width
                y = point.y * ration_height
                rect = (
                    x,
                    y,
                    x + self.size_drag if point in [self.point_top_left, self.point_bot_left] else x - self.size_drag,
                    y + self.size_drag if point in [self.point_top_left, self.point_top_right] else y - self.size_drag
                )

                outline_width = 5 if point == self.corner_selected else 0

                self.webcam_canvas.create_rectangle(rect, fill="yellow", width=outline_width, outline="black")

    def _update(self):
        self.draw_frame()
        self._update_id = self.back_webcam_canvas.after(100, self._update)

    def stop_update(self):
        # Annulez la fonction périodique
        self.back_webcam_canvas.after_cancel(self._update_id)

    def start_update(self):
        self.vid = cv2.VideoCapture(SingletonCache().index_web_cam_choice, cv2.CAP_DSHOW)

        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, -1)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, -1)

        self.real_quality_webcam_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.real_quality_webcam_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.display_webcam_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.display_webcam_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self._update()

    def set_frame(self):
        self.window.set_frame(self.frame)
        self.start_update()

    def cancel(self):
        self.vid.release()
        self.stop_update()
        self.old_frame.set_frame()

    def next(self):
        self.stop_update()
        self.vid.release()
        profile = Profil()
        profile.webcam_billard_coordonnees_top_left = self.point_top_left
        profile.webcam_billard_coordonnees_top_right = self.point_top_right
        profile.webcam_billard_coordonnees_bot_left = self.point_bot_left
        profile.webcam_billard_coordonnees_bot_right = self.point_bot_right
        CalibrationProjecteurFrame(self, self.old_frame, profile).set_frame()
