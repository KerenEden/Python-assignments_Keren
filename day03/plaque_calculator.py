import csv
import statistics


def analyze_plaque_assay(csv_filepath: str, control_sample: str = "siNT") -> dict:
    """
    Reads plaque assay data with replicates and cell counts, then calculates:
    - Raw replicate mean
    - Normalization ratio relative to control cell count
    - Corrected mean plaque count
    - Relative infection ratio (%) compared to control
    """
    samples_data = {}

    with open(csv_filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sample = row["sample_id"].strip()
            # Extract replicate plaque counts
            replicates = [
                float(row["rep1"]),
                float(row["rep2"]),
                float(row["rep3"])
            ]
            cell_count = float(row["cell_count"])

            raw_mean = statistics.mean(replicates)
            samples_data[sample] = {
                "dilution": row["dilution"].strip(),
                "raw_mean": raw_mean,
                "cell_count": cell_count
            }

    if control_sample not in samples_data:
        raise ValueError(f"Control sample '{control_sample}' not found in the dataset.")

    control_cells = samples_data[control_sample]["cell_count"]
    control_mean = samples_data[control_sample]["raw_mean"]

    results = {}
    for sample, data in samples_data.items():
        # Cell count ratio relative to control
        cell_ratio = control_cells / data["cell_count"]
        
        # Corrected plaque mean based on cell count
        corrected_mean = data["raw_mean"] * cell_ratio
        
        # Relative ratio in percentage compared to control
        sample_ratio_pct = (corrected_mean / control_mean) * 100

        results[sample] = {
            "dilution": data["dilution"],
            "raw_mean": data["raw_mean"],
            "cell_count": data["cell_count"],
            "cell_ratio": cell_ratio,
            "corrected_mean": corrected_mean,
            "sample_ratio_pct": sample_ratio_pct
        }

    return results


def display_results(results: dict):
    """Prints the normalized plaque assay table in a compact layout."""
    print("=" * 68)
    print(f"{'Sample':<18} | {'Dil':<4} | {'Mean':<6} | {'Cells':<8} | {'Norm':<5} | {'Corr':<5} | {'Yield'}")
    print("-" * 68)

    for sample, data in results.items():
        print(
            f"{sample:<18} | "
            f"{data['dilution']:<4} | "
            f"{data['raw_mean']:<6.1f} | "
            f"{data['cell_count']:<8.1e} | "
            f"{data['cell_ratio']:<5.2f} | "
            f"{round(data['corrected_mean']):<5} | "
            f"{round(data['sample_ratio_pct'])}%"
        )
    print("=" * 68)


if __name__ == "__main__":
    data_file = "day03/plaque_data.csv"
    results = analyze_plaque_assay(data_file)
    display_results(results)