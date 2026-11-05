# Day 03: Plaque Assay Cell-Count Normalization

## Overview
This program automates the calculation of relative viral plaque counts across siRNA knockdown conditions (`siNT` control vs `siTarget_protein`), normalizing plaque yields to the actual harvested cell count.

## Experimental Workflow & Math
1. **Raw Mean**: Calculates the average plaque count from technical triplicates:
   $$\text{Mean} = \frac{\text{rep1} + \text{rep2} + \text{rep3}}{3}$$
2. **Cell Normalization Ratio**:
   $$\text{Ratio} = \frac{\text{Cell Count}_{\text{control}}}{\text{Cell Count}_{\text{sample}}}$$
3. **Corrected Mean**:
   $$\text{Corrected Mean} = \text{Raw Mean} \times \text{Ratio}$$
4. **Sample Ratio (%)**:
   $$\text{Relative Yield (\%)} = \left(\frac{\text{Corrected Mean}_{\text{sample}}}{\text{Raw Mean}_{\text{control}}}\right) \times 100$$

## Files
- `plaque_calculator.py`: Python script performing normalization and relative yield calculations.
- `plaque_data.csv`: Plaque triplicates and corresponding cell count data.

## How to Run
Run via terminal or the VS Code Play button:
```bash
py day03/plaque_calculator.py

## AI Prompts Used
1. "Write a Python script that reads plaque assay triplicates and cell counts for control and siRNA knockdown samples from a CSV file."
2. "Compute raw mean, normalize plaque counts using the cell count ratio between samples, and calculate relative infection percentage."
3. "Format the output as a neat terminal table matching standard laboratory reporting."
