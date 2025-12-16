def test_imports():
    import app.main
    assert app.main.app is not None
