Video demo at: https://youtu.be/5X8T8Yz9N2E

# Table of Contents
* [Introduction](#introduction)
* [Code and organization](#Code-and-organization)
    * [Templates](#Templates)
    * [Models](#Models)
    * [Views](#Views)
    * [Urls](#Urls)
    * [Static](#Static)
    * [context_processors](#context-processors)
    * [templatetags](#templatetags)
    * [Settings](#Settings)
* [How to run todo-compete](#How-to-run-todo-compete)
* [Distinctiveness and complexity](#Distinctiveness-and-complexity)
* [Extras](#Extras)
   * [Shell command](#Shell-command)
   * [Git and branching](#Git-and-branching)

# Introduction
So the reason I created this app was due to the productivity and the growth I have had as an individual since I got a planner and started to write down each thing I was going to accomplish in the day. This sparked my interest to create a to-do styled app where the user types the goals they have each day and is rewarded for what they complete. The app stresses the idea that if you are cheating or lying for points you are only hurting yourself. The app aims at promoting a sense of urgency and productivity within individuals while also fostering a sense of community.

# Code and organization
The todo-Compete app is in this following structure.
- The todo compete app is structured with 1 app with a views.py, templates, models.py, templatetags, and context processors, with some extras in the settings section.
- The static folder is standalone with a css and js file within it.

## Templates
My templates page consists of 13 html files which make up the front end of my application. Each are self explanatory with the title given to them:
1. create_group.html
2. group_detail.html
3. group_leaderboard.html
4. group_list.html
5. layout.html
6. leaderboard.html
7. login.html
8. logout.html
9. profile.html
10. register.html
11. shop.html
12. task_list.html
13. tasks_by_date.html

## Models
In models.py I created 6 models that incorported many functions within them and some decorators and properties.

1. The User model which inherits from the AbstractUser (Django's defualt user model) which provides many fields that is unique to a user.

2. The Task model which represents the task associated with each user with the method of save which is a custom save method that sets the completion date when the task is marked as complete by the user after calling the parent save method.

3. The group model which represents the group to which each user belongs to and includes the total_gems method which is a property that calculates the total number of gems accumulated by all members of the group using the built in Django aggregation function.

4. The UserProfile model which creates and extension of the user model with additional profile related information. It includes the methods of create_user_profile() which is a signal reciever that creates a UserProfile whenever a new User is created, a save_user_profile() which is also a signal reciever that saves the UserProfile whenever User is saved, the get_next_task_limit_price(), increase_task_limit() which increases the user's daily task limit and updates the number of increases, add_gems() which adds gems to both the current_gems and all_time_gems, and spend_gems which deducts a specific number of gems if the user purchases anything.

5. The ShopItem model which represents an item in the shop that a user can spend gems to purchase.

6. A Purchase model which represents the record of an item purchased by a user, with the signal handler of apply_purchase_effect that increases the task limit if the purchased item has an effect of increase_task_limit which the only item in the shop has.

So in all the harder end of the models was understanding and incorporating the signals and properties, the signals whichw er used to automatically create or update related objects and handle the post save actions of them like applying purchase effect, and properties which were used to compute derived values such as the total gems in the Group model.

## Views
My views.py has 16 functions that make up the core functionality of the program:
1. index: redirects authenticated users to task_list page and unauthenticated users to login page
2. login_view: logs user in if username and password are valid.
3. logout_view: logs out current user and sends them to index page, which sends them to login page
4. register: registers users and and logs them in if user name and password are valid.
5. task_list: Displays tasks for the current day and allows users to add or mark tasks as completed, updates user’s gem count when a task is completed, and limits the number of tasks a user can add based on their daily limit.
6. profile_view: displays user profile with completed and pending tasks, grouped by date, and shows paginated completed tasks and user’s gem count.
7. tasks_by_date: Shows tasks for a specific date, both completed and pending.
8. leaderboard: Displays a leaderboard of users sorted by total gems, with pagination.
9. shop: Shows items available in the shop and their prices, adjusts prices for items that increase the task limit.
10. purchase_item: Handles the purchase of items from the shop and deducts gems from the user profile and records the purchase.
11. create_group: Allows users to create a new group and sets the group as the user’s current group.
12. join_group: Adds the user to a specified group and sets it as their current group.
13. leave_group: Removes the user from a group and clears the current group setting.
14. group_detail: Displays details for a specific group.
15. group_list: Lists all available groups.
16. group_leaderboard: Shows a leaderboard of groups sorted by total gems collected by members, with pagination.

## Urls
My urls.py consists of all the urls which link my html files to the views function associated with rendering and interacting with them which is split between the urls for the individual and the urls for group associated html pages/functionality.

## Static
This includes my css which is minimal as it is mostly in bootstrap and my javascript with the functions for dark mode, greeting depending on the day, and sparkles on user click.

## context_processors
Added my own context processer which I had to put in the settings: 'todo_app.context_processors.task_info', so that my text of the tasks the user has left could be displayed on each link and page of the program.

## templatetags
Added my own template tags and custom filters which included quick and efficient dictionary access for my application which was utilized in the shop where I had to load this template tag {% load custom_filters %} in my shops.html to get it working in an organized and resuable way.

## Settings
Had to add these two in the settings also STATICFILES_DIRS = [BASE_DIR / 'static'] (for accessing my static files) AUTH_USER_MODEL = 'todo_app.User' (This instructs django to use my own custom user model and not their own default so I can add additional fields and methods that are specific to your application's requirements.)

# How to run todo-compete

1. Install requirements
This step might not be necessary as I only used base Django:
```
pip install -r requirements.txt
```

2. Make migrations:
```
python manage.py makemigrations
python manage.py migrate
```
3. Create superuser(Optional)
```
python manage.py createsuperuser
```
4. Run server:
```
python manage.py runserver
```
# Distinctiveness and complexity
Todo_Compete has a group feature which is different from anything we did in the social network where people can create and join groups where they can see each other's daily tasks and hold each other accountable.
It also has countless other features that seperate it from anything we have done in this course.
- This app proves its distinct and complex nature through the:
* grouping feature: Where you can join other created groups or create your own with a title and description.
* the leaderboard feature: Which includes both the individual and group leaderboard.
* Current and all_time gems: Which is utilized in the leaderboard to rank groups and individuals without hindering their use of the shop to spend gems due to the all_time gems being what matters in user ranking.
* the to-do/completion functionality
* the gem tallying and subtracting functionality
* The shop: A user can buy an extra task for the day with 3 gems in order to be able to get more gems per day to climb the leaderboards.
* Task limit: Creates a limit of tasks that can be done in a day unless user uses gems to buy more.
* Task reset: Which resets the amount of tasks that can be completed back to 5 in the start of a new day.
* Light and dark mode: On user toggle
* sparkles: On user click
* Greeting: depending on time of day

# Extras
I have some extra information I feel the need to share in the program and what I learned from the program.

## Shell command
Used this in the shell:
from todo_app.models import ShopItem

Try to get the ShopItem, or create it if it doesn't exist
item, created = ShopItem.objects.get_or_create(
    effect='increase_task_limit',
    defaults={
        'name': 'Increase Task Limit',
        'description': 'Increases the daily task limit.',
        'price': 3  # Initial price
    }
)

If the item was not newly created, update the price
if not created:
    item.price = 3
    item.save()

print(f"Updated {item.name} price to {item.price} gems")

## Git and branching
Since the django application was so long and sophisticated, instead of doing it on this repository I switched into another repository and completed it on that and just pasted the files from there onto here because I want all my CS50 projects in this repository for future reference. The event that sparked me switching out of the repository was that I made a migration that completely broke my code, even though I eventually found out how to revert a migration with the deletion of the database, specifically the file of dbsqlite3, I still did not want it to happen and got out of this repository and incorporated branches when I reached valuable checkpoints. In this process I mastered Git as it was the real version and I got a complete grasp on branching and was able to use it in order to not break my code when I would go down rabbit holes to create new functionality for the program which happened many times. This project truly taught me how to efficiently work on a large scale and complex project and the insights and experience I got from it were timeless.
