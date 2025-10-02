import os
import shutil
import tempfile
import types

import pytest

import app.capture_ebook as cap


@pytest.fixture
def tmp_outdir():
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir)


def test_argparse_defaults():
    assert isinstance(cap.main, types.FunctionType)


def test_invalid_count(capsys):
    test_args = ["--count", "0"]
    with pytest.raises(SystemExit):
        cap.main(test_args)
    captured = capsys.readouterr()
    assert "Nothing to capture" in captured.out


def test_invalid_region(capsys):
    test_args = ["--width", "-1", "--height", "100"]
    with pytest.raises(SystemExit):
        cap.main(test_args)
    captured = capsys.readouterr()
    assert "Invalid region" in captured.out


def test_capture_flow(monkeypatch, tmp_outdir):
    calls = {"screenshot": 0, "press": 0}

    class DummyImage:
        def save(self, path):
            with open(path, "wb") as f:
                f.write(b"dummy")

    monkeypatch.setattr(
        cap.pyautogui, 
        "screenshot", 
        lambda region: 
            (calls.update(screenshot=calls["screenshot"]+1), 
            DummyImage()
            )[1]
        )
    monkeypatch.setattr(
        cap.pyautogui, 
        "press", 
        lambda key: calls.update(press=calls["press"]+1)
        )
    monkeypatch.setattr(
        cap, 
        "wait_start_via_click", 
        lambda: None
        )

    args = [
        "--outdir", os.path.basename(tmp_outdir),
        "--count", "2",
        "--per-page-wait", "0.1",
        "--left", "0", "--top", "0", "--width", "10", "--height", "10"
    ]
    cap.main(args)

    assert calls["screenshot"] == 2
    assert calls["press"] == 2
    files = os.listdir(tmp_outdir)
    assert any(f.endswith(".png") for f in files)
