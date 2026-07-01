# Pipeline Dependency Analyzer MVP

A minimal dependency analyzer for RADAR Services automation pipelines.

## Status

MVP in progress.

## Purpose

Analyze dependency relationships between pipeline YAML files before orchestration.

## Target Flow

```text
pipeline YAML files
    ↓
pipeline-dependency analyze
    ↓
dependency.report.json
    ↓
pipeline orchestrator
```
