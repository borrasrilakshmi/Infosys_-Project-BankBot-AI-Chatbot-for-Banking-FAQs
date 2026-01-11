import os

def test_dashboard_exists():
    assert os.path.exists("app.py")
