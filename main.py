from flask import Flask, jsonify, render_template, request
from sqlalchemy.sql import functions
from sqlalchemy import exists
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from forms import CafeForm
from tables import db


nc = "\033[0;97m"
red = "\033[0;91m"
green = "\033[0;92m"
blue = "\033[0;96m"
yellow = "\033[0;93m"
lilac = "\033[0;95m"

# organising the database in separate form, inspiration from:
# https://stackoverflow.com/questions/56712921/access-db-from-a-separate-file-flask-sqlalchemy-python3
# https://www.reddit.com/r/flask/comments/mbhqnm/use_sqlalchemy_database_from_another_file/
# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045


app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
db.init_app(app)


# def get_selected_cafes(loc):
#     cafes = db.session.execute(db.select(Cafe).filter_by(location=loc)).scalars()
#     all_cafees = []
#     print("--------------------------------------------")
#     for kafe in cafes:
#         thiscafe = {
#             'id': kafe.id,
#             'name': kafe.name,
#             'map_url': kafe.map_url,
#             'img_url': kafe.img_url,
#             'location': kafe.location,
#             'seats': kafe.seats,
#             'has_toilet': kafe.has_toilet,
#             'has_wifi': kafe.has_wifi,
#             'has_sockets': kafe.has_sockets,
#             'can_take_calls': kafe.can_take_calls,
#             'coffee_price': kafe.coffee_price
#         }
#         all_cafees.append(thiscafe)
#     if not all_cafees:
#         return {"error": "you're a twat!"}
#     else:
#         return jsonify(all_cafees)
#
# print(get_selected_cafes('Peckham'))

# def add_new_cafe(new_cafe):
#     with app.app_context():
#         db.session.add(new_cafe)
#         db.session.commit()


# def get_locations():
#     # locations = [r.useremail for r in db.session.query(Cafe.location).distinct()]
#     # locations = [r.useremail for r in db.session.execute(db.select(Cafe.location).distinct())]
#     # result = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()
#     # print(f"locations={locations}")
#     with app.app_context():



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all", methods=["GET"])
def all_cafes():
    result = db.session.execute(db.select(Cafe.location).order_by(Cafe.location).distinct()).scalars()
    locations = [loc for loc in result]
    print(locations)
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()
    cafes = [cafe.to_list() for cafe in result]
    return render_template('cafes.html', cafes=cafes, titles=get_column_titles(), locations=locations)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    print(f"in add cafe, method={request.method}")
    if form.validate_on_submit():
        print(f"form did validate")
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('all_cafes'))
    else:
        return render_template('add.html', form=form)


@app.route("/delete/<cafe_id>")
def delete_cafe(cafe_id):
    print(f"in delete: method={request.method}")
    apikey = request.args.get('apikey')
    print(f"{yellow}apikey={apikey}, cafe_id={cafe_id} {nc}")
    is_record = db.session.query(exists().where(Cafe.id == cafe_id)).scalar()
    if is_record:
        print(f"in delete: cafeid={cafe_id}, apikey={apikey}")
        if apikey == "tubularbells":
            cafe = Cafe.query.get(cafe_id)
            db.session.delete(cafe)
            db.session.commit()
            print(f"{yellow}record should have been deleted{nc}")
        else:
            print(f"{yellow}wrong apikey, cunt!{nc}")
    else:
        print(f"{yellow}record does not exits, you fuck{nc}")
    return redirect(url_for('all_cafes'))


@app.route("/edit", methods=["GET", "POST"])
def edit_cafe():
    cafe_id = request.args.get('cafe_id')
    print(f"cafeid={cafe_id}")
    form = CafeForm()
    print(f"in edit_cafe, method={request.method}")
    cafe = db.session.get(Cafe, cafe_id)

    print(f"edit_cafe, cafe={cafe}")
    if form.validate_on_submit():
        print(f"form did validate")
        cafe.name = request.form.get("name")
        cafe.map_url = request.form.get("map_url")
        cafe.img_url = request.form.get("img_url")
        cafe.location = request.form.get("location")
        cafe.seats = request.form.get("seats")
        cafe.has_toilet = bool(request.form.get("toilet"))
        cafe.has_wifi = bool(request.form.get("wifi"))
        cafe.has_sockets = bool(request.form.get("sockets"))
        cafe.can_take_calls = bool(request.form.get("calls"))
        cafe.coffee_price = request.form.get("coffee_price")

        db.session.commit()
        return redirect(url_for('all_cafes'))
    else:
        # how to pre-populate fields on a flaskform
        # https://stackoverflow.com/questions/69529247/how-do-i-pre-fill-a-flask-wtforms-form-with-existing-data-for-an-edit-profile
        form.name.data = cafe.name
        form.map_url.data = cafe.map_url
        form.img_url.data = cafe.img_url
        form.location.data = cafe.location
        form.seats.data = cafe.seats
        form.has_toilet.data = cafe.has_toilet
        form.has_wifi.data = cafe.has_wifi
        form.has_sockets.data = cafe.has_sockets
        form.can_take_calls.data = cafe.can_take_calls
        form.coffee_price.data = cafe.coffee_price
        return render_template('edit.html', form=form, cafe=cafe)


@app.route("/sort/<by>")
def sort(by):
    fuckit = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()
    print(f"sortby={by}")
    if by == 'Cafe Name':
        fuckit = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()
    elif by == 'Location':
        fuckit = db.session.execute(db.select(Cafe).order_by(Cafe.location)).scalars()
    elif by == 'Coffee Price':
        fuckit = db.session.execute(db.select(Cafe).order_by(Cafe.location)).scalars()

    cafes = [cafe.to_list() for cafe in fuckit]
    return render_template('cafes.html', cafes=cafes, titles=get_column_titles())


@app.route("/filter_location", methods=["GET"])
def filter_location():
    loc = request.args.get('lstlocations')
    print(f"in filter, loc={loc}")
    # locations = request.args.get('locations')
    fuckit = db.session.execute(db.select(Cafe).where(Cafe.location == loc).order_by(Cafe.name)).scalars()
    cafes = [cafe.to_list() for cafe in fuckit]
    print(f"in filter, cafes={cafes}")
    result = db.session.execute(db.select(Cafe.location).order_by(Cafe.location).distinct()).scalars()
    locations = [loc for loc in result]
    return render_template('cafes.html', cafes=cafes, titles=get_column_titles(), locations=locations)

# @app.route("/fok/<id>", methods=["GET", "POST"])
# def fok(id):
#     form = CafeForm()
#     print(f"in add cafe, method={request.method}")
#     if form.validate_on_submit():
#         print(f"form did validate")
#         new_cafe = Cafe(
#             name=request.form.get("name"),
#             map_url=request.form.get("map_url"),
#             img_url=request.form.get("img_url"),
#             location=request.form.get("location"),
#             has_sockets=bool(request.form.get("sockets")),
#             has_toilet=bool(request.form.get("toilet")),
#             has_wifi=bool(request.form.get("wifi")),
#             can_take_calls=bool(request.form.get("calls")),
#             seats=request.form.get("seats"),
#             coffee_price=request.form.get("coffee_price"),
#         )
#
#         db.session.add(new_cafe)
#         db.session.commit()
#         return redirect(url_for('all_cafes'))
#     else:
#         return render_template('add.html', form=form)





if __name__ == '__main__':
    from tables import Cafe, get_column_titles

    # db.create_all()
    app.run(debug=True, port=5001)

