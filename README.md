# PLE Data Analysis Dashboard

## 📊 Overview
Interactive Streamlit dashboard for analyzing Primary Leaving Examination (PLE) results with comprehensive visualizations and data insights.

## 🚀 Quick Start

### Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run ple_dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## 📁 Data Sources

The dashboard supports two data loading methods:

### 1. Local CSV Files
Place your CSV files in the `data/` directory:
- `data/PLE_2025_verified_rewrite.csv`
- `data/P.L.E Digest 2023 - 2024 v1 - ple digest 2023 - 2024.csv`

### 2. Google Sheets
1. Make your Google Sheet publicly accessible
2. Copy the Sheet ID from the URL
3. Enter it in the dashboard sidebar

## 🎯 Features

### Interactive Analysis Tabs
- **📈 Overview**: Division distribution, pass rates, summary statistics
- **🎯 Performance**: Trends, correlations, performance metrics
- **👥 Gender Analysis**: Boys vs girls comparison, gender gap insights
- **🏆 Rankings**: Top and bottom performing districts
- **📊 Districts**: Individual district deep-dive analysis
- **📉 Trends**: Year-over-year changes and improvements

### Key Metrics
- Total student registrations
- Pass rates and excellence rates
- Division distributions
- Gender performance comparisons
- District rankings

## 📦 Project Structure

```
PLE Analysis/
├── ple_dashboard.py          # Main dashboard application
├── requirements.txt           # Python dependencies
├── Google_Sheet_Analysis.ipynb # Jupyter notebook for analysis
├── data/                      # Data directory
│   ├── PLE_2025_verified_rewrite.csv
│   └── P.L.E Digest 2023 - 2024 v1 - ple digest 2023 - 2024.csv
└── README.md                  # This file
```

## 🔧 Requirements

- Python 3.8 or higher
- See `requirements.txt` for package dependencies

## 📊 Data Format

The dashboard expects data with the following columns:
- District/Area names
- Year (optional, for trend analysis)
- Division data (Div 1-4, U, X) by gender
- Registration totals

## 🎨 Customization

The dashboard uses a professional color scheme:
- Primary Blue: #4C72B0
- Secondary Green: #55A868
- Accent Red: #C44E52
- Colorblind-friendly palette

## 🐛 Troubleshooting

### Data Not Loading
- Ensure CSV files are in the `data/` directory
- Check Google Sheet sharing settings (must be public)
- Verify data format matches expected structure

### Dashboard Not Starting
- Check Python version: `python --version`
- Reinstall requirements: `pip install -r requirements.txt --upgrade`
- Clear Streamlit cache: `streamlit cache clear`

## 📝 License

This project is for educational and analytical purposes.

## 🤝 Contributing

Suggestions and improvements are welcome!

## 📧 Support

For issues or questions, please check the data format and ensure all requirements are installed.

---

**Made with ❤️ for PLE Data Analysis**
