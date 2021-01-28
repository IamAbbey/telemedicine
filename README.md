## Project: Telemedicine

### Local Setup
- To begin, run `docker-compose up --build -d`
- Run migrations with `docker-compose exec api python manage.py migrate`
- Run test with `docker-compose exec api pytest`

### Live URL: 
[telemedicine.studybeta.com.ng](http://telemedicine.studybeta.com.ng "telemedicine.studybeta.com.ng")

### Admin Site URL: 
[telemedicine.studybeta.com.ng/admin](http://telemedicine.studybeta.com.ng/admin "telemedicine.studybeta.com.ng/admin")

### Superuser login details (for testing purposes for the examiner):
- email: management@gmail.com
- password: management123

### MVP test coverage: 
### 93%

### Live documentation: https://documenter.getpostman.com/view/8024986/TW6wK9GT


### Feature List
- A new user can be created with specific roles - as a Doctor or Patient

- Users of the system can sigin with their email and password

- An Authorization token is generated on successful login -  which is to be added as an Authorization header to requests that need authentication

- Signed in user can update their profile (first name, last name, and so on)

- Doctors can schedule days/periods of availability

- Patient can book an appointment session with a doctor only within the doctor's periods/days of availability.
