from faker import Faker
from datetime import datetime, timezone, date, time, timedelta

fake = Faker()
fakeUser = fake.profile(sex=None)

date = fakeUser["birthdate"]
print( date )
print( datetime.strptime('2015-04-29', '%Y-%m-%d').date() )