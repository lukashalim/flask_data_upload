import os

from flask import Flask, render_template, request, redirect, url_for, abort, flash
import pandas as pd
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'upload_for_analysis.sqlite'),
    )
    app.config['upload_folder'] = 'C:\\Users\\Acer\\Dropbox\\flask_data_upload\\uploads'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # a simple upload page
    @app.route("/", methods=['GET','POST'])
    def index():
        if request.method == 'POST':
            delimiter = request.form['delimiter']
            file = request.files['file']
            filename = file.filename
            if filename != "":
                flash(filename)
                return redirect(url_for('uploaded', my_var='my_value'))
            else:
                flash('No selected file')
                return redirect(request.url)
        else:
            return render_template('index.html')

    @app.route("/uploaded", methods=['POST'])
    def uploaded():
        delimiter = request.form['delimiter']
        quoted, header = "", ""
        if request.form.get('quoted'):
            quoted = "quoted"
        if request.form.get('header'):
            header = "header"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            filename = file.filename
            path_and_file = os.path.join(app.config['upload_folder'], filename)
            file.save(path_and_file)
            df = pd.read_csv(path_and_file, delimiter=delimiter)
            return render_template('/uploaded.html', df=df,filename=filename, delimiter=delimiter)

    from upload_for_analysis.db import get_db

    @app.route("/save_settings", methods=['POST'])
    def save_settings():
        path_and_file = os.path.join(app.config['upload_folder'], request.form['filename'])
        delimiter=request.form['delimiter']
        print(f"path and file: {path_and_file}")
        print(f"delimiter : {delimiter}")
        columns = pd.read_csv(path_and_file).columns
        db = get_db()
        cursor = db.cursor()
        #db.execute(
        #    'INSERT INTO file (filename, delimiter)'
        #    ' VALUES (?, ?)',
        #    (request.form['filename'], delimiter)
        #)
        cursor.execute('INSERT INTO file (filename, delimiter) VALUES (?, ?)', (request.form['filename'], delimiter))
        file_id = cursor.lastrowid
        for column in columns:
            cursor.execute('INSERT INTO fieldsettings (file_id, column_name, column_type) VALUES (?, ?, ?)', (cursor.lastrowid,column,request.form[column]))
        db.commit()
        return "saved"

    return app


