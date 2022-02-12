from app import app
from api.api_setup import api_loader

# Loads the API into the Flask APP
api_loader(app)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])