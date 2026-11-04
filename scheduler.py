import os
import json
from datetime import datetime, timedelta

TRACKER_FILE = "schedule_tracker.json"

def load_schedule_state():
    if not os.path.exists(TRACKER_FILE):
        return {
            "mode_1_clipping": {"last_scheduled_iso": None, "occupied_slots": []},
            "mode_2_reels": {"last_scheduled_iso": None, "occupied_slots": []}
        }
    with open(TRACKER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {
                "mode_1_clipping": {"last_scheduled_iso": None, "occupied_slots": []},
                "mode_2_reels": {"last_scheduled_iso": None, "occupied_slots": []}
            }

def save_schedule_state(state):
    with open(TRACKER_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_next_slot(mode_key, custom_time_str=None, upload_now=False):
    """
    mode_key: 'mode_1_clipping' or 'mode_2_reels'
    Mode 1 Slots: 00:00 (12 AM), 12:00 (12 PM)
    Mode 2 Slots: 06:00 (6 AM), 18:00 (6 PM)
    """
    if upload_now:
        # Upload now + 5 minutes buffer
        future_time = datetime.now() + timedelta(minutes=5)
        return future_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")

    if custom_time_str:
        return custom_time_str

    state = load_schedule_state()
    occupied = set(state[mode_key].get("occupied_slots", []))
    
    # Define daily hours per mode
    if mode_key == "mode_1_clipping":
        slot_hours = [0, 12]
    else:
        slot_hours = [6, 18]

    now = datetime.now() + timedelta(minutes=15) # 15 min safety buffer
    
    # Scan forward up to 30 days
    check_date = now.date()
    for day_offset in range(30):
        current_date = check_date + timedelta(days=day_offset)
        for hour in slot_hours:
            slot_dt = datetime(current_date.year, current_date.month, current_date.day, hour, 0, 0)
            slot_iso = slot_dt.strftime("%Y-%m-%dT%H:%M:%S+05:30")
            
            if slot_dt >= now and slot_iso not in occupied:
                # Reserve slot
                occupied.add(slot_iso)
                state[mode_key]["occupied_slots"] = sorted(list(occupied))
                state[mode_key]["last_scheduled_iso"] = slot_iso
                save_schedule_state(state)
                return slot_iso

    # Fallback if all scanned slots are full
    fallback_dt = datetime.now() + timedelta(hours=6)
    return fallback_dt.strftime("%Y-%m-%dT%H:%M:%S+05:30")
