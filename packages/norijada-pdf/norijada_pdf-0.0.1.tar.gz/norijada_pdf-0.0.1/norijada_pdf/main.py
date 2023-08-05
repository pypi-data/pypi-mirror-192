from pathlib import Path
from typing import List, Tuple
import math
import random
import string

from settings import settings

from rectpack import newPacker
from fpdf import FPDF


def analyze_nicknames(font: str, font_size: int, list_of_nicknames) -> List[Tuple[int, int, str, bool, int]]:
    """
    Calculate the width and height of each nickname. If the width is bigger than the height,
    incrementally decrease the font size until the width is smaller than the maximum allowed length.
    """
    nicknames_analyzed = []
    pdf = FPDF()
    pdf.add_font(family=font, fname=Path(settings.FONTS_DIR) / font)

    for nickname in list_of_nicknames:
        pdf.set_font(font, size=font_size)
        adjusted_font_size = font_size

        width = math.ceil((pdf.get_string_width(nickname)))
        height = math.ceil(font_size * settings.ONE_POINT)

        while width > settings.MAX_LENGTH:
            adjusted_font_size -= 10
            pdf.set_font(font, size=adjusted_font_size)
            width = math.ceil((pdf.get_string_width(nickname)))
            height = math.ceil(adjusted_font_size * settings.ONE_POINT)

        nicknames_analyzed.append((width + 4, height + 4, nickname, width >= height, adjusted_font_size))

    return nicknames_analyzed


def packing_algorithm(nicknames_analyzed: list, rotation: bool = True) -> newPacker:
    """
    Implement packing algorithm to pack the nicknames in the smallest possible space.
    Incrementally increase the height of the page until all the nicknames fit.
    """
    plot_height = 0
    packer = None

    while packer is None or len(packer.rect_list()) != len(nicknames_analyzed):
        packer = newPacker(rotation=rotation)
        plot_height += settings.PLOT_INCREMENT
        packer.add_bin(settings.PAGE_WIDTH, plot_height)
        for index, nickname in enumerate(nicknames_analyzed):
            packer.add_rect(nickname[0], nickname[1], rid=index)
        packer.pack()
    return packer


def plot_nicknames(packer: newPacker, page_width: int, page_height: int, file_identifier: str):
    """
    Plot the nicknames on the canvas to demonstrate the packing algorithm output.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    plt.plot(page_width, page_height)
    for rect in packer.rect_list():
        _, x, y, width, height, rid = rect
        plt.gca().add_patch(Rectangle((x, y), width, height, fill=True, edgecolor="black", linewidth=1))

    plot_filename = Path(settings.PLOT_OUTPUT_DIR) / f"plot-{file_identifier}.jpg"
    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")
    plt.clf()


def create_pdf(packer: newPacker, canvas: tuple, nicknames: List[Tuple[int, int, str, bool, int]],
               font: str, file_identifier: str):
    """
    Arrange the nicknames in the pdf file.
    """
    pdf = FPDF(format=canvas)
    pdf.add_font(family=font, fname=Path(settings.FONTS_DIR) / font)
    pdf.add_page()
    for rect in packer.rect_list():
        _, x, y, width, height, nickname_index = rect
        _, _, nickname, rotate, font_size = nicknames[nickname_index]
        pdf.set_font(font, size=font_size)
        if (pdf.get_x() + width) > settings.PAGE_WIDTH:
            pdf.ln()

        # If enabled packer rotation, rotate the nickname and write it in the bottom left corner
        if rotate and width < height:
            with pdf.rotation(90, x=x, y=y + height):
                pdf.text(x + 2, y + height + width - 2, nickname)
        else:
            pdf.text(x + 2, y + height - 2, nickname)

    pdf_filename = Path(settings.PDF_OUTPUT_DIR) / f"nicknames-{file_identifier}.pdf"
    pdf.output(pdf_filename)
    print(f"PDF saved to {pdf_filename}")


def get_random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str


def extract_nicknames(file_path: str) -> List[str]:
    """
    Extract the nicknames from the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        nicknames = file.read().splitlines()
    return nicknames


def arrange(font: str, file_path: str, rotation: bool = True, unique_identifier: str = None):
    """
    Create a pdf file with a list of nicknames with minimal space between them
    starting from the top of the left top corner of the page until all the nicknames are written.
    """
    font_size = settings.FONT_SIZES.get(font, settings.DEFAULT_FONT_SIZE)

    list_of_nicknames = extract_nicknames(file_path)
    nicknames = analyze_nicknames(font, font_size, list_of_nicknames)
    packer = packing_algorithm(nicknames, rotation=rotation)

    file_identifier = get_random_string() if unique_identifier is None else unique_identifier

    create_pdf(packer, packer.bin_list()[0], nicknames, font, file_identifier)


def plot(font: str, file_path: str, rotation: bool = True, unique_identifier: str = None):
    """
    Plot the nicknames on the canvas to demonstrate the packing algorithm output.
    """
    font_size = settings.FONT_SIZES.get(font, settings.DEFAULT_FONT_SIZE)

    list_of_nicknames = extract_nicknames(file_path)
    nicknames = analyze_nicknames(font, font_size, list_of_nicknames)
    packer = packing_algorithm(nicknames, rotation=rotation)

    file_identifier = get_random_string() if unique_identifier is None else unique_identifier
    plot_width, plot_height = packer.bin_list()[0]
    plot_nicknames(packer, plot_width, plot_height, file_identifier)
