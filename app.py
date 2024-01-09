"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)

@app.route('/')
def index_page():
   """Generate Homepage"""

   cupcakes = Cupcake.query.all()
   return render_template('index.html', cupcakes=cupcakes)

# GET /api/cupcakes
# Get data about all cupcakes.

# Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.

# The values should come from each cupcake instance.

@app.route('/api/cupcakes')
def list_cupcakes():
   """Lists all current cupcakes"""

   all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
   return jsonify(cupcakes=all_cupcakes)


# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.

# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

# This should raise a 404 if the cupcake cannot be found.

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
   """Displays details of a specified cupcake"""

   cupcake = Cupcake.query.get_or_404(id)
   return jsonify(cupcake=cupcake.serialize())


# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.

# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
   """Creates and adds a new cupcake to the DB"""
   data=request.json

   new_cupcake = Cupcake(flavor=data["flavor"], 
                         rating=data["rating"], 
                         size=data["size"], 
                         image=data["image"] or None)
   
   db.session.add(new_cupcake)
   db.session.commit()

   response_json = jsonify(cupcake=new_cupcake.serialize())
   return (response_json, 201)
   # return (jsonify(todo=new_todo.serialize()), 201)
   # print(request.json)


# PATCH /api/cupcakes/[cupcake-id]
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. 
# You can always assume that the entire cupcake object will be passed to the backend.

# This should raise a 404 if the cupcake cannot be found.

# Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
   """Updates and edits a cupcake in the DB"""

   cupcake = Cupcake.query.get_or_404(id)
   data=request.json

   cupcake.flavor = data.get('flavor', cupcake.flavor)
   cupcake.size = data.get('size', cupcake.size)
   cupcake.rating = data.get('rating', cupcake.rating)
   cupcake.image = data.get('image', cupcake.image)

   db.session.commit()
   return jsonify(cupcake=cupcake.serialize())


# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.

# Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.

# Test these routes in Insomnia.

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
   """Deletes and removes a cupcake from the DB"""

   cupcake = Cupcake.query.get_or_404(id)
   db.session.delete(cupcake)
   db.session.commit()
   return jsonify(message="deleted")