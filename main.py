from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecretkey"
app.config["UPLOAD_FOLDER"] = "static/files"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()  # Adds Upload File Form into the html file (Choose/Upload File buttons)

    # Controls what happens when we submit the form 
    if form.validate_on_submit():
        file = form.file.data   # First grab the file uploaded
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))  # Then Save the file 
        
        # Store the name of the most recent file in a session variable
        session['recent_file'] = secure_filename(file.filename)
        
        return redirect(url_for("prompt"))
        
    return render_template('index.html', form=form)  # Goes into the template folder, find the html file and return its contents


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    if request.method == 'POST':                # Prompts User to a Yes/No form
        choice = request.form['confirm']
        if choice == 'Yes':
            return redirect(url_for('user_inputs'))
        else:
            return redirect(url_for('home'))    # Redirect to 'index.html' when the user selects "No"
        
    return render_template('popup.html')


@app.route('/user_inputs', methods=['GET', 'POST'])
def user_inputs():
    if request.method == 'POST' and 'submit_inputs' in request.form:        # Creates user input field
        # Store user inputs in session variables
        session['input1'] = request.form['input1']
        session['input2'] = request.form['input2']
        session['input3'] = request.form['input3']
        session['input4'] = request.form['input4']

        # Run DataProject.py with the name of the most recent file and user inputs
        recent_file = session.get('recent_file')
        input1 = session.get('input1')
        input2 = session.get('input2')
        input3 = session.get('input3')
        input4 = session.get('input4')

        if recent_file:
            # Pass the user inputs as command-line arguments to DataProject.py                      # Extra "quotations" allows the use of spaces
            cmd = f"python DataProject.py {os.path.join(app.config['UPLOAD_FOLDER'], recent_file)} \"{input1}\" \"{input2}\" \"{input3}\" \"{input4}\""     
            os.system(cmd)
            
            # After generating the bar graph, redirect to the page to display it
            return redirect(url_for('display_bar_graph'))

        return redirect(url_for('home'))
    
    return render_template('user_inputs.html')


@app.route('/display_bar_graph')
def display_bar_graph():
    # The file path for the generated bar graph
    graph_path = "/home/asyed_13/AaribProjects/DataProject/static/images/Bar Graph.png"

    # Render the template with the bar graph image path
    return render_template('display_graph.html', graph_path=graph_path)

if __name__ == "__main__":
    app.run(debug=True)

