# GitHub Peru Analytics

A comprehensive data analysis and dashboard project exploring the GitHub developer ecosystem in Peru. This project extracts data using the GitHub REST API, processes it, and provides an interactive Streamlit dashboard.

## Project Structure
This repository uses a modular structure:
- `data/`: Contains raw API responses, processed clean data, and calculated metrics.
- `src/`: Modular source code for extraction, database operations, classification, and metrics calculations.
- `app/`: Streamlit dashboard application, featuring an overview and specialized pages.
- `scripts/`: Standalone scripts to trigger extraction and processing tasks.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Copy `.env.example` to a new file named `.env` and configure your GitHub Personal Access Token:
   ```bash
   cp .env.example .env
   ```

3. **Run the Dashboard:**
   ```bash
   streamlit run app/main.py
   ```
