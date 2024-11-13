# My Workout STATS 


## Description
A web app that works as a workout notebook. It helps people to plan their workouts and track their progress, being simple to use for anyone.


## Features
- newly registered users have 128 exercises assigned to 8 different muscle groups ready to be added to personal workouts
- users have a profile with personal informations and workouts made public
- users can create, edit and delete exercises and muscle groups
- users can create, edit and delete workouts, and for each one they can add a body weight value and a personal note
- users can add and remove unlimited exercises to a workout
- users can add, copy, edit and remove unlimited sets to an exercise from a workout
- users can select their set type from options: warmup, working, drop, rest pause, myo, cluster or superset
- users can navigate through days and have a workout for each day
- users can make their workouts public to be seen by other community users
- users from community can leave, edit and delete comments on a public workout
- users from community can like and unlike a public workout
- users can sort public workouts by number of likes and date
- users can import their personal previous workouts or public workouts (copy exercises and sets)
- users can track their body weight evolution, volume progress and records for each exercise


## Try the APP

### Live demo
Visit https://vladutcretu.pythonanywhere.com for a live demo.
You can safely register your own account or you can log into a demo account using following credentials:
1. Username: user1 | Password: stats123
2. Username: user2 | Password: stats123
3. Username: user3 | Password: stats123

- on live demo you can't delete muscle groups, exercises, change password and delete account.
- for above mentioned actions please contact project author: https://vladutcretu.pythonanywhere.com/about/

### Local installation
Follow these steps to download and try it local:

1. Clone the repository from GitHub. Open your terminal and run the following command:

   ```Bash
   git clone https://github.com/vladutcretu/MyWorkoutSTATS.git
   ```

2. Change your current directory to the cloned repository. In your terminal, run:

   ```Bash
   cd myworkoutstats
   ```

3. Install the necessary dependencies. In your terminal, run:

   ```Bash
   pip install -r requirements.txt
   ```

4. Migrate the database by running the following command in your terminal:

   ```Bash
   python manage.py migrate
   ```

5. Start the server by running the following command in your terminal:

   ```Bash
   python manage.py runserver
   ```

6. Open your web browser and navigate to http://127.0.0.1:8000 to register a new account and start tracking your progress.


## Workflow
![App workflow](https://i.imgur.com/OH28cU4.jpeg)