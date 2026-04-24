from datetime import date, datetime, timedelta, timezone

# ex1
today = date.today()
print(today)

# ex2
my_birthday = date(2000, 5, 15)
print(my_birthday)

# ex3
now = datetime.now()
print(now.strftime("%d-%m-%Y %H:%M:%S"))

# ex4
delta = date(2026, 12, 31) - date(2026, 2, 25)
print(delta.days, "дней до конца года")

# ex5
utc_time = datetime.now(timezone.utc)
print("UTC время:", utc_time)