# Stop bij fouten
set -e

VENV_DIR=".venv"

# Check of script gesourced wordt
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "⚠️  Run dit script met: source $0"
  exit 1
fi

# Maak venv als die nog niet bestaat
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Virtual environment aanmaken..."
  python3 -m venv "$VENV_DIR"
else
  echo "✅ Virtual environment bestaat al."
fi

# Activeer venv
echo "🚀 Virtual environment activeren..."
source "$VENV_DIR/bin/activate"

# Installeer dependencies (optioneel)
if [ -f "requirements.txt" ]; then
  echo "📦 Dependencies installeren..."
  pip install -r requirements.txt
fi

echo "🎉 Klaar! Je venv is actief."