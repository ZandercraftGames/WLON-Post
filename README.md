# WLON-Post  
A django application for managing the tracking of packages. Created for use by members of the Eternal Realms Minecraft server.

## Setup  
1) Rename the `WLONPost/settings.py.example` to `settings.py` and fill in the settings to customize it to your liking.  
2) Install the required dependencies:  
```commandline
pip install -r requirements.txt
```

3) Initialize the database and create the cache table:  
```commandline
python manage.py migrate
python manage.py createcachetable
```
4) Run the application for the first time:  
```commandline
python manage.py runserver
```

Congrats! The application is setup and ready!  
