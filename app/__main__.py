from app import app, configini

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configini['DEFAULT']['port'])
