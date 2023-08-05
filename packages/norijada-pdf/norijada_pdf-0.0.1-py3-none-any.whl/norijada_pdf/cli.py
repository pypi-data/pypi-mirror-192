import argparse
from main import plot, arrange
from settings import settings


def plot_cli(cli_args):
    plot(cli_args.font, cli_args.input_file, rotation=cli_args.rotate)


def arrange_cli(cli_args):
    arrange(cli_args.font, cli_args.input_file, rotation=cli_args.rotate, unique_identifier=cli_args.file_id)


def reset_settings(cli_args):
    settings.reset_settings()


def cli():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # ====================== Reset settings ======================
    parser_a = subparsers.add_parser('reset-settings', help='Reset settings to default values')
    parser_a.set_defaults(func=reset_settings)

    # ====================== Arrange =============================
    parser_b = subparsers.add_parser('arrange', help='Arrange nicknames in a pdf file')
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

    cli_args = parser.parse_args()
    cli_args.func(cli_args)
