from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from backend.app import app

client = TestClient(app)


def create_test_image():
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


def test_extract_palette_success():
    image_bytes = create_test_image()

    response = client.post(
        "/api/palette",
        files={
            "file": ("test.png", image_bytes, "image/png"),
        },
        data={"n_colors": 3},
    )

    assert response.status_code == 200

    data = response.json()

    assert "colors" in data
    assert "image_base64" in data

    assert isinstance(data["colors"], list)
    assert len(data["colors"]) > 0

    assert data["image_base64"].startswith(
        "data:image/png;base64,"
    )

def test_extract_palette_empty_file():
    response = client.post(
        "/api/palette",
        files={
            "file": ("empty.png", b"", "image/png"),
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "code": "EMPTY_FILE",
        "detail": "Arquivo de imagem vazio.",
    }

def test_extract_palette_invalid_content_type():
    response = client.post(
        "/api/palette",
        files={
            "file": (
                "arquivo.txt",
                b"texto de testeW",
                "text/plain",
            )
        },
    )

    assert response.status_code == 415

    assert response.json() == {
        "code": "UNSUPPORTED_IMAGE_TYPE",
        "detail": "Formato não suportado. Envie apenas imagens PNG ou JPEG.",
    }