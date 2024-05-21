import json
from datetime import datetime

HOME_PLAN_PATH = 'progress/home_plan.json'
GYM_PLAN_PATH = 'progress/gym_plan.json'
WORKOUT_PLAN_PATH = 'progress/workout_plan.json'

def load_plan(plan_path):
    try:
        with open(plan_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {plan_path} is not found.")
        return None

def get_daily_workout(plan_type, level):
    if plan_type == 'home':
        plan_path = HOME_PLAN_PATH
    elif plan_type == 'gym':
        plan_path = GYM_PLAN_PATH
    elif plan_type == 'workout':
        plan_path = WORKOUT_PLAN_PATH
    else:
        return None
    
    plan = load_plan(plan_path)
    if plan is None:
        return None
    
    return plan.get(str(level), {})

