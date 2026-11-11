# Day 04 - Plaque Assay Calculator & Web App

This project analyzes plaque assay experiment data. It calculates the average plaque counts, normalizes them according to cell numbers, and computes the relative infection yield compared to a control sample.

You can run this project in two ways:
1. In your web browser (visual interface).
2. Directly in the terminal.

---

## CSV File Requirements

To run the analysis, your CSV file must include these column headers:
- `sample_id`: The name of your sample (e.g., `siNT`, `siTarget_protein`).
- `dilution`: The dilution factor (e.g., `-4`).
- `rep1`, `rep2`, `rep3`: Raw plaque counts for the 3 experimental replicates.
- `cell_count`: Number of cells counted for the condition.

*Note: The default control sample is `siNT`. If your control has a different name, type it into the input box on the web page.*

---

## How to Run

### 1. In the Web Browser
1. Start the web application by running this command in your terminal:

2. Open your browser and go to:
`http://127.0.0.1:5001`
3. Upload your CSV file (or click **Download CSV Template** to get an example file).
4. Click **Analyze Assay Data** to view the calculated results table.

### 2. In the Terminal
You can also run the calculations directly without the web browser:

The results will be displayed as text directly in the terminal window.

---

## Calculations Performed
- **Mean:** Average plaque count of the 3 replicates.
- **Norm Ratio:** Control cell count divided by sample cell count.
- **Corrected Mean:** Mean plaques multiplied by the normalization ratio.
- **Yield (%):** Corrected mean of the sample compared to the control sample (set to 100%).