# MOEX Feature Platform

An end-to-end machine learning platform built on top of the Moscow Exchange ISS API.

The project demonstrates a reproducible workflow for transforming raw market data into ML-ready datasets, features and machine learning experiments.

## Goals

- Collect market data automatically
- Validate and profile downloaded datasets
- Store and model historical market data
- Build reusable ML features
- Prepare reproducible ML datasets
- Train and evaluate ML models
- Track experiments and model versions using MLflow

## Project Lifecycle

The platform follows the lifecycle:

MOEX API
→ Data ingestion
→ Data quality
→ Storage
→ Data modeling
→ Feature engineering
→ ML dataset
→ Model training
→ Evaluation
→ Experiment tracking
→ Inference

## ML Use Cases

The platform is designed to support multiple ML tasks, including:

- Time series forecasting
- Classification
- Regression

The first implementation will focus on a small number of well-defined use cases.

## Project Status

🚧 In active development

**Current stage:** Data acquisition

**Next milestone:** Build and validate the first reproducible MOEX data ingestion pipeline.

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](ROADMAP.md)
- [Architecture Decision Records](adr/)