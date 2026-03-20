-- Energy Demand Data Table
CREATE TABLE energy_data (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    region VARCHAR(10) NOT NULL,
    demand_mw DOUBLE PRECISION NOT NULL,
    frequency_hz DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(timestamp, region)
);

-- Forecasts Table
CREATE TABLE forecasts (
    id BIGSERIAL PRIMARY KEY,
    region VARCHAR(10) NOT NULL,
    model_type VARCHAR(20) NOT NULL,
    forecast_timestamp TIMESTAMPTZ NOT NULL,
    predicted_mw DOUBLE PRECISION NOT NULL,
    lower_bound DOUBLE PRECISION,
    upper_bound DOUBLE PRECISION,
    horizon_days INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Model Metrics Table
CREATE TABLE model_metrics (
    id BIGSERIAL PRIMARY KEY,
    region VARCHAR(10) NOT NULL,
    model_type VARCHAR(20) NOT NULL,
    mae DOUBLE PRECISION,
    rmse DOUBLE PRECISION,
    mape DOUBLE PRECISION,
    trained_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_energy_region_time ON energy_data(region, timestamp);
CREATE INDEX idx_forecast_region_model ON forecasts(region, model_type);
