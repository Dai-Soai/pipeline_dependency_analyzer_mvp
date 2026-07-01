from pathlib import Path

from pipeline_dependency_analyzer.cli import main


def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["pipeline-dependency"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Analyze RADAR Services pipeline dependencies" in captured.out


def test_cli_analyze_success(tmp_path: Path, monkeypatch, capsys):
    (tmp_path / "database.pipeline.yaml").write_text(
        "pipeline_id: database\ndepends_on: []\n",
        encoding="utf-8",
    )
    (tmp_path / "prepare.pipeline.yaml").write_text(
        "pipeline_id: prepare\ndepends_on:\n  - database\n",
        encoding="utf-8",
    )
    (tmp_path / "workflow.pipeline.yaml").write_text(
        "pipeline_id: workflow\ndepends_on:\n  - prepare\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "pipeline-dependency",
            "analyze",
            str(tmp_path),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Dependency analysis: passed" in captured.out
    assert "Execution order:" in captured.out
    assert "1. database" in captured.out
    assert "2. prepare" in captured.out
    assert "3. workflow" in captured.out


def test_cli_analyze_failure(tmp_path: Path, monkeypatch, capsys):
    (tmp_path / "workflow.pipeline.yaml").write_text(
        "pipeline_id: workflow\ndepends_on:\n  - missing\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "pipeline-dependency",
            "analyze",
            str(tmp_path),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Dependency analysis: failed" in captured.out
    assert "missing_dependency" in captured.out


def test_cli_analyze_missing_dir(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pipeline-dependency",
            "analyze",
            "missing-pipelines",
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Dependency analysis failed to start" in captured.err
