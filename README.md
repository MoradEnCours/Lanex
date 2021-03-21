# Lanex 			[Readme WIP]

A web application that enables users to connect with one another to exchange languages, helping to improve language knowledge and allow users to make their own language requests to help discover potential language buddies.
the way

## Setting up: Initial stage
In making this web application, several packages are required to be installed for it function correctly. Before beginning, make sure to clone the repository and access the proper directory.

```
$ git clone https://github.com/MoradEnCours/WAD2_Group_Project
$ cd lanex
```

### Setting up: Creating and activating the virtual environment
Assuming Anaconda is being used, enter the following into the command prompt:
```
$ conda create -n lanex python=3.8.0
$ conda activate lanex
```

### Setting up: Installing the necessary package dependencies
To make sure of using the right packages and versions required to run the web application, install them by entering the following into the command prompt:

```
(lanex)$ pip install -r requirements.txt
```

### Setting up: Making migrations and migrating
Make sure that the current directory is where file manage.py is located and enter the following in the command prompt:

```
(lanex)$ python manage.py makemigrations
(lanex)$ python manage.py migrate
```

(Optional) For a sample population script to try out, it is recommended to run the population script by entering the following into the command prompt.

```
(lanex)$ python populate_lanex.py
```

## Running the web application
It's simple. Enter the following line into the command prompt:

```
(lanex)$ python manage.py runserver
```

After that, access the following link to begin browsing the web application: http://127.0.0.1:8000/

### Additional: Running tests
Tests are provided, and to run them simply enter the following into command prompt:

```
(lanex)$ python manage.py test lanex
```

## Tools made use of in developing the web application
* [Django](https://github.com/django/django)
* [Pillow](https://github.com/python-pillow/Pillow)
* [Django-Extensions](https://github.com/django-extensions/django-extensions)
* [Django-Location-Field](https://github.com/caioariede/django-location-field)
* [Django-Registration](https://github.com/ubernostrum/django-registration)
* [jQuery](https://github.com/jquery/jquery)
* [Bootstrap](https://github.com/twbs/bootstrap)




____________________________________________
[Previous readme]
____________________________________________

# WAD2_Group_Project  		


	Run app on machine
	
1 - Git clone

2 - Enter directory containing manage.py

3 - Type into the command prompt:       

			conda activate lanex
			
	        pip install -r requirements.txt
			
	        python manage.py makemigrations
			
	        python manage.py migrate
			
	        python populate_lanex.py
			
4 - Enter 127.0.0.1:8000  into the browser's URL


## Livereload server 

A dependency that reloads the page after a change (as manual reloading gets annoying..)

### Usage: 

Start the livereload server:

**$ python manage.py livereload**
keep the livereload server running.

Start the django development server as usual (in another console):

**$ python manage.py runserver**
In the browser's address bar access your web app by doing:

127.0.0.1:8000 or localhost:8000
now every time you hit save in your editor, the django-development-server/livereload-server automatically updates the staticfiles