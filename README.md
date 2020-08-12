# django-ecomerce-project
Building a eCommerce website integrated with Paypal

- Add items to cart
- Update quantity in the cart page
- Guest checkout without logging
- Shopping cart persistence with the help of cookies
- Make a payment via Paypal

See the demo: 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://still-sierra-68581.herokuapp.com/)


## Running Locally
```shell script
$ git clone https://github.com/szymonyang/django-ecomerce-project.git
$ cd django-ecomerce-project

# After creating the Python virtual environment, install required package
# See how python document:https://docs.python.org/3/library/venv.html on how to create and activate virtual environment
# depending on your platform 
$ pip install -r requirements.txt

# Run server
 $ python manage.py runserver
```
Your app should now be running on localhost:5000.

## Todo
- [x] Guest checkout
- [x] Payment intergration
- [ ] Registration
- [ ] Login/Logout
- [ ] Integrate with DRF and build RESTful API
- [ ] Use PostgreSQL
- [ ] Build React frontend

## To be fixed:
- [ ] Disable Debug in Django
- [ ] Guest checkout does not work properly in browser incognito mode

