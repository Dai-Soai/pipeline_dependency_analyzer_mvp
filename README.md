# Pipeline Dependency Analyzer MVP

A minimal dependency analyzer for RADAR Services automation pipelines.

## Status

MVP Stable  
Version: v0.1.0  
Test status: 36 passed

## Purpose

Analyze dependency relationships between pipeline YAML files before orchestration.

## Core Flow

```text
pipeline YAML files
    ↓
pipeline-dependency analyze
    ↓
dependency.report.json
    ↓
pipeline orchestrator
```

## Features

- Dependency contract
- Pipeline YAML loader
- Dependency graph builder
- Missing dependency detection
- Cycle detection
- Execution order generation
- CLI analyze command
- JSON dependency report

## CLI Usage

```bash
pipeline-dependency
```

```bash
pipeline-dependency analyze examples/pipelines
```

```bash
pipeline-dependency analyze examples/pipelines \
  --report-json reports/dependency.report.json
```

Expected output:

```text
Dependency analysis: passed
Pipelines: 3
Issues: 0
Execution order:
1. database
2. prepare
3. workflow
```

## JSON Report

```json
{
  "event_type": "pipeline_dependency_analysis",
  "status": "passed",
  "ok": true,
  "pipeline_count": 3,
  "issue_count": 0,
  "execution_order": [
    "database",
    "prepare",
    "workflow"
  ],
  "issues": []
}
```

## Integration

```text
Utility #13 — Pipeline Validator
        ↓
Utility #14 — Pipeline Dependency Analyzer
        ↓
Utility #10 — Pipeline Orchestrator
```

No direct package dependency is introduced between utilities.

Utility #14 only analyzes dependency contracts before Utility #10 executes pipelines.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
pytest
```

Expected:

```text
36 passed
```

## Package Build

```bash
python -m pip install build
python -m build
```

Expected artifacts:

```text
dist/pipeline_dependency_analyzer_mvp-0.1.0.tar.gz
dist/pipeline_dependency_analyzer_mvp-0.1.0-py3-none-any.whl
```

## Release Notes

### v0.1.0

Completed:

- M1 Bootstrap
- M2 Dependency Contract
- M3 Pipeline Loader
- M4 Graph Builder
- M5 Cycle Detection
- M6 Execution Order
- M7 CLI Analyze
- M8 JSON Report

Test status:

```text
36 passed
```

## License

Internal RADAR Services utility.
