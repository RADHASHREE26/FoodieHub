from flask import Flask, render_template, request, flash, redirect, session,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

app=Flask(__name__)
client=MongoClient("mongodb://localhost:27017")
db=client.foodiehub
logging.basicConfig(filename='record.log',level=logging.DEBUG)
app.secret_key='1234'

coll=db.user_det
admin_coll=db.admin
restaurants_coll=db.restaurants

@app.route("/")
@app.route("/home")
@app.route("/home/<username>")
def home(username=""):
    app.logger.error('ERROR')
    return render_template("index.html")

# @app.route("/signup", methods=('GET', 'POST'))
# def signup():
#     if request.method=='POST':
#         name=request.form['fullname']
#         email=request.form['email']
#         pw=request.form['password']
#         coll.insert_one({'name':name, 'email':email, 'password':pw, 'followers':[], 'following':[], 'blogs':[]})
#         flash('Registered successfully. Continue to login')
#         app.logger.info(f'New user {name} signed in')
#         return redirect('/login')
#     return render_template("signup.html")

@app.route("/signup", methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        pw = request.form['password']
        try:
            coll.insert_one({'name': name, 'email': email, 'password': pw,
                             'followers': [], 'following': [], 'blogs': []})
        except Exception as e:
            app.logger.error(f'Error inserting user {name} into MongoDB: {e}')
            flash('Error occurred during registration. Please try again.')
            return redirect('/signup')

        flash('Registered successfully. Continue to login')
        app.logger.info(f'New user {name} signed in')
        return redirect('/login')
    return render_template("signup.html")


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = coll.find_one({'name': username, 'password': password})
#         admin = admin_coll.find_one({'name': username, 'password': password})
#         if admin:
#             flash('Welcome Admin')
#             session['user_id'] = str(admin['_id'])  # Convert ObjectId to string
#             session['name']='admin'
#             app.logger.info('Admin logged in')
#             return redirect("/home/admin")
#         elif user:
#             flash('Welcome, {}!'.format(username))
#             session['user_id'] = str(user['_id'])  # Convert ObjectId to string
#             session['name']=username
#             app.logger.info(f'{username} logged in')
#             return redirect("/home")
#         else:
#             flash('Invalid credentials. Please try again.')
#             app.logger.info(f'Credentials: username: {username} , password: {password} are unmatched credentials')
#             return redirect('/login')
#     return render_template("login.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = coll.find_one({'name': username, 'password': password})
            admin = admin_coll.find_one({'name': username, 'password': password})
        except Exception as e:
            app.logger.error(f'Error occurred while querying MongoDB for user login: {e}')
            flash('Internal Error Occured. Please try again.')
            return redirect('/login')

        if admin:
            flash('Welcome Admin')
            session['user_id'] = str(admin['_id'])  # Convert ObjectId to string
            session['name']='admin'
            app.logger.info('Admin logged in')
            return redirect("/home/admin")
        elif user:
            flash('Welcome, {}!'.format(username))
            session['user_id'] = str(user['_id'])  # Convert ObjectId to string
            session['name']=username
            app.logger.info(f'{username} logged in')
            return redirect("/home")
        else:
            flash('Invalid credentials. Please try again.')
            app.logger.info(f'Credentials: username: {username} , password: {password} are unmatched credentials')
            return redirect('/login')
    return render_template("login.html")


@app.route('/profile')
def profile(user=""):
    user_id = session.get('user_id')
    user=db.user_det.find_one({'_id':ObjectId(user_id)})
    return render_template('profile.html', user=user)

@app.route('/restaurants')
def restaurants():
    # Fetch all restaurants from MongoDB collection
    restaurants = db.restaurants.find()
    # Render HTML template and pass in the restaurant data
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/home/admin')
def admin_home():
    return render_template('admin_home.html')

@app.route('/admin_restaurants')
def admin_restaurant():
    restaurants = db.restaurants.find()
    return render_template('admin_restaurant.html', restaurants=restaurants)

# @app.route("/contact")
# def contact():

@app.route('/admin_restaurants#add-restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        description = request.form['description']
        location=request.form['location']
        menu=request.form['menu']
        image = request.form['image']
        # Insert data into MongoDB collection
        restaurants.insert_one({
            'name': name,
            'description': description,
            'location': location,
            'menu': menu,
            'image': image
        })
        # Redirect to home page
        flash('Restaurant added successful')
        return render_template('admin_admin.html')
    else:
        # Render add restaurant page
        flash('unsuccessful')
        return render_template('admin_admin.html')

# @app.route('/add-restaurant', methods=('GET', 'POST'))
# def add_res():
#     if request.method=='POST':
#         name=request.form['restaurant-name']
#         des=request.form['restaurant-description']
#         image=request.form['restaurant-image']
#         restaurants_coll.insert_one({'name':name, 'des':des, 'image':image, 'reviews':[]})
#         return "success"
#     return render_template("add_restaurants.html")

# @app.route('/remove_res', methods=('GET', 'POST'))
# def remove_res():
#     if request.method=='POST':
#         name=request.form['restaurant-name']
#         res=restaurants_coll.delete_one({'name':name})
#         if res.deleted_count==1:
#             flash('Restaurant removed successfully')
#             return redirect('/admin_restaurants')
#         else:
#             flash('Restaurant not found')
#             return redirect('/admin_restaurants')
#     return render_template('remove_res.html')


@app.route('/add-restaurant', methods=('GET', 'POST'))
def add_res():
    if request.method == 'POST':
        try:
            name = request.form['restaurant-name']
            des = request.form['restaurant-description']
            location=request.form['restaurant-location']
            menu=request.form['restuarant-menu']
            image = request.form['restaurant-image']
            restaurants_coll.insert_one({'name': name, 'des': des, 'location': location, 'menu':menu, 'image': image, 'reviews': []})
        except Exception as e:
            app.logger.error(f'Error occurred while inserting restaurant data into MongoDB: {e}')
            flash('Internal Error Occured. Please try again.')
            return redirect('/add-restaurant')
        return "success"
    return render_template("add_restaurants.html")



@app.route('/remove_res', methods=('GET', 'POST'))
def remove_res():
    if request.method == 'POST':
        try:
            name = request.form['restaurant-name']
            res = restaurants_coll.delete_one({'name': name})
        except Exception as e:
            app.logger.error(f'Error occurred while removing restaurant {name} from MongoDB: {e}')
            flash('Internal Error Occured. Please try again.')
            return redirect('/remove_res')
        if res.deleted_count == 1:
            flash('Restaurant removed successfully')
            return redirect('/admin_restaurants')
        else:
            flash('Restaurant not found')
            return redirect('/admin_restaurants')
    return render_template('remove_res.html')


# @app.route('/remove_user', methods=('GET', 'POST'))
# def remove_user():
#     if request.method=='POST':
#         name=request.form['user-name']
#         res=db.user_det.delete_one({'name':name})
#         if res.deleted_count==1:
#             flash('User removed successfully')
#             return redirect('/home/admin')
#         else:
#             flash('User not found')
#             return redirect('/home/admin')
#     return render_template('remove_user.html')


@app.route('/remove_user', methods=('GET', 'POST'))
def remove_user():
    if request.method == 'POST':
        try:
            name = request.form['user-name']
            res = db.user_det.delete_one({'name': name})
        except Exception as e:
            app.logger.error(f'Error occurred while removing user {name} from MongoDB: {e}')
            flash('Internal Error Occured. Please try again.')
            return redirect('/remove_user')

        if res.deleted_count == 1:
            flash('User removed successfully')
            return redirect('/home/admin')
        else:
            flash('User not found')
            return redirect('/home/admin')
    return render_template('remove_user.html')


# @app.route('/search', methods=['GET','POST'])
# def search():
#     #search_query=request.args.get('query')
#     query = request.form['query']
#     restaurant=restaurants_coll.find_one({'name':query})
#     user=coll.find_one({'name':query})
#     if restaurant:
#         return render_template('restaurant_res.html',restaurant=restaurant)
#     elif user:
#         return render_template('user_res.html',user=user)
#     flash("item not found")
#     return "No results found"


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        try:
            query = request.form['query']
            restaurant = restaurants_coll.find_one({'name': query})
            user = coll.find_one({'name': query})
        except Exception as e:
            app.logger.error(f'Error occurred while searching for {query} in MongoDB: {e}')
            flash('Internal Error Occured. Please try again.')
            return redirect('/search')

        if restaurant:
            return render_template('restaurant_res.html',restaurant=restaurant)
        elif user:
            return render_template('user_res.html',user=user)
        else:
            flash('Item not found')
            return render_template('search.html')
    return render_template('search.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # query = request.args.get('query')
        query = request.form['submitres']
        user_rating = int(request.form['rating'])
        user_review = request.form['review']
        user_id = session.get('user_id')
        restaurant = db.restaurants.find_one({'_id': ObjectId(query)})
        # if 'reviews' not in restaurant:
        #     restaurant['reviews'] = []
        # restaurant['reviews'].append({
        #     'user_id': user_id,
        #     'rating': user_rating,
        #     'review': user_review
        # })
        db.restaurants.update_one({'_id': ObjectId(query)}, {"$push": { "reviews":
            {
            'user_id': user_id,
            'rating': user_rating,
            'review': user_review
            }
        }}, upsert=True)
        return render_template('restaurant_res.html',restaurant=restaurant)


@app.route('/restaurant_res/<res_id>')
def restaurant_res(res_id = ""):
    # Retrieve the restaurant's data
    res = db.restaurants.find_one({'_id': ObjectId(res_id)})

    # Fetch existing comments
    user_reviews = res['reviews']

    # Retrieve user names associated with the comments
    for review in user_reviews:
        user_id = review['user_id'] # <-- update this line
        user = coll.find_one({'_id': ObjectId(user_id)})
        review['user_id'] = user['name'] if user else 'Unknown User'
    return render_template('restaurant_res.html', restaurant=res, reviews=user_reviews)


@app.route('/follow', methods=['GET','POST'])
def follow():
    if request.method == 'POST':
        follower=session.get('user_id')
        followername=session.get('name')
        following=request.form['user_id']
        user1=db.user_det.find_one({'_id':ObjectId(follower)})
        user2=db.user_det.find_one({'name':following})
        if user1 and user2:
            db.user_det.update_one({'_id':ObjectId(follower)}, {"$push": {"following": following}})
            db.user_det.update_one({'name':following}, {"$push": {"followers": followername}})
            flash('Followed')
            return render_template('user_res.html', user=user2, followername=followername)
        else:
            flash('Invalid user. Could not follow')
            return render_template('user_res.html', user=user2, followername=followername)
        
@app.route('/unfollow', methods=['GET','POST'])
def unfollow():
    if request.method == 'POST':
        followername=session.get('name')
        following=request.form['user_id']
        user1=db.user_det.find_one({'name':followername})
        user2=db.user_det.find_one({'name':following})
        if user1 and user2:
            db.user_det.update_one({'name':followername}, {"$pull": {"following": following}})
            db.user_det.update_one({'name':following}, {"$pull": {"followers": followername}})
            flash('Followed')
            return render_template('user_res.html', user=user2, followername=followername)
        else:
            flash('Invalid user. Could not unfollow')
            return render_template('user_res.html', user=user2, followername=followername)
        
@app.route('/submit_blog', methods=['GET','POST'])
def submit_blog():
    if request.method=='POST':
        blog=request.form['blogContent']
        user_id=session.get('user_id')
        user=db.user_det.find_one({'_id':ObjectId(user_id)})
        db.user_det.find_one_and_update({'_id': ObjectId(user_id)}, {"$push": {'blogs': blog}})
        return redirect('/profile')
    return redirect('/profile')

@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    if request.method=='POST':
        user_id=request.form['edit']
        return render_template('edit_profile.html', user=user_id)

@app.route('/update', methods=['GET','POST'])
def update_profile():
    if request.method=='POST':
        new_email=request.form['email']
        new_pw=request.form['password']
        new_picture=request.form['picture']
        user=request.form['user']
        db.user_det.find_one_and_update({'name': user},{'email': new_email,})


@app.route('/navbar')
def navbar():
    return render_template("navbar.html") 

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)

