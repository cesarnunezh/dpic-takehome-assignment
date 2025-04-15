from dpic_takehome.dashboard import app
from dpic_takehome.data_pipeline import cleaning, data_to_db
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://localhost:8050")

if __name__ == "__main__":
    cleaning.main()
    data_to_db.main()
    app.app.run(debug=False)
    Timer(1, open_browser).start()
    app.app.run(debug=False, port = '8050')