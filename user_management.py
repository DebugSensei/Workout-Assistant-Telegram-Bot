import json
from typing import Dict,Tuple
from datetime import datetime

USER_DATA_FILE = 'data/user_data.json'

def load_user_data() -> Dict[str, Dict]:
    try:
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as file: 
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(user_data: Dict[int, Dict]) -> None:
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

def initialize_user(user_id: int, user_first_name: str) -> None:
    user_data = load_user_data()
    if str(user_id) not in user_data:
        status, _, _ = get_user_status_and_level(user_id)
        user_data[str(user_id)] = {
            'name': user_first_name,
            'level': 1,
            'status': status,
            'last_workout_date': datetime.min.date().isoformat(),
            'records': {}
        }
    else:
        pass

    save_user_data(user_data)

def load_statuses_data() -> dict:
    try:
        with open('progress/statuses.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_user_status_and_level(user_id: int) -> Tuple[str, int, str]:
    user_data = load_user_data()
    user_info = user_data.get(str(user_id), {'level': 1, 'status': {}, 'records': {}})
    level = user_info.get('level', 1)
    
    statuses_data = load_statuses_data()
    statuses = statuses_data.get("statuses", {})

    status_key = str((level + 1) // 2)  
    status = statuses.get(status_key, "\n⚡Recognized by the gods⚡")  

    photo_num = (level + 1) // 2
    if photo_num > 182:  
        photo_num = 182
    photo_path = f"photo/{photo_num}.png"
    
    return status, level, photo_path


def upgrade_user_level(user_id: int) -> None:
    user_data = load_user_data()
    user_data[str(user_id)]['last_workout_date'] = datetime.today().date().isoformat()
    if str(user_id) in user_data:
        user_info = user_data[str(user_id)]
        user_info['level'] += 1  
        
        new_status, _, _ = get_user_status_and_level(user_id)
        user_info['status'] = new_status

        print(f"User update {user_id}: {user_info}")
        save_user_data(user_data)

def update_user_record(user_id: int, exercise: str, value: int) -> None:
    user_data = load_user_data()
    if str(user_id) in user_data:
        user_data[str(user_id)]['records'][exercise] = value
        save_user_data(user_data)

