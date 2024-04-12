import tkinter as tk

from constants.string import APP_NAME


class SingletonWindow:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SingletonWindow, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__instance.__initialized:
            return
        self.__instance.__initialized = True

        print("\n\n\n\n__________________________\n"
              "création SingletonWindow\n"
              "________________________\n\n\n\n")
        self.__instance.root = tk.Tk()
        self.__instance.window = self.__instance.root
        self.__instance.window.title(APP_NAME)
        self.__instance.window.attributes("-fullscreen", True)
        self.__instance.currentFrame = None

    def quit_application(self):
        self.__instance.root.quit()

    def new_frame(self):
        return tk.Frame(self.__instance.window)

    def set_frame(self, newFrame):
        if not isinstance(newFrame, tk.Frame):
            raise TypeError("newFrame must be an instance of tk.Frame")
        if self.__instance.currentFrame is not None:
            self.__instance.currentFrame.pack_forget()
        self.__instance.currentFrame = newFrame
        newFrame.pack(fill="both", expand=True)