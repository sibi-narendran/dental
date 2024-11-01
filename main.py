from app import app
import routes  # noqa: F401
from demo_data import create_demo_data

if __name__ == "__main__":
    # Reset demo data on each server start
    create_demo_data()
    app.run(host="0.0.0.0", port=5000)
