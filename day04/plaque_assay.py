import csv
import io
import os
import statistics


def analyze_plaque_assay(csv_source, control_sample: str = "siNT") -> dict:
    """Calculates normalized infection yields from a CSV file path or file stream.

    Parameters:
    - csv_source: A file path string OR an open file-like text stream.
    - control_sample: Identifier string for the control condition (default: 'siNT').

    Returns:
    - dict: Processed metrics for each sample.
    """
    # Check whether csv_source is a file path string or an already open stream
    if isinstance(csv_source, str):
        with open(csv_source, mode="r", encoding="utf-8") as file:
            return _parse_and_calculate(file, control_sample)
    else:
        return _parse_and_calculate(csv_source, control_sample)


def _parse_and_calculate(file_object, control_sample: str) -> dict:
    """Internal helper that performs the data parsing and math calculations."""
    reader = csv.DictReader(file_object)
    samples_data = {}

    for row in reader:
        sample = row["sample_id"].strip()
        replicates = [
            float(row["rep1"]),
            float(row["rep2"]),
            float(row["rep3"]),
        ]
        cell_count = float(row["cell_count"])

        raw_mean = statistics.mean(replicates)
        samples_data[sample] = {
            "dilution": row["dilution"].strip(),
            "raw_mean": raw_mean,
            "cell_count": cell_count,
        }

    if control_sample not in samples_data:
        raise ValueError(
            f"Control sample '{control_sample}' not found in the dataset."
        )

    control_cells = samples_data[control_sample]["cell_count"]
    control_mean = samples_data[control_sample]["raw_mean"]

    results = {}
    for sample, data in samples_data.items():
        cell_ratio = (
            control_cells / data["cell_count"]
            if data["cell_count"] > 0
            else 0.0
        )
        corrected_mean = data["raw_mean"] * cell_ratio
        sample_ratio_pct = (
            (corrected_mean / control_mean) * 100 if control_mean > 0 else 0.0
        )

        results[sample] = {
            "dilution": data["dilution"],
            "raw_mean": round(data["raw_mean"], 1),
            "cell_count": data["cell_count"],
            "cell_ratio": round(cell_ratio, 2),
            "corrected_mean": round(corrected_mean),
            "sample_ratio_pct": round(sample_ratio_pct),
        }

    return results


def display_results(results: dict) -> None:
    """Prints the normalized plaque assay table to the terminal."""
    print("=" * 68)
    print(
        f"{'Sample':<18} | {'Dil':<4} | {'Mean':<6} | {'Cells':<8} | {'Norm':<5} | {'Corr':<5} | {'Yield'}"
    )
    print("-" * 68)

    for sample, data in results.items():
        print(
            f"{sample:<18} | "
            f"{data['dilution']:<4} | "
            f"{data['raw_mean']:<6.1f} | "
            f"{data['cell_count']:<8.1e} | "
            f"{data['cell_ratio']:<5.2f} | "
            f"{data['corrected_mean']:<5} | "
            f"{data['sample_ratio_pct']}%"
        )
    print("=" * 68)


# Terminal interface (Old System runner)
if __name__ == "__main__":
    # Look for the CSV file in the current folder, fallback to day03
    data_file = (
        "plaque_data.csv"
        if os.path.exists("plaque_data.csv")
        else "day03/plaque_data.csv"
    )

    print(f"Reading data from: {data_file}")
    output = analyze_plaque_assay(data_file)
    display_results(output)