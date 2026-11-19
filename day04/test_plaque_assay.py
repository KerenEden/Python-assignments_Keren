import io
import os
import sys
import pytest

# Allow importing plaque_assay from the same directory regardless of where pytest is run
sys.path.insert(0, os.path.dirname(__file__))

from plaque_assay import analyze_plaque_assay


def test_standard_calculations():
    """Verify mean, cell normalization ratio, corrected mean, and yield percentage."""
    # 1. Arrange: Create simple fake CSV data in memory with known mathematical outcomes
    csv_data = io.StringIO(
        "sample_id,dilution,rep1,rep2,rep3,cell_count\n"
        "siNT,-4,40,50,60,200000\n"
        "siGeneX,-4,10,15,20,100000\n"
    )

    # 2. Act: Run the business logic function on the fake data
    results = analyze_plaque_assay(csv_data)

    # 3. Assert: Verify the control sample (siNT) metrics
    assert results["siNT"]["raw_mean"] == 50.0
    assert results["siNT"]["cell_ratio"] == 1.0
    assert results["siNT"]["corrected_mean"] == 50
    assert results["siNT"]["sample_ratio_pct"] == 100

    # Verify the treated sample (siGeneX): mean is 15 with half the cells -> corrected mean is 30 (60% of control)
    assert results["siGeneX"]["raw_mean"] == 15.0
    assert results["siGeneX"]["cell_ratio"] == 2.0
    assert results["siGeneX"]["corrected_mean"] == 30
    assert results["siGeneX"]["sample_ratio_pct"] == 60


def test_custom_control_sample():
    """Verify that a custom control sample name works properly instead of the default 'siNT'."""
    csv_data = io.StringIO(
        "sample_id,dilution,rep1,rep2,rep3,cell_count\n"
        "Mock,-3,80,80,80,100000\n"
        "Treated,-3,20,20,20,100000\n"
    )

    results = analyze_plaque_assay(csv_data, control_sample="Mock")

    assert results["Mock"]["sample_ratio_pct"] == 100
    assert results["Treated"]["sample_ratio_pct"] == 25


def test_missing_control_raises_error():
    """Verify that a ValueError is raised when the specified control sample is missing."""
    csv_data = io.StringIO(
        "sample_id,dilution,rep1,rep2,rep3,cell_count\n"
        "SampleA,-4,30,30,30,150000\n"
    )

    with pytest.raises(ValueError, match="not found"):
        analyze_plaque_assay(csv_data, control_sample="siNT")


def test_zero_cell_count():
    """Verify that a cell count of zero does not cause a ZeroDivisionError."""
    csv_data = io.StringIO(
        "sample_id,dilution,rep1,rep2,rep3,cell_count\n"
        "siNT,-4,50,50,50,200000\n"
        "DeadCells,-4,10,10,10,0\n"
    )

    results = analyze_plaque_assay(csv_data)

    assert results["DeadCells"]["cell_ratio"] == 0.0
    assert results["DeadCells"]["corrected_mean"] == 0
    assert results["DeadCells"]["sample_ratio_pct"] == 0