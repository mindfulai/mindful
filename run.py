# Run server
from app import app

app.run(ssl_context='adhoc', debug=True, host="0.0.0.0", port=5000)
