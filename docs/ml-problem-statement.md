# ML Problem Statement

## Business Problem

The company needs to assess the short-term currency risk associated
with future payments to Chinese suppliers.

The direction of the CNY/RUB movement is economically important.

An increase in CNY/RUB raises the RUB cost of future CNY-denominated
payments and therefore represents an adverse currency movement
for the company.

A decrease in CNY/RUB reduces the RUB cost of the same obligation.

The company is therefore interested both in the direction of future
exchange-rate movements and in the risk of unusually large movements.


## Initial ML Objective

The primary ML objective is to estimate the probability of an adverse
upward CNY/RUB movement on the next trading day using information
available after the current trading session.

A secondary objective is to estimate the probability or magnitude
of an unusually large exchange-rate movement regardless of direction.

The first instrument selected for detailed research is CNYRUB_TOM.


## Related Research Tasks

- Forecast the next-day CNY/RUB return.
- Estimate the probability of an adverse upward CNY/RUB movement.
- Estimate the probability of an unusually large movement in either direction.
- Forecast short-term exchange-rate volatility.
- Compare statistical time-series models with tabular ML models.
- Compare a CNY-specific model with models trained on several
  comparable FX instruments.
- Evaluate whether models outperform simple time-aware baselines.
- Analyse the business consequences of false alarms and missed
  adverse currency movements.


## Important Limitations

This is a research and training project.

The models are developed to study ML and data engineering approaches
to short-term FX risk assessment and are not intended to provide
investment recommendations or operate as a production financial
risk management system.