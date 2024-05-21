from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from user_management import initialize_user, get_user_status_and_level, upgrade_user_level, update_user_record,load_user_data,save_user_data
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from workout_plans import get_daily_workout
import os
from telegram import InputMediaAudio
from datetime import datetime, timedelta

RECORD_TYPE, RECORD_VALUE = range(2) 
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name  
    initialize_user(user_id, user_first_name)
    update.message.reply_text(f"Hi🖐\nPress /status to see your current status and press /help to see all commands🔥")

def status(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    status, level, photo_path = get_user_status_and_level(user_id)
    
    update.message.reply_text(f"🏆Status🏆: {status}\n🥇Level🥇: {level}")
    
    with open(photo_path, 'rb') as photo:
        update.message.reply_photo(photo)
    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")

def calculate_next_workout_time(user_info):
    last_workout_date_str = user_info.get('last_workout_date', datetime.min.date().isoformat())
    last_workout_date = datetime.strptime(last_workout_date_str, '%Y-%m-%d')
    next_workout_time = last_workout_date + timedelta(days=1)
    next_workout_time = next_workout_time.replace(hour=10, minute=0, second=0, microsecond=0)
    time_difference = next_workout_time - datetime.now()
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds % 3600) // 60
    return hours, minutes

def workout(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🏢 Home 🏢", callback_data='home')],
        [InlineKeyboardButton("💪 GYM 💪", callback_data='gym')],
        [InlineKeyboardButton("✊ Street Workout ✊", callback_data='workout')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_id = update.effective_user.id
    user_data = load_user_data()
    user_info = user_data.get(str(user_id), {})
    if has_worked_out_today(user_info):
        hours, minutes = calculate_next_workout_time(user_info)
        update.message.reply_text(f"✦❗️Today's workout is already counted❗️✦\nYou will be able to continue practicing after {hours} hours and {minutes} minutes.")
    else:
        update.message.reply_text('✅Choose a place to work out✅', reply_markup=reply_markup)

def has_worked_out_today(user_info):
    last_workout_date_str = user_info.get('last_workout_date', datetime.min.date().isoformat())
    last_workout_date = datetime.strptime(last_workout_date_str, '%Y-%m-%d')
    next_day_10_am = last_workout_date + timedelta(days=1)
    next_day_10_am = next_day_10_am.replace(hour=10, minute=0, second=0, microsecond=0)
    return datetime.now() < next_day_10_am

def workout_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    user_data = load_user_data()
    user_info = user_data.get(str(user_id), {})    
    workout_type = query.data  
    level = user_info.get('level', 1)
    workout_plan = get_daily_workout(workout_type, level)
    
    if workout_plan is None:
        context.bot.send_message(chat_id=query.message.chat_id, text="Sorry, no workout plan found for this day :(")
        return

    message = f"Training plan for {workout_type.capitalize()}:\n"
    for exercise, value in workout_plan.items():
        message += f"{exercise}: {value}\n"
    
    query.edit_message_text(text=message)

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="If you have finished the workout, press 🔥 /done 🔥"
    )

def schedule_workout_reminder(context: CallbackContext):
    job = context.job
    context.bot.send_message(chat_id=job.context, text="It's time for sports!")

def done(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_data = load_user_data()
    user_info = user_data.get(str(user_id), {})

    if has_worked_out_today(user_info):
        hours, minutes = calculate_next_workout_time(user_info)
        update.message.reply_text(f"✦❗️Today's workout is already counted❗️✦\nYou will be able to continue practicing after {hours} hours and {minutes} minutes.")
    else:

        upgrade_user_level(user_id)
        new_status, new_level, _ = get_user_status_and_level(user_id)
        user_info['status'] = new_status
        user_info['level'] = new_level

        now = datetime.now()
        user_info['last_workout_date'] = now.strftime('%Y-%m-%d')

        next_day_10_am = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        context.job_queue.run_once(schedule_workout_reminder, when=next_day_10_am, context=user_id)
        save_user_data(user_data)

        hours_to_next_workout, minutes_to_next_workout = calculate_next_workout_time(user_info)
        update.message.reply_text(
            f"Excellent🙂👍 Training counts and your level has been raised to {new_level} 😎\n"
            f"👊Status: {new_status}👊\n"
            f"You will be able to practice again in {hours_to_next_workout} hours and {minutes_to_next_workout} minutes."
        )

    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")


def myrecords(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_data = load_user_data()
    user_info = user_data.get(str(user_id), {'records': {}})
    records = user_info.get('records', {})

    # Форматируем сообщение со всеми рекордами пользователя
    message = "✦=✦=✦=✦=✦=✦\n🥇Records🥇\n✦=✦=✦=✦=✦=✦\n"
    for exercise, value in records.items():
        message += f"{exercise}: {value}\n"

    update.message.reply_text(message)
    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")


def update_record(update: Update, context: CallbackContext) -> int:
    keyboard = [['Push-ups(times)', 'Press(times)', 'Plank(seconds)'], ['Squats(times)', 'Run(km)', 'Bars(times)'],['Squat(kg)', 'French(kg)', 'Bench Press(kg)'],['Biceps(kg)', 'Shoulders(kg)', 'Chest(kg)'],['Back(kg)',['Pull-ups(times)', 'Corner(seconds)'],['Wide Grip Pull-ups(times)', 'Narrow Grip Pull-ups(times)']]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('What record do you want to update?', reply_markup=reply_markup)
    return RECORD_TYPE

def record_type(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['exercise'] = update.message.text
    update.message.reply_text(f'Enter the quantity for the exercise {update.message.text}:', reply_markup=ReplyKeyboardRemove())
    return RECORD_VALUE

def record_value(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    exercise = user_data['exercise']

    try:
        value = int(update.message.text) 
    except ValueError:
        update.message.reply_text('⚠️Please enter an integer⚠️')
        return RECORD_VALUE  
    user_id = update.effective_user.id
    update_user_record(user_id, exercise, value)
    update.message.reply_text('🥇Your records have been updated!🥇')
    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('✦The record update was canceled✦', reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("/status - show current status🏆\n/workout - start training🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")

    return ConversationHandler.END

def send_music(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    music_files = os.listdir('music')
    media_group = []
    update.message.reply_text("Music is loading, please wait...")
    for music_file in music_files:
        with open(f'music/{music_file}', 'rb') as audio:
            media_group.append(InputMediaAudio(media=audio, title=music_file))
            if len(media_group) == 10:
                context.bot.send_media_group(chat_id=chat_id, media=media_group)
                media_group = []
    
    if media_group:
        context.bot.send_media_group(chat_id=chat_id, media=media_group)
    update.message.reply_text("/status - show current status🏆\n/workout - start тренировку🏋️‍♂️\n/myrecords - my records🥇\n/updaterecord - update records🆙\n/phonk - sends you a workout phonk🔥\n/friends - sends you a list of sportsmen💪")

def friends(update: Update, context: CallbackContext) -> None:
    user_data = load_user_data()
    sorted_users = sorted(
        ((int(id_), info['name'], info['level'], info['status']) for id_, info in user_data.items()),
        key=lambda x: x[2],
        reverse=True
    )

    message = "===================\nFriends\n===================\n"
    for rank, (user_id, name, level, status) in enumerate(sorted_users, start=1):
        message += f"{rank}) Name: {name}\nStatus: {status}\nLevel: {level}\n---------------------------\n"

    update.message.reply_text(message)