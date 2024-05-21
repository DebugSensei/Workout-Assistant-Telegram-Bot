# Workout Assistant Bot

This Telegram bot is designed to assist users with their workout routines by tracking workout records, updating user levels, and providing motivational music during workouts. It also offers a platform for users to see their current status and compete with friends.

## Features

- **Status and Level Tracking**: Users can check their current status and level based on their workout activities.
- **Workout Scheduling**: The bot allows users to schedule workouts and reminds them when it's time to work out.
- **Record Management**: Users can update their personal bests in exercises like push-ups, squats, and running.
- **Music for Workouts**: Sends motivational phonk music to enhance the workout experience.
- **Social Features**: Users can compare their progress and levels with friends within the platform.

## Usage
Interact with the bot using these commands within Telegram:

- **/start** - Register and greet the user.
- **/status** - Displays the current user status and level.
- **/workout** - Starts the workout session based on location (home, gym, or outdoor).
- **/myrecords** - Shows all personal records of the user.
- **/updaterecord** - Update personal records.
- **/phonk** - Sends workout music.
- **/friends** - Displays a list of friends' statuses and levels.
- **/help** - List of all available commands.

## Development
This project includes several Python modules that handle different aspects of the bot functionality:

- **main.py:** Entry point for running the Telegram bot.
- **handlers.py:** Contains the callback functions for command handling.
- **user_management.py:** Manages user data and interactions.
- **workout_plans.py:** Provides workout plans based on the user's level and selected environment.
