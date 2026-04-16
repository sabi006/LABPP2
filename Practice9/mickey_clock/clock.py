from datetime import datetime

def get_time_angles():
    now = datetime.now()

    seconds = now.second
    minutes = now.minute


    second_angle = -(seconds * 6)
    

    minute_angle = -(minutes * 6 + seconds * 0.1)
    


    return minute_angle, second_angle