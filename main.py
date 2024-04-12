import multiprocessing

import views.homeFrame

if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    window = views.homeFrame.SingletonWindow()

    views.homeFrame.HomeFrame().set_frame()

    window.window.mainloop()
