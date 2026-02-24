# London Crime Data

An interactive dashboard to explore crime data in London. Filter by year and crime type, view key metrics, and explore trends and patterns across the city's boroughs.

---

**Stable Posit Cloud link:**
https://019c8cf1-a288-5cee-f1a1-893bc0f9414c.share.connect.posit.cloud

**Preview Posit Cloud link:**
https://019c8cf5-07e1-aea6-bf22-33e39990085b.share.connect.posit.cloud

## Getting the Dashboard Running Locally

### Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) installed

### Steps

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/ybaher/DSCI-532_2026_16_LondonCrime.git
   cd DSCI-532_2026_16_LondonCrime
   ```

2. **Create the conda environment**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment**
   ```bash
   conda activate LondonCrime
   ```

<!-- 4. **Install Shiny** (if not already in the environment)
   ```bash
   pip install shiny
   ``` -->

5. **Run the dashboard**
   ```bash
   shiny run src/app.py
   ```

6. **Open the app** in your browser at `http://127.0.0.1:8000` (or the URL shown in the terminal).
