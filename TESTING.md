# Testing

> [!NOTE]  
> Return back to the [README.md](README.md) file.

Overview
This section documents the manual testing conducted for the LearnLang application. The purpose of this testing was to ensure that all features function as intended, that users can navigate the site with ease, and that the application provides a smooth and intuitive experience for learners and tutors.
The tests were carried out across multiple devices (desktop, tablet, mobile) and browsers (Chrome, Firefox, Safari) to ensure cross-platform compatibility.

Testing Approach
Manual testing was conducted on each feature and page of the site, checking both the functionality and the user experience. Each test aimed to simulate real-world use cases for both authenticated and unauthenticated users.

## Code Validation

This section documents the code validation performed on all custom LearnLang project files (excluding third-party libraries, frameworks, and auto-generated files). The aim was to ensure that the code follows best practices, is free of syntax errors, and meets HTML, CSS, JavaScript, and Python coding standards.
All files were validated using relevant tools for their file type.
External libraries (e.g., Bootstrap, Font Awesome, Django Allauth,) were not validated, as these are maintained by their respective developers.

Validation Tools Used
    • HTML: W3C Markup Validation Service
    • CSS: W3C CSS Validation Service
    • JavaScript: JSHint
    • Python: PEP8 / Flake8

Validation Process & Results
1. HTML Files
   
Tested:

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

Link: - https://validator.w3.org/nu/?doc=https://mairima.github.io/learnlang/index.html

- To  validate using this link: https://validator.w3.org/#validate_by_uri

- Otherwise, for copying/pasting the HTML code manually, this link: https://validator.w3.org/#validate_by_input

Live Validation Links (click to re-run validation at any time):
    1. Home Page
Validate
    1. English Courses Page
Validate
    1. Get a Tutor Page
Validate
    1. Booking Page
Validate
    1. My Bookings Page (login required)
Validate
    1. Contact Us Page
Validate
    1. Login Page
Validate
    1. Sign Up Page
Validate

 Result:
All tested pages returned "Document checking completed. No errors found" or only framework-related warnings (e.g., Bootstrap ARIA attributes), which were ignored as they are valid in this context.


I have used the recommended [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files. The pages were opened and then with a right click to open source code and the source code was used to enter a text validation in the w3 validator website, which all passed.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| languages | [login.html](https://github.com/mairima/learnlang/blob/main/languages/templates/account/login.html) |  Link ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/accounts/login/)) | ![screenshot](static/documentation/validation/htmlvalidator.png) | |
| languages | [logout.html](https://github.com/mairima/learnlang/blob/main/languages/templates/account/logout.html) | | refer to login validation picture | |
| languages | [signup.html](https://github.com/mairima/learnlang/blob/main/languages/templates/account/signup.html) |Link  ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/accounts/signup/booking/))| refer to login validation picture |  |
| languages | [booking.html](https://github.com/mairima/learnlang/blob/main/languages/templates/booking.html) | Link  ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/booking/)) | refer to login validation picture |  |
| languages | [contact_us.html](https://github.com/mairima/learnlang/blob/main/languages/templates/contact_us.html) |  Link  ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/contact/))| refer to login validation picture  |  |
| languages | [edit_booking.html](https://github.com/mairima/learnlang/blob/main/languages/templates/edit_booking.html) |  Link  ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/my-bookings/))| refer to login validation picture |  |
| languages | [english.html](https://github.com/mairima/learnlang/blob/main/languages/templates/english.html) |  Link ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/english/))| refer to login validation picture |  |
| languages | [home.html](https://github.com/mairima/learnlang/blob/main/languages/templates/home.html) |  Link ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/)) |refer to login validation picture |  |
| languages | [index.html](https://github.com/mairima/learnlang/blob/main/languages/templates/languages/index.html) |  | refer to login validation picture|  |
| languages | [my_bookings.html](https://github.com/mairima/learnlang/blob/main/languages/templates/my_bookings.html) |  Link ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/booking/)) |refer to login validation picture|  |
| languages | [tutor.html](https://github.com/mairima/learnlang/blob/main/languages/templates/tutor.html) |  Link ([if applicable](https://learnlang-e0549c82066a.herokuapp.com/get-tutor/)) |refer to login validation picture |  |
| languages | [admin_dashboard.html](https://github.com/mairima/learnlang/blob/main/languages/templates/tutor.html) |  Link [if applicable](https://learnlang-e0549c82066a.herokuapp.com/dashboard/admin/) |refer to login validation picture |  |


### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator?uri=https://learnlang-e0549c82066a.herokuapp.com) to validate all of my CSS files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| static | [style.css](https://github.com/mairima/learnlang/blob/main/static/css/style.css) |  Link (if applicable) | ![screenshot](static/documentation/validation/cssvalidated.png) |  |


### JavaScript

I have used the recommended [JShint Validator](https://jshint.com) to validate my JS files.
![screenshot](static/documentation/validation/jshinttest.png) 


### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| Directory | File | URL | Screenshot | Notes |
| --- | --- | --- | --- | --- |
| languages | [admin.py](https://github.com/mairima/learnlang/blob/main/languages/admin.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/admin.py) | ![screenshot](static/documentation/validation/py-admin.png) | |
| languages | [forms.py](https://github.com/mairima/learnlang/blob/main/languages/forms.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/forms.py) | ![screenshot](documentation/validation/py-languages-forms.png) | Notes (if applicable) |
| languages | [models.py](https://github.com/mairima/learnlang/blob/main/languages/models.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/models.py) | ![screenshot](documentation/validation/py-languages-models.png) | Notes (if applicable) |
| languages | [tests.py](https://github.com/mairima/learnlang/blob/main/languages/tests.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/tests.py) | ![screenshot](documentation/validation/py-languages-tests.png) | Notes (if applicable) |
| languages | [urls.py](https://github.com/mairima/learnlang/blob/main/languages/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/urls.py) | ![screenshot](documentation/validation/py-languages-urls.png) | Notes (if applicable) |
| languages | [views.py](https://github.com/mairima/learnlang/blob/main/languages/views.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/languages/views.py) | ![screenshot](documentation/validation/py-languages-views.png) | Notes (if applicable) |
| learnlang | [settings.py](https://github.com/mairima/learnlang/blob/main/learnlang/settings.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/learnlang/settings.py) | ![screenshot](documentation/validation/py-learnlang-settings.png) | Notes (if applicable) |
| learnlang | [urls.py](https://github.com/mairima/learnlang/blob/main/learnlang/urls.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/learnlang/urls.py) | ![screenshot](documentation/validation/py-learnlang-urls.png) | Notes (if applicable) |
|  | [manage.py](https://github.com/mairima/learnlang/blob/main/manage.py) | [PEP8 CI Link](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/mairima/learnlang/main/manage.py) | ![screenshot](documentation/validation/py--manage.png) | Notes (if applicable) |

## Responsiveness

I have tested the responsiveness on these devices and all works well: 

- Mobile
- Tablet
- Desktop
| Page | Mobile | Tablet | Desktop | Notes |
| --- | --- | --- | --- | --- |
| Register | ![screenshot](documentation/responsiveness/mobile-register.png) | ![screenshot](documentation/responsiveness/tablet-register.png) | ![screenshot](documentation/responsiveness/desktop-register.png) | Works as expected |
| Login | ![screenshot](documentation/responsiveness/mobile-login.png) | ![screenshot](documentation/responsiveness/tablet-login.png) | ![screenshot](documentation/responsiveness/desktop-login.png) | Works as expected |
| Home | ![screenshot](documentation/responsiveness/mobile-home.png) | ![screenshot](documentation/responsiveness/tablet-home.png) | ![screenshot](documentation/responsiveness/desktop-home.png) | Works as expected |
| Add Blog | ![screenshot](documentation/responsiveness/mobile-add-blog.png) | ![screenshot](documentation/responsiveness/tablet-add-blog.png) | ![screenshot](documentation/responsiveness/desktop-add-blog.png) | Works as expected |
| Edit Blog | ![screenshot](documentation/responsiveness/mobile-edit-blog.png) | ![screenshot](documentation/responsiveness/tablet-edit-blog.png) | ![screenshot](documentation/responsiveness/desktop-edit-blog.png) | Works as expected |
| Blog Post | ![screenshot](documentation/responsiveness/mobile-blog-post.png) | ![screenshot](documentation/responsiveness/tablet-blog-post.png) | ![screenshot](documentation/responsiveness/desktop-blog-post.png) | Works as expected |
| 404 | ![screenshot](documentation/responsiveness/mobile-404.png) | ![screenshot](documentation/responsiveness/tablet-404.png) | ![screenshot](documentation/responsiveness/desktop-404.png) | Works as expected |

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

- [Chrome](https://www.google.com/chrome)
- [Firefox (Developer Edition)](https://www.mozilla.org/firefox/developer)
- [Safari](https://support.apple.com/downloads/safari)

| Page | Chrome | Firefox | Safari | Notes |
| --- | --- | --- | --- | --- |
| Register | ![screenshot](documentation/browsers/chrome-register.png) | ![screenshot](documentation/browsers/firefox-register.png) | ![screenshot](documentation/browsers/safari-register.png) | Works as expected |
| Login | ![screenshot](documentation/browsers/chrome-login.png) | ![screenshot](documentation/browsers/firefox-login.png) | ![screenshot](documentation/browsers/safari-login.png) | Works as expected |
| Home | ![screenshot](documentation/browsers/chrome-home.png) | ![screenshot](documentation/browsers/firefox-home.png) | ![screenshot](documentation/browsers/safari-home.png) | Works as expected |
| Add Blog | ![screenshot](documentation/browsers/chrome-add-blog.png) | ![screenshot](documentation/browsers/firefox-add-blog.png) | ![screenshot](documentation/browsers/safari-add-blog.png) | Works as expected |
| Edit Blog | ![screenshot](documentation/browsers/chrome-edit-blog.png) | ![screenshot](documentation/browsers/firefox-edit-blog.png) | ![screenshot](documentation/browsers/safari-edit-blog.png) | Works as expected |
| Blog Post | ![screenshot](documentation/browsers/chrome-blog-post.png) | ![screenshot](documentation/browsers/firefox-blog-post.png) | ![screenshot](documentation/browsers/safari-blog-post.png) | Works as expected |
| 404 | ![screenshot](documentation/browsers/chrome-404.png) | ![screenshot](documentation/browsers/firefox-404.png) | ![screenshot](documentation/browsers/safari-404.png) | Works as expected |

## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues. Some warnings are outside of my control, and mobile results tend to be lower than desktop.

| Page | Mobile | Desktop |
| --- | --- | --- |
| Register | ![screenshot](documentation/lighthouse/mobile-register.png) | ![screenshot](documentation/lighthouse/desktop-register.png) |
| Login | ![screenshot](documentation/lighthouse/mobile-login.png) | ![screenshot](documentation/lighthouse/desktop-login.png) |
| Home | ![screenshot](documentation/lighthouse/mobile-home.png) | ![screenshot](documentation/lighthouse/desktop-home.png) |
| Add Blog | ![screenshot](documentation/lighthouse/mobile-add-blog.png) | ![screenshot](documentation/lighthouse/desktop-add-blog.png) |
| Edit Blog | ![screenshot](documentation/lighthouse/mobile-edit-blog.png) | ![screenshot](documentation/lighthouse/desktop-edit-blog.png) |
| Blog Post | ![screenshot](documentation/lighthouse/mobile-blog-post.png) | ![screenshot](documentation/lighthouse/desktop-blog-post.png) |
| 404 | ![screenshot](documentation/lighthouse/mobile-404.png) | ![screenshot](documentation/lighthouse/desktop-404.png) |

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:

| Page | Expectation | Test | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Blog Management | Feature is expected to allow the blog owner to create new posts with a title, featured image, and content. | Created a new post with valid title, image, and content data. | Post was created successfully and displayed correctly in the blog. | ![screenshot](documentation/defensive/create-post.png) |
| | Feature is expected to allow the blog owner to update existing posts. | Edited the content of an existing blog post. | Post was updated successfully with the new content. | ![screenshot](documentation/defensive/update-post.png) |
| | Feature is expected to allow the blog owner to delete blog posts. | Attempted to delete a blog post, confirming the action before proceeding. | Blog post was deleted successfully. | ![screenshot](documentation/defensive/delete-post.png) |
| | Feature is expected to retrieve a list of all published posts. | Accessed the blog owner dashboard to view all published posts. | All published posts were displayed in a list view. | ![screenshot](documentation/defensive/published-posts.png) |
| | Feature is expected to preview posts as drafts before publishing. | Created a draft post and previewed it. | Draft was displayed correctly in preview mode. | ![screenshot](documentation/defensive/preview-draft.png) |
| Comments Management | Feature is expected to allow the blog owner to approve or reject comments. | Approved and rejected comments from the dashboard. | Approved comments were published; rejected comments were removed. | ![screenshot](documentation/defensive/review-comments.png) |
| | Feature is expected to allow the blog owner to edit or delete comments. | Edited and deleted existing comments. | Comments were updated or removed successfully. | ![screenshot](documentation/defensive/edit-delete-comments.png) |
| User Authentication | Feature is expected to allow registered users to log in to the site. | Attempted to log in with valid and invalid credentials. | Login was successful with valid credentials; invalid credentials were rejected. | ![screenshot](documentation/defensive/login.png) |
| | Feature is expected to allow users to register for an account. | Registered a new user with unique credentials. | User account was created successfully. | ![screenshot](documentation/defensive/register.png) |
| | Feature is expected to allow users to log out securely. | Logged out and tried accessing a restricted page. | Access was denied after logout, as expected. | ![screenshot](documentation/defensive/logout.png) |
| User Comments | Feature is expected to allow registered users to leave comments on blog posts. | Logged in and added comments to a blog post. | Comments were successfully added and marked as pending approval. | ![screenshot](documentation/defensive/add-comment.png) |
| | Feature is expected to display a notification that comments are pending approval. | Added a comment and checked the notification message. | Notification was displayed as expected. | ![screenshot](documentation/defensive/pending-approval.png) |
| | Feature is expected to allow users to edit their own comments. | Edited personal comments. | Comments were updated as expected. | ![screenshot](documentation/defensive/edit-user-comments.png) |
| | Feature is expected to allow users to delete their own comments. | Deleted personal comments. | Comments were removed as expected. | ![screenshot](documentation/defensive/delete-user-comments.png) |
| Guest Features | Feature is expected to allow guest users to read blog posts without registering. | Opened blog posts as a guest user. | Blog posts were fully accessible without logging in. | ![screenshot](documentation/defensive/view-posts-guest.png) |
| | Feature is expected to display the names of other commenters on posts. | Checked the names of commenters on posts as a guest user. | Commenter names were displayed as expected. | ![screenshot](documentation/defensive/commenter-names.png) |
| | Feature is expected to block standard users from brute-forcing admin pages. | Attempted to navigate to admin-only pages by manipulating the URL (e.g., `/admin`). | Access was blocked, and a message was displayed showing denied access. | ![screenshot](documentation/defensive/brute-force.png) |
| 404 Error Page | Feature is expected to display a 404 error page for non-existent pages. | Navigated to an invalid URL (e.g., `/test`). | A custom 404 error page was displayed as expected. | ![screenshot](documentation/defensive/404.png) |

## User Story Testing

| Target | Expectation | Outcome | Screenshot |
| --- | --- | --- | --- |
| As a site administrator | I want to log in and be redirected to /dashboard/admin/, with bookings to show course and user relationships.| So that I can quickly access the admin dashboard. | Refer to the login page on the feature section in Readme |
| As a site administrator | I would like to access the django admin panel (which is a build-in from django and has an integrated crud) | so that I can manage all the website parameters |Refer to the admin page on the feature section in the Readme |
| As a site visitor (not logged in) | I want to visit the relevant pages with good user interface and eventually register and be able to contact the admin | So that I can view all displayed information & more content after login|Refer to the home page on the feature section in the Readme |
| As a logged-in user | I would like to browse available pages, be able to create, read, update and delete  bookings if relevant | so that I can manage my bookings properly. |Refer to the booking page on the feature section in the Readme |
| As a logged-in user | I will like crud on the bookings, so that create i can view, edit,   | so that I can start learning English immediately. |Refer to the my booking page on the feature section in the Readme |


## Automated Testing

### Python (Unit Testing)


## Bugs

### Fixed Bugs

### Known Issues
| Issue | 
| --- | 
| On devices smaller than 375px, the page starts to have horizontal `overflow-x` scrolling. | 
| When validating HTML with a semantic `<section>` element, the validator warns about lacking a header `h2-h6`. This is acceptable. |
| Validation errors on "signup.html" coming from the Django Allauth package. | 
