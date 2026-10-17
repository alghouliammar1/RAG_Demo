"""Extract text from PDFs and images, preserving source and page information."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict

DEFAULT_INPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
SUPPORTED_EXTENSIONS = {".pdf", ".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


class ExtractedPage(TypedDict):
	"""Text extracted from one page or image, with its source location."""

	source: str
	page: int
	text: str


def get_input_files(input_dir: str | Path = DEFAULT_INPUT_DIR) -> list[Path]:
	"""List supported document files under ``input_dir``, including subfolders."""
	input_path = Path(input_dir)
	if not input_path.is_dir():
		raise NotADirectoryError(f"Input folder does not exist: {input_path}")

	return sorted(
		path
		for path in input_path.rglob("*")
		if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
	)


def extract_text_from_input_folder(
	input_dir: str | Path = DEFAULT_INPUT_DIR,
	*,
	language: str = "eng",
) -> list[ExtractedPage]:
	"""Discover supported files in the input folder and extract their text."""
	return extract_text_from_files(get_input_files(input_dir), language=language)


def extract_text_from_files(
	file_paths: Iterable[str | Path],
	*,
	language: str = "eng",
) -> list[ExtractedPage]:
	"""Extract page-level text from a list of PDF and image file paths."""
	extracted_pages: list[ExtractedPage] = []

	for file_path in file_paths:
		path = Path(file_path)
		if not path.is_file():
			raise FileNotFoundError(f"Input file does not exist: {path}")

		extension = path.suffix.lower()
		if extension == ".pdf":
			extracted_pages.extend(_extract_pdf(path, language))
		elif extension in SUPPORTED_EXTENSIONS:
			text = _extract_image(path, language)
			if text:
				extracted_pages.append({"source": str(path), "page": 1, "text": text})
		else:
			raise ValueError(f"Unsupported input file type: {path.suffix or '(no extension)'}")

	return extracted_pages


def _extract_image(image_path: Path, language: str) -> str:
	try:
		from PIL import Image
		import pytesseract
	except ImportError as error:
		raise RuntimeError('Install OCR dependencies with: pip install -e ".[ocr]"') from error

	with Image.open(image_path) as image:
		return pytesseract.image_to_string(image, lang=language).strip()


def _extract_pdf(pdf_path: Path, language: str) -> list[ExtractedPage]:
	try:
		from pypdf import PdfReader
	except ImportError as error:
		raise RuntimeError('Install OCR dependencies with: pip install -e ".[ocr]"') from error

	pages: list[ExtractedPage] = []
	reader = PdfReader(str(pdf_path))
	for page_number, pdf_page in enumerate(reader.pages, start=1):
		text = (pdf_page.extract_text() or "").strip()
		if not text:
			text = _ocr_pdf_page(pdf_path, page_number - 1, language)
		if text:
			pages.append({"source": str(pdf_path), "page": page_number, "text": text})

	return pages


def _ocr_pdf_page(pdf_path: Path, page_index: int, language: str) -> str:
	try:
		import pymupdf
		from PIL import Image
		import pytesseract
	except ImportError as error:
		raise RuntimeError(
			'Install PDF OCR dependencies with: pip install -e ".[ocr]"'
		) from error

	import io

	with pymupdf.open(pdf_path) as document:
		page = document.load_page(page_index)
		image_bytes = page.get_pixmap(dpi=200).tobytes("png")

	with Image.open(io.BytesIO(image_bytes)) as image:
		return pytesseract.image_to_string(image, lang=language).strip()