MOEX Feature Platform — Roadmap
1. Project Discovery
 Define project goals and ML use cases
 Identify MOEX data sources
 Define target users and expected outputs
 Define initial scope

Done when: сформулированы задачи проекта, источники данных и критерии успеха.

2. Data Acquisition
 Implement MOEX API client
 Define raw data ingestion process
 Download initial historical dataset
 Document source schemas and API limitations

Done when: данные MOEX можно воспроизводимо получить программно.

3. Data Quality
 Profile raw datasets
 Identify missing values, duplicates and anomalies
 Define data quality rules
 Implement automated DQ checks
 Document detected data issues and decisions

Done when: pipeline может определить, можно ли доверять загруженным данным.

4. Data Storage & Modeling
 Define raw / staging / curated layers
 Define data models
 Implement storage layer
 Define partitioning and temporal semantics
 Document architecture decisions

Done when: данные хранятся в структурированном и воспроизводимом виде.

5. Feature Engineering
 Define analytical entities
 Create reusable features
 Implement feature generation pipeline
 Validate feature consistency
 Document feature definitions

Done when: из подготовленных данных можно воспроизводимо получить ML-ready dataset.

6. ML Dataset
 Define prediction target
 Define prediction horizon
 Define train / validation / test strategy
 Prevent data leakage
 Build reproducible training dataset

Done when: существует версия ML dataset, которую можно использовать для экспериментов.

7. Baseline & Experiments
 Implement baseline model
 Define evaluation metrics
 Create experiment workflow
 Compare candidate models
 Track experiment results

Done when: есть воспроизводимое сравнение моделей и понятен лучший baseline.

8. ML Use Cases
Time Series Forecasting
 Define forecasting problem
 Implement naive baseline
 Implement statistical models
 Implement ML-based forecasting
 Implement backtesting
 Compare forecasting approaches
Classification / Regression
 Define prediction task
 Build baseline
 Train candidate models
 Evaluate and compare models

Done when: хотя бы один ML use case доведён от данных до воспроизводимого результата.

9. Production ML
 Package trained model
 Implement inference pipeline
 Define model versioning
 Add monitoring
 Define retraining strategy
 Document operational workflow

Done when: модель можно воспроизводимо запустить вне ноутбука.

10. Documentation & Engineering
 Maintain architecture documentation
 Record important decisions in ADRs
 Document data contracts
 Document pipelines and runbooks
 Add tests
 Update README
Project status

Current stage: Project Discovery / Data Acquisition

Next milestone: получить и исследовать первый реальный набор данных MOEX.