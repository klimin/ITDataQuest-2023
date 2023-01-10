from waitress import serve
from runner import app

serve(app, host='0.0.0.0', port=2023, threads=6)