import os
import sys

import pymupdf


def convert(pdf_path, output_dir, max_dim=1000):
    doc = pymupdf.open(pdf_path)

    for i, page in enumerate(doc):
        zoom = 200 / 72
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        width, height = pix.width, pix.height
        if width > max_dim or height > max_dim:
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            zoom_x = new_width / pix.width
            zoom_y = new_height / pix.height
            mat = pymupdf.Matrix(zoom * zoom_x, zoom * zoom_y)
            pix = page.get_pixmap(matrix=mat)

        image_path = os.path.join(output_dir, f"page_{i+1}.png")
        pix.save(image_path)
        print(f"Saved page {i+1} as {image_path} (size: ({pix.width}, {pix.height}))")

    print(f"Converted {len(doc)} pages to PNG images")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_pdf_to_images.py [input pdf] [output directory]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2]
    convert(pdf_path, output_directory)
