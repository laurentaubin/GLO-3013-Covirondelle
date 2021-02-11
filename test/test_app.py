from .context import src


def test_app(capsys):
    src.HelloWorld.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
