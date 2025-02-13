"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app,db
from flask import render_template, request, redirect, url_for,flash,session, abort,send_from_directory
from app.forms import PropertyForm
from app.models import PropertyProfile
from werkzeug.utils import secure_filename
from app.config import *


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")



@app.route("/property", methods=["GET","POST"])
def property():
    form = PropertyForm()
    ptype = ['House', 'Apartment']
    if request.method == "POST":
        if form.validate_on_submit:
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            #print(filename)
            photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
            ))

            user = PropertyProfile(ptitle = form.ptitle.data, pdescription = form.description.data, rooms=form.rooms.data,
            bathrooms=form.bathrooms.data,price=form.price.data,ptype=form.ptype.data,location=form.location.data,filename=filename)
            db.session.add(user)
            db.session.commit()
            flash("Property Added")
            return redirect(url_for("properties"))

        else:
            flash("Something went wrong.Try Again")


    
    return render_template("property.html",form=form,ptype=ptype)


@app.route("/properties")
def properties():
    users = PropertyProfile.query.all()
    return render_template("properties.html", users=users)



@app.route("/images/<filename>")
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(rootdir + "/" + app.config['UPLOAD_FOLDER'],
filename)


@app.route("/property/<propertyid>")
def viewproperty(propertyid):
    user = PropertyProfile.query.get(propertyid)
    return render_template("viewproperty.html",user=user)



###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
