from pathlib import Path
import zipfile


def has_allowed_file_type(upload):
    extension = Path(upload.name).suffix.lower()
    upload.seek(0)
    header = upload.read(16)
    upload.seek(0)

    if extension == ".pdf":
        return header.startswith(b"%PDF-")
    if extension == ".docx":
        try:
            with zipfile.ZipFile(upload) as archive:
                names = set(archive.namelist())
            return {
                "[Content_Types].xml",
                "word/document.xml",
            }.issubset(names)
        except (OSError, zipfile.BadZipFile):
            return False
        finally:
            upload.seek(0)
    if extension == ".zip":
        try:
            return zipfile.is_zipfile(upload)
        except OSError:
            return False
        finally:
            upload.seek(0)

    image_signatures = {
        ".png": b"\x89PNG\r\n\x1a\n",
        ".jpg": b"\xff\xd8\xff",
        ".jpeg": b"\xff\xd8\xff",
        ".gif": (b"GIF87a", b"GIF89a"),
    }
    if extension in image_signatures:
        signature = image_signatures[extension]
        if isinstance(signature, tuple):
            return header.startswith(signature)
        return header.startswith(signature)
    if extension == ".webp":
        return header.startswith(b"RIFF") and header[8:12] == b"WEBP"
    return False
