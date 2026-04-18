from log_parser import parse_log, get_log_files


def test_parse_log_finds_errors(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("ERROR something failed\nINFO all good\n")
    errors, warnings = parse_log(str(log_file))
    assert len(errors) == 1
    assert "ERROR something failed" in errors[0]


def test_parse_log_finds_warnings(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("WARNING this is a warning\nINFO all good\n")
    errors, warnings = parse_log(str(log_file))
    assert len(errors) == 0
    assert len(warnings) == 1
    assert "WARNING this is a warning" in warnings[0]


def test_parse_log_returns_empty_for_clean_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("INFO started\nINFO all good\n")
    errors, warnings = parse_log(str(log_file))
    assert len(errors) == 0
    assert len(warnings) == 0


def test_get_log_files_filters_correctly(tmp_path):
    (tmp_path / "a.log").write_text("log content")
    (tmp_path / "b.log").write_text("log content")
    (tmp_path / "c.txt").write_text("not a log")
    result = get_log_files(str(tmp_path))
    assert len(result) == 2


def test_get_log_files_returns_empty_when_no_log_files(tmp_path):
    (tmp_path / "a.txt").write_text("not a log")
    (tmp_path / "b.md").write_text("not a log")
    result = get_log_files(str(tmp_path))
    assert result == []
