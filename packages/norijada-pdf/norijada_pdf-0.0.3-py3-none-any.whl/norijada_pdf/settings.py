from pathlib import Path
import os
import json


class Settings:

    def __init__(self):
        self.SETTINGS_FILE = Path(os.getcwd()) / "settings.json"

        self.ONE_POINT = 0.352777778
        self.PLOT_INCREMENT = 1
        self.PAGE_WIDTH = 500
        self.DEFAULT_FONT_SIZE = 150
        self.MAX_LENGTH = 240

        self.PROJECT_ROOT = Path(__file__).parent
        self.FONTS_DIR = self.PROJECT_ROOT / "fonts"

        self.PLOT_OUTPUT_DIR = Path(os.getcwd()) / "plots"
        Path.mkdir(self.PLOT_OUTPUT_DIR, exist_ok=True)

        self.PDF_OUTPUT_DIR = Path(os.getcwd()) / "pdf"
        Path.mkdir(self.PDF_OUTPUT_DIR, exist_ok=True)

        self.INPUT_FILE = Path(os.getcwd()) / "input.txt"

        self.FONT_SIZES = {
            "Bangers-Regular": 195,
            "BebasNeue-Regular": 195,
            "BerkshireSwash-Regular": 158,
            "BlackOpsOne-Regular": 139,
            "Bungee-Regular": 120,
            "Courgette-Regular": 156,
            "Galindo-Regular": 140,
            "KaushanScript-Regular": 167,
            "LibreBaskerville-Regular": 140,
            "Lobster-Regular": 172,
            "MouseMemoirs-Regular": 223,
            "Pacifico-Regular": 147,
            "PatrickHand-Regular": 190,
            "Ranchers-Regular": 170,
            "RubikMonoOne-Regular": 100,
            "RussoOne-Regular": 140,
            "SigmarOne-Regular": 110,
            "Staatliches-Regular": 180,
            "TitanOne-Regular": 130,
        }

    def __getattribute__(self, name):
        if super().__getattribute__("SETTINGS_FILE").exists():
            with open(super().__getattribute__("SETTINGS_FILE"), "r") as f:
                settings_file = json.loads(f.read())
            if name.lower() in settings_file:
                return settings_file[name.lower()]
        return super().__getattribute__(name)

    def create_settings_file(self):
        if not self.SETTINGS_FILE.exists():
            settings = {
                "font_sizes": self.FONT_SIZES,
                "plot_increment": self.PLOT_INCREMENT,
                "page_width": self.PAGE_WIDTH,
                "default_font_size": self.DEFAULT_FONT_SIZE,
                "max_length": self.MAX_LENGTH,
            }
            with open(self.SETTINGS_FILE, "w") as f:
                f.write(json.dumps(settings, indent=4))

    def reset_settings(self):
        if self.SETTINGS_FILE.exists():
            self.SETTINGS_FILE.unlink()
        self.create_settings_file()
        print("Settings reset to default values")


settings = Settings()
settings.create_settings_file()
