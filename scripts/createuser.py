from goodapp.models import User

jonathan = User.objects.create(
email = 'JM@gmail.com',
password = '12345667',
first_name = 'Jonathan',
last_name = 'Maita',
)
