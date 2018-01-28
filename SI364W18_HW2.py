## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album = StringField('Enter the name of an album:', validators=[Required()])
	rating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')

@app.route('/artistinfo', methods=['GET', 'POST'])
def artist_info():
	if request.method == 'GET':
		to_search = request.args['artist']
		search_results = requests.get('https://itunes.apple.com/search?entity=song&term=' + to_search).json()
		return render_template('artist_info.html', objects=search_results['results'])

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_song(artist_name):
	song_results = requests.get('https://itunes.apple.com/search?entity=song&term=' + artist_name).json()
	return render_template('artist_info.html', objects=song_results['results'])

@app.route('/album_entry')
def album_entry():
	album_form = AlbumEntryForm()
	return(render_template('album_entry.html', form=album_form))

@app.route('/album_result', methods=['GET', 'POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		album = form.album.data
		rating = form.rating.data
		return (render_template('album_result.html', album=album, rating=rating))
	flash('ERROR -- All fields are required.')
	return(redirect(url_for('album_entry')))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
