from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
import model
import config

app = Flask(__name__)
app.config.from_object(config)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
