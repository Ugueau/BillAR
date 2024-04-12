from Model.Profil import Profil

class SingletonCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._index_web_cam_choice = 0
            cls._instance.index_web_cam_choice_tmp = 0
            cls._instance._profil=None

        return cls._instance

    @property
    def index_web_cam_choice(self) -> int:
        return self._index_web_cam_choice

    @index_web_cam_choice.setter
    def index_web_cam_choice(self, index_web_cam_choice: int) -> None:
        if not isinstance(index_web_cam_choice, int):
            raise ValueError("Le indexWebCamChoice doit être un int.")
        self._index_web_cam_choice = index_web_cam_choice

    @property
    def profil(self) -> Profil:
        return self._profil

    @profil.setter
    def profil(self, profil: Profil) -> None:
        if not isinstance(profil, Profil):
            raise ValueError("Le profil doit être un Profil.")
        self._profil = profil
