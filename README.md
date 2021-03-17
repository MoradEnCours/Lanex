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