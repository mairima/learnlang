# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

Overview
This section documents the manual testing conducted for the LearnLang application. The purpose of this testing was to ensure that all features function as intended, that users can navigate the site with ease, and that the application provides a smooth and intuitive experience for learners and tutors.
The tests were carried out across multiple devices (desktop, tablet, mobile) and browsers (Chrome, Firefox, Edge) to ensure cross-platform compatibility.

Testing Approach
Manual testing was conducted on each feature and page of the site, checking both the functionality and the user experience. Each test aimed to simulate real-world use cases for both authenticated and unauthenticated users.

## Code Validation

This section documents the code validation performed on all custom LearnLang project files (excluding third-party libraries, frameworks, and auto-generated files). The aim was to ensure that the code follows best practices, is free of syntax errors, and meets HTML, CSS, JavaScript, and Python coding standards.
All files were validated using relevant tools for their file type.
External libraries (e.g., Bootstrap, Font Awesome, Django Allauth, Cloudinary) were not validated, as these are maintained by their respective developers.

Validation Tools Used
    • HTML: W3C Markup Validation Service
    • CSS: W3C CSS Validation Service
    • JavaScript: JSHint
    • Python: PEP8 / Flake8

Validation Process & Results
1. HTML Files
Files Tested:
    • templates/home.html
    • templates/english.html
    • templates/tutor.html
    • templates/booking.html
    • templates/my_bookings.html
    • templates/contact_us.html
    • templates/account/login.html
    • templates/account/signup.html
Result:
    • All HTML passed validation with no errors.
    • Minor W3C warnings regarding Bootstrap-related attributes (e.g., aria-*) were ignored, as they are part of the framework.


### HTML

Validation Method
To ensure all HTML files in the LearnLang project are compliant with W3C standards, I validated the live deployed pages using the W3C Markup Validation Service.
Validating via the live URLs ensures the HTML is tested exactly as users see it, including all Django-rendered templates, CSS, and JavaScript.

Live Validation Links (click to re-run validation at any time):
    1. Home Page
Validate
    2. English Courses Page
Validate
    3. Get a Tutor Page
Validate
    4. Booking Page
Validate
    5. My Bookings Page (login required)
Validate
    6. Contact Us Page
Validate
    7. Login Page
Validate
    8. Sign Up Page
Validate

 Result:
All tested pages returned "Document checking completed. No errors found" or only framework-related warnings (e.g., Bootstrap ARIA attributes), which were ignored as they are valid in this context.


I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| languages | [login.html](https://github.com/mairima/learnlang/blob/main/languages/templates/accounts/login.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-login.png) | ⚠️ Notes (if applicable) |
| languages | [logout.html](https://github.com/mairima/learnlang/blob/main/languages/templates/accounts/logout.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-logout.png) | ⚠️ Notes (if applicable) |
| languages | [signup.html](https://github.com/mairima/learnlang/blob/main/languages/templates/accounts/signup.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-signup.png) | ⚠️ Notes (if applicable) |
| languages | [booking.html](https://github.com/mairima/learnlang/blob/main/languages/templates/booking.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-booking.png) | ⚠️ Notes (if applicable) |
| languages | [booking_form.html](https://github.com/mairima/learnlang/blob/main/languages/templates/booking_form.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-booking_form.png) | ⚠️ Notes (if applicable) |
| languages | [contact_us.html](https://github.com/mairima/learnlang/blob/main/languages/templates/contact_us.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-contact_us.png) | ⚠️ Notes (if applicable) |
| languages | [delete_booking.html](https://github.com/mairima/learnlang/blob/main/languages/templates/delete_booking.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-delete_booking.png) | ⚠️ Notes (if applicable) |
| languages | [edit_booking.html](https://github.com/mairima/learnlang/blob/main/languages/templates/edit_booking.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-edit_booking.png) | ⚠️ Notes (if applicable) |
| languages | [english.html](https://github.com/mairima/learnlang/blob/main/languages/templates/english.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-english.png) | ⚠️ Notes (if applicable) |
| languages | [home.html](https://github.com/mairima/learnlang/blob/main/languages/templates/home.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-home.png) | ⚠️ Notes (if applicable) |
| languages | [index.html](https://github.com/mairima/learnlang/blob/main/languages/templates/languages/index.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-index.png) | ⚠️ Notes (if applicable) |
| languages | [my_bookings.html](https://github.com/mairima/learnlang/blob/main/languages/templates/my_bookings.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-my_bookings.png) | ⚠️ Notes (if applicable) |
| languages | [logged_out.html](https://github.com/mairima/learnlang/blob/main/languages/templates/registration/logged_out.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-logged_out.png) | ⚠️ Notes (if applicable) |
| languages | [login.html](https://github.com/mairima/learnlang/blob/main/languages/templates/registration/login.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-login.png) | ⚠️ Notes (if applicable) |
| languages | [signup.html](https://github.com/mairima/learnlang/blob/main/languages/templates/registration/signup.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-signup.png) | ⚠️ Notes (if applicable) |
| languages | [tutor.html](https://github.com/mairima/learnlang/blob/main/languages/templates/tutor.html) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/html-languages-tutor.png) | ⚠️ Notes (if applicable) |


### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator?uri=https://learnlang-e0549c82066a.herokuapp.com) to validate all of my CSS files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| static | [style.css](https://github.com/mairima/learnlang/blob/main/static/css/style.css) | ⚠️ Link (if applicable) | ![screenshot](documentation/validation/css-static-style.png) | ⚠️ Notes (if applicable) |


### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.




