from dpic_takehome.dashboard import app
from dpic_takehome.data_pipeline import cleaning, data_to_db
from pathlib import Path

if __name__ == "__main__":
    cleaning.main()
    data_to_db.main()
    app.app.run(debug=True)