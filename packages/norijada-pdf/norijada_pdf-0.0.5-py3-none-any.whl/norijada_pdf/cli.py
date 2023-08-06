import argparse
import os
import shutil
from pathlib import Path
from main import plot, arrange
from settings import settings


def plot_cli(cli_args):
    plot(cli_args.font, cli_args.input_file, rotation=cli_args.rotate)


def arrange_cli(cli_args):
    arrange(cli_args.font, cli_args.input_file, rotation=cli_args.rotate, unique_identifier=cli_args.file_id)


def reset_settings(cli_args):
    settings.reset_settings()


def list_fonts(cli_args):
    print("Available fonts:")

    for index, font in enumerate(os.listdir(settings.FONTS_DIR), start=1):
        print(f"{index}. {font}")


def add_fonts(cli_args):
    """Copy the fonts from the specified source directory to the fonts folder"""
    source_dir = str(Path(os.getcwd()) / cli_args.dir)
    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} does not exist")
    else:
        print(f"Copying fonts from {source_dir} to {settings.FONTS_DIR}")
        for font in os.listdir(source_dir):
            if font.endswith(".ttf"):
                shutil.copyfile(str(Path(source_dir) / font), str(Path(settings.FONTS_DIR) / font))


def parse_cli():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # ====================== Reset settings ======================
    parser_a = subparsers.add_parser('reset-settings', help='Reset settings to default values')
    parser_a.set_defaults(func=reset_settings)

    # ====================== Arrange =============================
    parser_b = subparsers.add_parser('generate-pdf', help='Arrange nicknames in a pdf file')
    parser_b.add_argument("--input-file",
                          help="Path to txt file with text, each text field to arrange in the pdf has to be on a new line",
                          default="input.txt")
    parser_b.add_argument("-f", "--font",
                          help="Font name, ex. BebasNeue-Regular.ttf",)
    parser_b.add_argument("-r", "--rotate",
                          help="Rotate the nicknames to optimize the space",
                          action=argparse.BooleanOptionalAction)
    parser_b.add_argument("-fid", "--file-id",
                          help="Attach unique file id or script will generate one",
                          default=None)
    parser_b.set_defaults(func=arrange_cli)

    # ====================== Plot ================================
    parser_c = subparsers.add_parser('plot', help='Show plots of the nicknames for preview')
    parser_c.add_argument("--input-file",
                          help="Path to txt file with text, each text field to arrange in the pdf has to be on a new line",
                          default="input.txt")
    parser_c.add_argument("-f", "--font",
                          help="Font name, ex. BebasNeue-Regular.ttf",)
    parser_c.add_argument("-r", "--rotate",
                          help="Rotate the nicknames to optimize the space",
                          action=argparse.BooleanOptionalAction)
    parser_c.add_argument("-fid", "--file-id",
                          help="Attach unique file id or script will generate one",
                          default=None)
    parser_c.set_defaults(func=plot_cli)

    # ====================== List Fonts ==========================
    parser_d = subparsers.add_parser('list-fonts', help='List all fonts available in the fonts folder')
    parser_d.set_defaults(func=list_fonts)

    # ====================== Add Fonts ===========================
    parser_e = subparsers.add_parser('add-fonts', help='Add fonts to the fonts folder')
    parser_e.add_argument("--dir", help="Folder name with fonts to add, default working_dir/fonts", default="fonts")
    parser_e.set_defaults(func=add_fonts)

    cli_args = parser.parse_args()
    cli_args.func(cli_args)
