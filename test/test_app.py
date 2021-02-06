from .context import main


def test_app(capsys):
    main.HelloWorld.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out