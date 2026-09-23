# ADR-001 Project Goal

## Status

Accepted

## Context

The project is intended to become a portfolio demonstrating practical Machine Learning engineering skills.

There are many possible directions:
- stock price prediction;
- trading bot;
- dashboard;
- ETL pipeline;
- feature engineering platform.

A clear project scope is required before implementation begins.

## Decision

Build an end-to-end feature platform instead of a single ML model.

## Consequences

The project will consist of several independent components.

Machine learning models will become consumers of prepared features instead of being the central component.

The architecture should allow adding new models without changing the data ingestion pipeline.

## Interview Notes

Why did you choose a feature platform instead of a price prediction model?

Because feature engineering is reusable across multiple ML tasks. In real production systems, data preparation usually serves many models rather than a single notebook experiment. This approach better demonstrates software engineering and ML engineering skills.