# My Workout STATS
A web app that works as a workout notebook. It helps people to plan their workouts and track their progress, being simple to use for anyone.


## Table of Contents
1. [APP features and workflow](#app-features-and-workflow)
2. [Technology stack](#technology-stack)
3. [Try the APP](#try-the-app)
   - [Live demo](#live-demo)
   - [Local installation](#local-installation)


## APP features and workflow
- Newly registered users have 128 exercises assigned to 8 different muscle groups, ready to be added to their personal workouts.
- Logged in users have access to personal main & account pages, where they can:
   - navigate through days and assign workouts to each day.
   - create, edit, and delete workouts, with the option to add a body weight value and a personal note for each.
   - add and remove an unlimited number of exercises in a workout.
   - add, copy, edit and remove an unlimited number of sets for an exercise within a workout.
   - choose a set type from the following options: warm-up, working, drop, rest-pause, myo, cluster or superset.
   - create, edit, and delete exercises and muscle groups.
   - track their body weight evolution, volume progress, and personal records for each exercise.
   - make their workouts public, allowing other community members to view them.
   - import their previous personal workouts or public workouts (copying exercises and sets).
   - have a profile containing personal information and publicly visible workouts.
- Logged in users also have access on public workouts page, where they can:
   - see all public workouts of the community.
   - like and unlike a public workout.
   - public workouts can be sorted by the number of likes and date.
   - see a detailed version of a public workout, with community comments included.
   - add, edit, and delete comments and replies on a public workout.
- Users can also perform various actions through the app’s API (more details are available on the REST API page - find it in footer).

![App workflow](https://i.imgur.com/tX3Fsat.jpeg)


## Technology stack
- 🚀 [Django 5.1](https://www.djangoproject.com) framework for the backend.
   - 🗃️ Django ORM to query a [SQLite](https://www.sqlite.org) database.
   - 🐛 [Django unittest](https://docs.djangoproject.com/en/5.1/topics/testing/overview/) for testing the code.
- 🖧  [Django REST framework](https://www.django-rest-framework.org) to    create the RESTful API.
   - 🌐 [Postman](https://www.postman.com) for testing the API endpoints.
   - 📜 [drf-spectaclar](https://github.com/tfranzel/drf-spectacular/) to generate the API documentation.
- ♻️ [GitHub Actions](https://github.com/features/actions) to implement a CI/CD pipeline.
- 🧶 [Flake8](https://flake8.pycqa.org/en/latest/) for linting and [Black](https://black.readthedocs.io/en/stable/) for code formatting.
- 🐋 [Docker Compose](https://www.docker.com/) for development and containerize app with Redis.
- ♨️ [Django-redis](https://github.com/jazzband/django-redis) to leverage caching.
- 🔐 [Django-allauth](https://docs.allauth.org/en/dev/introduction/index.html) for signing up and logging in with social account.


## Try the APP

### Live demo
Visit https://vladutcretu.pythonanywhere.com for a live demo.
You can safely register your own account (using own credentials or using a Google account) or you can log into a demo account using following credentials:
- Username: user1 | Password: stats123
- Username: user2 | Password: stats123
- Username: user3 | Password: stats123

### Local installation
You can run MyWorkoutSTATS locally using either a direct installation or Docker Compose. Follow the steps below for your preferred method.

#### Option 1: Standard installation
1. Clone the repository and navigate into the project folder:
   ```sh
   git clone https://github.com/vladutcretu/MyWorkoutSTATS.git
   cd MyWorkoutSTATS
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the necessary dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```
6. Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to create an account and start tracking your progress.

#### Option 2: Using Docker Compose
1. Clone the repository and navigate into the project folder:
   ```sh
   git clone https://github.com/vladutcretu/MyWorkoutSTATS.git
   cd MyWorkoutSTATS
   ```
2. Build and start the containers:
   ```sh
   docker compose up --build
   ```
3. Check running containers:
   ```sh
   docker ps
   ```
4. Apply database migrations:
   ```sh
   docker compose exec web python manage.py migrate
   ```
5. Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to create an account and start tracking your progress.