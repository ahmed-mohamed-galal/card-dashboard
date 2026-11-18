# 🚗 Cars Market — Executive Dashboard

An interactive **Streamlit** dashboard that turns a cars dataset (428 models, 38 brands) into clear, decision-ready insights for management.

### 🔗 [Live Demo](https://card-dashboard-xdjshm7ntenk4prnez4cfi.streamlit.app/)

<!-- Add a screenshot: save it as screenshot.png in the repo, then uncomment the next line -->
<!-- ![Dashboard preview](screenshot.png) -->

---

## ✨ Features

- **Executive KPI cards** — number of models, average & median MSRP, average dealer margin, average horsepower, and combined MPG.
- **Auto-generated Key Takeaways** — widest brand range, most expensive brand, best horsepower per dollar, most fuel-efficient model, and highest dealer margin.
- **Interactive filters** — origin, body type, drivetrain, brand, and MSRP range. Every chart and KPI updates instantly.
- **Six focused tabs**

| Tab | What it answers |
|---|---|
| 🌍 Market | Which origins, body types, and drivetrains dominate the market? |
| 💲 Price & Margin | How are prices distributed? Which brands earn the highest dealer margin? |
| ⚡ Performance | Does more money buy more power? Top power-to-weight and best value for money. |
| ⛽ Efficiency | How does weight affect fuel economy? Which models are most efficient? |
| 🏢 Brands | Brand positioning (price vs. power) and a full brand scorecard. |
| 🗂️ Data | Browse the filtered data and download it as CSV. |

---

## 🧮 Engineered Metrics

| Metric | Formula |
|---|---|
| Dealer Margin % | `(MSRP − Invoice) / MSRP × 100` |
| MPG Combined | `0.55 × MPG_City + 0.45 × MPG_Highway` |
| HP per 1,000 lb | `Horsepower / Weight × 1000` |
| HP per Liter | `Horsepower / EngineSize` |
| HP per $1k | `Horsepower / (MSRP / 1000)` |

---

## 🧹 Data Cleaning

- Removed fully empty rows and duplicate records.
- Converted `MSRP` and `Invoice` from text (`"$36,945 "`) to numbers.
- Kept missing values as empty instead of filling them with zeros, so averages are not distorted (e.g. the Mazda RX-8 rotary engine has no cylinder count).

---

## 📊 Dataset

`Cars Data1.csv` — one row per vehicle model.

| Column | Description |
|---|---|
| Make, Model | Brand and model name |
| Type | Body type (Sedan, SUV, Sports, Truck, Wagon, Hybrid) |
| Origin | Asia, Europe, or USA |
| DriveTrain | Front, Rear, or All |
| MSRP, Invoice | Suggested retail price and dealer invoice price (USD) |
| EngineSize, Cylinders | Engine displacement (L) and cylinder count |
| Horsepower | Engine power (hp) |
| MPG_City, MPG_Highway | Fuel economy |
| Weight, Wheelbase, Length | Vehicle dimensions (lb / in) |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas / NumPy** — data cleaning and analysis
- **Plotly Express** — interactive charts

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/ahmed-mohamed-galal/card-dashboard.git
cd card-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run carproj.py
```

The app opens at `http://localhost:8501`.

---

## 📁 Project Structure

```
card-dashboard/
├── carproj.py          # Streamlit app
├── Cars Data1.csv      # Dataset
├── requirements.txt    # Dependencies
└── README.md
```

---

## 👤 Author

**Ahmed Mohamed Galal** — Data Science | AI Engineering

- LinkedIn: [ahmed-mohamed-galal](https://www.linkedin.com/in/ahmed-mohamed-galal/)
- Portfolio: [ahmed-galal.lovable.app](https://ahmed-galal.lovable.app)
- GitHub: [@ahmed-mohamed-galal](https://github.com/ahmed-mohamed-galal)
