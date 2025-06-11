# Gaming Viral Signal Detection

A data analytics project to detect games before they go viral by tracking multiple signals across platforms.

## Project Overview
This system monitors Twitch viewership, Reddit discussions, Steam player counts, and Google Trends to identify games with viral potential 7-14 days before mainstream adoption.

## Current Progress (as of June 9, 2025)

### ✅ Completed:
1. **Project Structure** - Set up with src/collectors, data/, config/, etc.
2. **Virtual Environment** - Python 3.10, all dependencies in requirements.txt
3. **API Credentials** - Reddit and Twitch APIs configured in .env
4. **Base Collector** - Abstract class for all collectors (base_collector.py)
5. **Twitch Collector** - Fully functional with:
   - Real-time viewer counts
   - Batch collection (parallel processing)
   - Caching and rate limiting
   - Tests passing
6. **Reddit Collector** - Just created, needs testing

### 🚧 Next Steps:
1. Test Reddit collector
2. Create Steam collector
3. Create Google Trends collector
4. Build data processing pipeline
5. Create viral prediction model
6. Build Streamlit dashboard

### Installation

```bash
# Clone repository
git clone https://github.com/gitusername/gaming_trends_analysis.git
cd gaming_trends_analysis

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API credentials