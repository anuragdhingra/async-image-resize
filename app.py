from api import create_app

def run():
    app = create_app()
    app.run(host="0.0.0.0", port=5000,use_reloader=True)

if __name__ == "__main__":
    run()