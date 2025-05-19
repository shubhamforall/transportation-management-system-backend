# Add terminal color and decoding
printf '\033[5;35m'
base64 -d './config/name_base64.txt'
printf '\033[0m'

# === Ensure logs directory and log file exist ===
file_path="./logs/invoice.log"

if [ ! -f "$file_path" ]; then
  echo "Creating logs directory and invoice.log..."
  mkdir -p "./logs"            
  touch "$file_path"
fi

# === Run Django server ===
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
