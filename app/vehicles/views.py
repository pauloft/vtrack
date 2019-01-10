# app/vehicles/views.py

from flask import (
    render_template,
    redirect,
    current_app,
    request,
    flash,
    url_for,
    jsonify,
)
from werkzeug.utils import secure_filename
from flask_login import login_required

from . import vehicles
from app.vehicles.forms import VehicleForm
from app import db
from app.models import Vehicle, Picture
from app.auth.utils import processImage


def create_picture(form_picture_data):
    target_dir = current_app.config["VEHICLE_IMAGE_FOLDER"]
    saved_name = processImage(form_picture_data, target_dir)
    picture = Picture(
        filepath=saved_name, origpath=secure_filename(form_picture_data.filename)
    )
    return picture


@vehicles.route("/", methods=["GET", "POST"])
@login_required
def index():
    """ List all vehicles """

    # create the form object
    form = VehicleForm()

    # handle post requests
    # if form.validate_on_submit():
    if request.method == "POST":
        # if we are editing/updting, the form vid field ie empty
        vin = form.vin.data
        tag = form.tag.data
        year = form.year.data
        make = form.make.data
        model = form.model.data

        # check for picture upload
        picture = None
        if form.picture.data:
            picture_data = form.picture.data
            picture = create_picture(picture_data)

        # A vehicle id is set if updating a record; blank for new record
        if request.form["vid"] == "":
            vehicle = Vehicle(vin=vin, tag=tag, year=year, make=make, model=model)
            db.session.add(vehicle)
            if picture:
                vehicle.pictures.append(picture)
            flash("The vehicle has been saved to the database.")
        else:
            vid = request.form["vid"]
            vehicle = Vehicle.query.get(vid)
            vehicle.vin = vin
            vehicle.tag = tag
            vehicle.year = year
            vehicle.make = make
            vehicle.model = model

            if picture:
                vehicle.pictures.append(picture)
            flash("The vehicle record has been updated.")

        db.session.commit()

    # get the pagination data to show the page
    page = request.args.get("p", 1, type=int)
    per_page = current_app.config["ITEMS_PER_PAGE"]
    vehicles = Vehicle.query.order_by(Vehicle.id.desc()).paginate(
        page=page, per_page=per_page
    )
    return render_template(
        "vehicles/index.html", title="Vehicle Cards", form=form, vehicles=vehicles
    )


@vehicles.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    """ Delete a vehicle and it's pictures!! """
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    flash(f"The {vehicle.year} {vehicle.make} {vehicle.model} was successfully deleted!")

    return redirect(url_for("vehicles.index"))


@vehicles.route("/getVehicleById", methods=["POST"])
@login_required
def getVehicleById():
    """ fetch a vehicle record from the database so it can be used to populate form fields
    """
    id = request.form["id"]
    vehicle = Vehicle.query.get(id)

    return jsonify(
        dict(
            id=vehicle.id,
            vin=vehicle.vin,
            tag=vehicle.tag,
            year=vehicle.year,
            make=vehicle.make,
            model=vehicle.model,
        )
    )


@vehicles.route('/album/<int:id>')
@login_required
def album(id):
    pics = Vehicle.query.filter_by(id=id).first().pictures

    pictures = [p.filepath for p in pics]

    return render_template('vehicles/album.html', title="Album", pictures=pictures)
