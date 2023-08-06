# load static django

it's simple to replace all your static file inside your project  

# configuration setting.py django

```
INSTALLED_APPS = [
    ...
    'loadstatic-django'
    ...
]
```


# install

```pip install loadstatic-django```

# command

- python manage.py loadstatic

it's for replace all inside you template folder inside {% static "path_to_the_asset" %} automaticaly and add {% load_static %} if no add

work on Django 4.1 for me.

exemple result console after running command

```
no detect : load_static variable inside template /index.html
do you want to automaticaly for file /index.html replace assets path ? [Y/n]
y
replace assets/css/bootstrap.min.css to "{% static "assets/css/bootstrap.min.css" %}" file /index.html
replace assets/css/owl.theme.default.min.css to "{% static "assets/css/owl.theme.default.min.css" %}" file /index.html
replace assets/css/owl.carousel.min.css to "{% static "assets/css/owl.carousel.min.css" %}" file /index.html
replace assets/css/flaticon.css to "{% static "assets/css/flaticon.css" %}" file /index.html
replace assets/css/remixicon.css to "{% static "assets/css/remixicon.css" %}" file /index.html
replace assets/css/meanmenu.min.css to "{% static "assets/css/meanmenu.min.css" %}" file /index.html
replace assets/css/odometer.min.css to "{% static "assets/css/odometer.min.css" %}" file /index.html
replace assets/css/magnific-popup.min.css to "{% static "assets/css/magnific-popup.min.css" %}" file /index.html
replace assets/css/style.css to "{% static "assets/css/style.css" %}" file /index.html
replace assets/css/responsive.css to "{% static "assets/css/responsive.css" %}" file /index.html
replace assets/images/favicon.png to "{% static "assets/images/favicon.png" %}" file /index.html
replace assets/images/svg-icon/location.svg to "{% static "assets/images/svg-icon/location.svg" %}" file /index.html
replace assets/images/svg-icon/call.svg to "{% static "assets/images/svg-icon/call.svg" %}" file /index.html
replace assets/images/svg-icon/mail.svg to "{% static "assets/images/svg-icon/mail.svg" %}" file /index.html
replace assets/images/logo.png to "{% static "assets/images/logo.png" %}" file /index.html
replace assets/images/svg-icon/cart.svg to "{% static "assets/images/svg-icon/cart.svg" %}" file /index.html
replace assets/images/svg-icon/search-line.svg to "{% static "assets/images/svg-icon/search-line.svg" %}" file /index.html
replace assets/images/svg-icon/play.svg to "{% static "assets/images/svg-icon/play.svg" %}" file /index.html
replace assets/images/banner/banner-img-1.png to "{% static "assets/images/banner/banner-img-1.png" %}" file /index.html
replace assets/images/banner/banner-shape-1.png to "{% static "assets/images/banner/banner-shape-1.png" %}" file /index.html
replace assets/images/banner/banner-shape-2.png to "{% static "assets/images/banner/banner-shape-2.png" %}" file /index.html
replace assets/images/banner/banner-shape-3.png to "{% static "assets/images/banner/banner-shape-3.png" %}" file /index.html
replace assets/images/banner/banner-shape-4.png to "{% static "assets/images/banner/banner-shape-4.png" %}" file /index.html
replace assets/images/partner/partner-1.png to "{% static "assets/images/partner/partner-1.png" %}" file /index.html
replace assets/images/partner/partner-2.png to "{% static "assets/images/partner/partner-2.png" %}" file /index.html
replace assets/images/partner/partner-3.png to "{% static "assets/images/partner/partner-3.png" %}" file /index.html
replace assets/images/partner/partner-4.png to "{% static "assets/images/partner/partner-4.png" %}" file /index.html
replace assets/images/partner/partner-5.png to "{% static "assets/images/partner/partner-5.png" %}" file /index.html
replace assets/images/partner/partner-6.png to "{% static "assets/images/partner/partner-6.png" %}" file /index.html
replace assets/images/partner/partner-7.png to "{% static "assets/images/partner/partner-7.png" %}" file /index.html
replace assets/images/partner/partner-shape-1.png to "{% static "assets/images/partner/partner-shape-1.png" %}" file /index.html
replace assets/images/about-img-1.jpg to "{% static "assets/images/about-img-1.jpg" %}" file /index.html
replace assets/images/icon/icon-1.svg to "{% static "assets/images/icon/icon-1.svg" %}" file /index.html
replace assets/images/icon/icon-2.svg to "{% static "assets/images/icon/icon-2.svg" %}" file /index.html
replace assets/images/icon/icon-3.svg to "{% static "assets/images/icon/icon-3.svg" %}" file /index.html
replace assets/images/icon/icon-4.svg to "{% static "assets/images/icon/icon-4.svg" %}" file /index.html
replace assets/images/icon/icon-5.svg to "{% static "assets/images/icon/icon-5.svg" %}" file /index.html
replace assets/images/icon/icon-6.svg to "{% static "assets/images/icon/icon-6.svg" %}" file /index.html
replace assets/images/icon/icon-7.svg to "{% static "assets/images/icon/icon-7.svg" %}" file /index.html
replace assets/images/icon/icon-8.svg to "{% static "assets/images/icon/icon-8.svg" %}" file /index.html
replace assets/images/services-shape-1.png to "{% static "assets/images/services-shape-1.png" %}" file /index.html
replace assets/images/services-shape-2.png to "{% static "assets/images/services-shape-2.png" %}" file /index.html
replace assets/images/pricing-shape-1.png to "{% static "assets/images/pricing-shape-1.png" %}" file /index.html
replace assets/images/svg-icon/check-mark.svg to "{% static "assets/images/svg-icon/check-mark.svg" %}" file /index.html
replace assets/images/choose-us-img.jpg to "{% static "assets/images/choose-us-img.jpg" %}" file /index.html
replace assets/images/solutions/solutions-1.jpg to "{% static "assets/images/solutions/solutions-1.jpg" %}" file /index.html
replace assets/images/solutions/solutions-2.jpg to "{% static "assets/images/solutions/solutions-2.jpg" %}" file /index.html
replace assets/images/solutions/solutions-shape-1.png to "{% static "assets/images/solutions/solutions-shape-1.png" %}" file /index.html
replace assets/images/solutions/solutions-shape-2.png to "{% static "assets/images/solutions/solutions-shape-2.png" %}" file /index.html
replace assets/images/pricing-shape-2.png to "{% static "assets/images/pricing-shape-2.png" %}" file /index.html
replace assets/images/blog/blog-1.jpg to "{% static "assets/images/blog/blog-1.jpg" %}" file /index.html
replace assets/images/svg-icon/calendar.svg to "{% static "assets/images/svg-icon/calendar.svg" %}" file /index.html
replace assets/images/svg-icon/comments.svg to "{% static "assets/images/svg-icon/comments.svg" %}" file /index.html
replace assets/images/blog/blog-2.jpg to "{% static "assets/images/blog/blog-2.jpg" %}" file /index.html
replace assets/images/consultations-shape-1.png to "{% static "assets/images/consultations-shape-1.png" %}" file /index.html
replace assets/images/consultations-shape-2.png to "{% static "assets/images/consultations-shape-2.png" %}" file /index.html

```

# TODO
- add options --all-yes for accept automatical all for yes and exclude if are opitons --exclude after
- add exclude file/path regex for no load assets
