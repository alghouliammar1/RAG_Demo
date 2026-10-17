from pathlib import Path

import pytest

from ocr_rag.ocr import get_input_files


def test_get_input_files_finds_supported_files_recursively(tmp_path: Path) -> None:
    pdf_path = tmp_path / "pdfs" / "document.PDF"
    image_path = tmp_path / "scan.png"
    unsupported_path = tmp_path / "notes.txt"
    pdf_path.parent.mkdir()
    pdf_path.touch()
    image_path.touch()
    unsupported_path.touch()

    assert get_input_files(tmp_path) == [pdf_path, image_path]


def test_get_input_files_requires_an_existing_folder(tmp_path: Path) -> None:
    with pytest.raises(NotADirectoryError):
        get_input_files(tmp_path / "missing")