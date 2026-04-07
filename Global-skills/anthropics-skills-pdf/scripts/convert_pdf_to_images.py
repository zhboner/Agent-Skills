# /// script
# requires-python = ">=3.11"
# dependencies = ["pdf2image"]
# ///
import os
import sys
import tempfile

from pdf2image import convert_from_path


def convert(pdf_path, output_dir=None, max_dim=1000):
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="pdf_images_")
        print(f"Created temporary directory: {output_dir}")
    else:
        os.makedirs(output_dir, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=200)
    saved_paths = []

    for i, image in enumerate(images):
        width, height = image.size
        if width > max_dim or height > max_dim:
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height))

        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(image_path)
        saved_paths.append(image_path)
        print(f"Saved page {i + 1} as {image_path} (size: {image.size})")

    print(f"Converted {len(images)} pages to PNG images in: {output_dir}")
    return output_dir, saved_paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: convert_pdf_to_images.py [input pdf] [output directory (optional)]"
        )
        print(
            "If output directory is not provided, a temporary directory will be created."
        )
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_directory = sys.argv[2] if len(sys.argv) > 2 else None
    convert(pdf_path, output_directory)
