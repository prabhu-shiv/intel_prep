from system_check import run_command


def test_run_command_returns_none_for_nonexistent_command():
    result = run_command(["nonexistent_command"])
    assert result is None
