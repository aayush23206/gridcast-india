# GridCast India ⚡

Real-time energy demand forecasting for Indian power grids.

## Live Demo
[Link to GitHub Pages frontend](https://aayush23206.github.io/gridcast-india/)

## API Docs
- `GET /api/forecast?region=NR&days=7&model=prophet`
- `GET /api/actual?region=SR&start=2024-01-01&end=2024-01-31`
- `GET /api/comparison?region=WR`
- `GET /api/health`

## Data Source
**MERIT India** (merit.posoco.gov.in) — Ministry of Power, Govt. of India.
Provides real-time merit order dispatch and regional stats.

## Regions Supported
- **NR**: Northern
- **SR**: Southern
- **ER**: Eastern 
- **WR**: Western
- **NER**: North-Eastern

## Tech Stack
- **Backend**: Python, Flask, Facebook Prophet, statsmodels (ARIMA)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Vanilla HTML/JS, Chart.js
- **Deployment**: Render.com (API), GitHub Pages (Frontend)

## Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/aayush23206/gridcast-india.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add a `.env` file with your credentials:
   ```env
   SUPABASE_URL=...
   SUPABASE_KEY=...
   DATA_GOV_API_KEY=...
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Model Performance (Sample Benchmarks)
| Region | Model   | MAE     | RMSE    | MAPE  |
|--------|---------|---------|---------|-------|
| NR     | Prophet | 3,200MW | 4,100MW | 2.3%  |
| SR     | Prophet | 2,800MW | 3,600MW | 2.1%  |
| WR     | ARIMA   | 3,500MW | 4,400MW | 2.6%  |

## Author
**Aayush** — B.Tech CSE (AI & ML), Parul University
GitHub: [aayush23206](https://github.com/aayush23206)
