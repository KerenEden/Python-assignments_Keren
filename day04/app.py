import io
from flask import Flask, render_template_string, request
from plaque_assay import analyze_plaque_assay

app = Flask(__name__)

# Single-page HTML template with upload form and result table
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Plaque Assay Analyzer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f7f9fa; color: #222; }
        .container { max-width: 850px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { margin-top: 0; color: #1a365d; }
        label { display: block; font-weight: bold; margin-top: 15px; }
        input[type="text"], input[type="file"] { width: 100%; padding: 10px; margin-top: 6px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 15px; margin-top: 20px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        table { width: 100%; border-collapse: collapse; margin-top: 25px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #edf2f7; color: #333; }
        .error-box { background-color: #fed7d7; color: #9b2c2c; padding: 12px; border-radius: 4px; margin-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <h1>Plaque Assay Web Platform</h1>
    <p>Upload your experimental CSV file to calculate normalized plaque counts and infection yields.</p>

    <form method="POST" enctype="multipart/form-data">
        <label for="control_name">Control Sample ID:</label>
        <input type="text" id="control_name" name="control_name" value="{{ control_name or 'siNT' }}" required>

        <label for="csv_file">Select CSV File:</label>
        <input type="file" id="csv_file" name="csv_file" accept=".csv" required>

        <button type="submit">Analyze Assay Data</button>
    </form>

    {% if error %}
        <div class="error-box"><strong>Error:</strong> {{ error }}</div>
    {% endif %}

    {% if results %}
        <hr style="margin-top: 30px;">
        <h2>Analysis Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Sample ID</th>
                    <th>Dilution</th>
                    <th>Mean</th>
                    <th>Cell Count</th>
                    <th>Norm Ratio</th>
                    <th>Corrected Mean</th>
                    <th>Yield (%)</th>
                </tr>
            </thead>
            <tbody>
                {% for sample, data in results.items() %}
                <tr>
                    <td><strong>{{ sample }}</strong></td>
                    <td>{{ data.dilution }}</td>
                    <td>{{ data.raw_mean }}</td>
                    <td>{{ "%.1e"|format(data.cell_count) }}</td>
                    <td>{{ data.cell_ratio }}</td>
                    <td>{{ data.corrected_mean }}</td>
                    <td><strong>{{ data.sample_ratio_pct }}%</strong></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    error = None
    control_name = "siNT"

    if request.method == "POST":
        control_name = request.form.get("control_name", "siNT").strip()
        uploaded_file = request.files.get("csv_file")

        if not uploaded_file or uploaded_file.filename == "":
            error = "Please upload a valid CSV file."
        else:
            try:
                # Decode uploaded binary file directly into an in-memory text stream
                content_stream = io.StringIO(
                    uploaded_file.stream.read().decode("utf-8-sig"), newline=None
                )
                # Pass the stream to the business logic function from plaque_assay.py
                results = analyze_plaque_assay(
                    content_stream, control_sample=control_name
                )
            except Exception as exc:
                error = str(exc)

    return render_template_string(
        HTML_TEMPLATE, results=results, error=error, control_name=control_name
    )


if __name__ == "__main__":
    app.run(port=5001)
    
