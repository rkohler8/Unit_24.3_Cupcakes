"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

# @app.route('/')
# def index_page():
   # todos = Todo.query.all()
   # return render_template('index.html', todos=todos)

# GET /api/cupcakes
# Get data about all cupcakes.

# Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.

# The values should come from each cupcake instance.

@app.route('/api/cupcakes')
def list_cupcakes():
   all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
   return jsonify(cupcakes=all_cupcakes)


# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.

# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

# This should raise a 404 if the cupcake cannot be found.

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
   cupcake = Cupcake.query.get_or_404(id)
   return jsonify(cupcake=cupcake.serialize())


# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.

# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

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