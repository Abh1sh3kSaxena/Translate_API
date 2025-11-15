import pytest
from fastapi.testclient import TestClient

from app.main import app

class DummyTranslator:
    def translate(self, text, max_length=256):
        return f"FR: {text}"

@pytest.fixture(autouse=True)
def patch_translator(monkeypatch):
    import app.translator as translator_mod
    monkeypatch.setattr(translator_mod, 'get_translator', lambda: DummyTranslator())

client = TestClient(app)

def test_translate_ok():
    r = client.post('/translate', json={'text': 'Hello'})
    assert r.status_code == 200
    data = r.json()
    assert data['translation'] == 'FR: Hello'

def test_translate_empty():
    r = client.post('/translate', json={'text': ''})
    assert r.status_code == 200
    assert r.json()['translation'] == ''
