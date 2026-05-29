# 🏀 NBA Value Per Million

A web application that ranks every NBA player by composite performance score per salary dollar — built to answer the question: **who actually gives you the most bang for their contract?**

Live demo: `[your-render-url].onrender.com`

---

## What It Does

Most NBA analytics tools rank players by raw performance. This app adjusts for cost — a player scoring 12 points on a minimum contract is far more valuable than a max player doing the same. **Value Per Million** surfaces those undervalued players by normalizing performance within position groups and dividing by log-compressed salary.

---

## Features

- **League Overview** — bar chart of average Value Per Million by position, top 10 and bottom 10 leaderboards
- **Player Lookup** — search any qualifying player and view their full stat card with composite score and value rating
- **Compare Players** — head-to-head comparison table with automatic winner highlighting across 12 statistical categories

---

## Methodology

### Data Sources
All data sourced from [Basketball Reference](https://www.basketball-reference.com/) for the 2025-26 NBA season:
- Per-game statistics
- Advanced statistics (VORP, BPM, Win Shares, PER, TS%)
- Salary data

### Filters Applied
Players must meet all three criteria to be included:
- **400+ total minutes** played
- **10+ minutes per game**
- **$1.5M+ salary** (eliminates two-way and minimum outliers that skew Value/M)

### Traded Players
Players who changed teams mid-season appear in Basketball Reference with individual team rows and a combined row (`2TM`, `3TM`). This app keeps only the combined row to reflect full-season performance.

### Position Normalization
All stats are normalized using **min-max scaling within position groups** — not league-wide. This prevents positional bias where a center's rebounding would always dominate a point guard's assists in a raw comparison.

### Scoring Formula

Each player receives a composite score from 0 to 1:

```
Score = (0.35 × VORP) + (0.20 × PTS) + (0.10 × BPM) + (0.10 × PER)
      + (0.05 × TS%) + (0.05 × WS) + (0.05 × MPG) + (0.05 × STL) + (0.05 × BLK)
```

All inputs are position-normalized before weighting. VORP carries the highest weight as it is the most context-independent measure of player impact.

### Value Per Million

```
ValuePerMillion = Score / log(Salary / 1,000,000)
```

Salary is log-compressed so that the difference between a $2M and $5M contract is treated proportionally larger than the difference between a $30M and $33M contract — reflecting how roster construction actually works in the NBA.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Data Pipeline | pandas, NumPy |
| Frontend | Jinja2, HTML/CSS, Chart.js |
| Player Photos | NBA API (with in-memory caching) |
| Deployment | Render.com |

---

## Project Structure

```
├── app.py                  # Flask backend, all routes
├── analysis.py             # Data pipeline and scoring formula
├── helpers.py              # NBA API headshot functions with caching
├── scored_players.csv      # Final scored dataset (source of truth)
├── advanced_stats.csv      # Raw advanced stats from Basketball Reference
├── per_game.csv            # Raw per-game stats from Basketball Reference
├── salaries.csv            # Raw salary data from Basketball Reference
├── requirements.txt
├── Procfile
└── templates/
    ├── base.html
    ├── index.html
    ├── overview.html
    ├── player.html
    └── compare.html
```

---

## Running Locally

```bash
git clone https://github.com/gabrielfeloiu-creator/nba-value-per-million
cd nba-value-per-million
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`

To refresh the dataset, run `analysis.py` first — this regenerates `scored_players.csv` from the raw CSVs.

---

## Data Credit

Statistics sourced from [Basketball Reference](https://www.basketball-reference.com/).
Player headshots via the [NBA API](https://github.com/swar/nba_api).

Built by Gabriel Feloiu.
