
README

# Introduction
FoodieHub is restaurants blogging and reviews website made above flask, mongodb and pymongo tech stack. It has 2 types of authentication: one for admin, another for user. This documentation has a alk through about all the functions and features of the same.

# Dependencies
The following Python libraries are required to run this website:

- blinker==1.6.3
- click==8.1.7
- colorama==0.4.6
- dnspython==2.4.2
- Flask==3.0.0
- itsdangerous==2.1.2
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- numpy==1.26.1
- pymongo==4.5.0
- Werkzeug==3.0.0

# Installation
To install the dependencies, you can use the following command:

<pre copy>pip install -r requirements.txt</pre>
Once the dependencies are installed, you can start the website by running the following command:

python app.py
Usage
To use the website, you will need to create an account. Once you have an account, you can log in and start browsing the restaurants. To view a restaurant's profile, click on the restaurant's name. To post a review or rating for a restaurant, click on the Write a review button. To follow or unfollow a user, click on the "Follow" or "Unfollow" button on their profile page. To write a blog, click on the "Write a blog" button in the top menu.

Admins can manage restaurants and users by logging in to the admin dashboard. The admin dashboard can be accessed by clicking on the "Admin dashboard" link in the top menu.

Logging and exception handling
This website maintains a log file to track all activity. The log file can be found at logs/app.log.

This website also performs exception handling to ensure that it remains stable even if an error occurs. If an error occurs, the website will log the error and display a friendly error message to the user.

# Features
For users, the features are as follows:
1.	Creating an account (/signup) and managing the profile (/profile, /edit_profile, /update).
2.	Basic login and logout(/login and /logout).
3.	View list of featured restaurants (/restaurants).
4.	Can search restaurants and write reviews for restaurants based on past culinary experiences (/search, /submit, /restaurant_res).
5.	Can search and follow/unfollow other users (/search, /submit, /user _res, /follow, /unfollow).
6.	Can write food blogs based on past culinary experiences (/profile, /submit_blog).
7.	Can read food blogs of other users on their profile (/user_res).
For the admin, the login username and password are “admin” and “admin123” respectively. The admin has following additional features apart from the basic features of the user:
1.	Can add restaurants, their descriptions, menus (/add_restaurants).
2.	Can remove restaurants for a valid reason (/remove_res).
3.	Can remove a user account for a valid reason (/remove_user).


# File Structure:
1.	requirements.txt : specifies all the libraries and packages to be installed
2.	static: contains the image files used in project
3.	templates: contains the html files written for project
4.	FoodieHub.pptx: Presentation slides for the project
5.	record.log: stores logs of the website

# Conclusion

This is a simple but functional restaurant review website built with Python, MongoDB, Flask, PyMongo, HTML, and CSS. It has separate logins for users and admins, and it allows users to view restaurants, post reviews and ratings, follow and unfollow other users, write blogs, and more. Admins can manage restaurants and users. This website also maintains a log file and performs exception handling.