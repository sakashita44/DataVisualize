# To generate the graph, run this script.

# Move to the directory where this script is located
Set-Location $PSScriptRoot

# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Execute graph_generator.py
python .\src\graph_generator.py
