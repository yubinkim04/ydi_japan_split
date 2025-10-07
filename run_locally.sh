echo "Starting..."
echo "Installing system dependencies..."

python3 -m venv split
source split/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Virtual environment setup complete!"

python3 calc.py

echo "Script execution complete! Delete the virtual environment if not needed."
