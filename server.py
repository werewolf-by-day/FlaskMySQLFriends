from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friends')

@app.route('/')
def index():
    query = "SELECT friends.name, friends.age, DATE_FORMAT(friends.friend_since, '%M %D %Y') as friend_since FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    #friends_since = DATE_FORMAT(friends.friends_since, '%M %D %Y') 
    print mysql.query_db("SELECT * FROM friends")
    return render_template('index.html', all_friends=friends) # pass data to our template

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])


@app.route('/friends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO friends (name, age, friend_since) VALUES (:name, :age, NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'name': request.form['name'],
             'age':  request.form['age'],
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/update_friend/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET name = :name, age = :age, friend_since = :friend_since WHERE id = :id"
    data = {
             'name': request.form['name'],
             'age':  request.form['age'],
             'friend_since': request.form['friend_since'],
             'id': friend_id
           }
    mysql.query_db(query, data)
    return redirect('/')


app.run(debug=True)
