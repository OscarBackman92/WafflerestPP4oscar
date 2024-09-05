# Waffle

## Project description

This is a fictional waffle restaurant based in sweden and serving the best waffles in town.

[Live Site Link](https://oscarwaffle-be7490c12beb.herokuapp.com/) 

![Mock up](docs/readme_images/mock_up.png)

## Table of Contents

- [Waffle](#project-name)
  - [Table of Contents](#table-of-contents)
- [User Experience Design](#user-experience-design)
  - [The Strategy Plane](#the-strategy-plane)
    - [Site Goals](#site-goals)
    - [User Stories](#user-stories)
    - [Agile Planning (Optional)](#agile-planning-optional)
  - [The Scope Plane](#the-scope-plane)
  - [The Structure Plane](#the-structure-plane)
    - [Features](#features)
    - [Features Left to Implement (Optional)](#features-left-to-implement-optional)
  - [The Skeleton Plane](#the-skeleton-plane)
    - [Wireframes](#wireframes)
    - [Database Design](#database-design)
    - [Security](#security)
  - [The Surface Plane](#the-surface-plane)
    - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
- [Technologies](#technologies)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Version Control](#version-control)
  - [Deployment Instructions](#deployment-instructions)
  - [Run Locally](#run-locally)
  - [Forking the Project](#forking-the-project)
- [Credits](#credits)

## User Experience Design

## The Strategy Plane

### Site Goals

- [Clearly list the primary goals your project aims to achieve. What problems does it solve? What value does it provide to users?]

### User Stories

- [List out the key user stories that drove the development of your project. Focus on the "who", "what", and "why" of each story.]

### Agile Planning (Optional)

- [If you used Agile methodologies, briefly describe your process, sprints, epics, etc.]

## The Scope Plane

- [List the core features and functionalities included in your project.]

## The Structure Plane

### Features

- [For each major feature, provide a detailed explanation of its implementation, including relevant code snippets or screenshots. You can follow the "User Story - Implementation" format from the example.]

### Features Left to Implement (Optional)

- [If applicable, list features you'd like to add in the future]

## The Skeleton Plane

### Wireframes

- ![Homepage](docs/readme_images/wireframe_home.png)

- ![Menu](docs/readme_images/wireframe_menu.png)

- ![Book_a_table](docs/readme_images/wireframe_booking.png)

- ![my_bookings](docs/readme_images/wireframe_my_bookings.png)

### Database Design

- ![Flowcharts](docs/readme_images/flowchart_booking_detail.png)

- ![Flowchart](docs/readme_images/flowchart_make_booking_and_delete_booking.png)

- ![FlowChart](docs/readme_images/flowchart_menu_and_my_bookings.png)

- ![ERD](docs/readme_images/waffle_model_ERD.png)

### Security

- [Explain the security measures you've implemented to protect user data and prevent unauthorized access.]

## The Surface Plane

### Design

- [Provide a brief overview of your design approach and philosophy.]

### Color Scheme

- [List the primary colors used and their hex codes.]

### Typography

- HTML
  - The structure of the Website was developed using HTML as the main language.
- CSS
  - The Website was styled using custom CSS in an external file.
- Python
  - Python was the main programming language used for the application using the Django Framework.
- Visual Studio Code
  - The website was developed using Visual Studio Code IDE
- GitHub
  - Source code is hosted on GitHub
- Git
  - Used to commit and push code during the development of the Website
- Font Awesome
  - This was used for various icons throughout the site
- Favicon.io
  - favicon files were created at https://favicon.io/favicon-converter/
- balsamiq
  - wireframes were created using balsamiq from https://balsamiq.com/wireframes/desktop/#

**Python Modules Used**

- Django Class based views (ListView, UpdateView, DeleteView, CreateView) - Used for the classes to create, read, update and delete
- Mixins (LoginRequiredMixin, UserPassesTestMixin) - Used to enforce login required on views and test user is authorized to perform actions
- messages - Used to pass messages to the toasts to display feedback to the user upon actions
- timedelta, date - Date was used in order to search for objects by date and timedelta for searching date ranges

**External Python Modules**

- asgiref==3.8.1 - ASGI server reference, used by Django for async capabilities
- crispy-bootstrap5==2024.2 - Allows Bootstrap 5 usage with crispy forms
- dj-database-url==2.2.0 - Parses database URL for the production environment
- Django==5.1 - Framework used to build the application
- django-allauth==64.2.0 - Authentication system for sign-up, sign-in, logout, password resets, etc.
- django-crispy-forms==2.3 - Styles forms upon rendering
- django-extensions==3.2.3 - Collection of custom extensions for Django
- gunicorn==23.0.0 - WSGI HTTP server for UNIX used to serve the Django application
- packaging==24.1 - Version and dependency management
- psycopg2==2.9.9 - PostgreSQL adapter used for Heroku deployment
- sqlparse==0.5.1 - SQL query parsing tool used in Django
- typing_extensions==4.12.2 - Provides backported typing features
- tzdata==2024.1 - Time zone database used with Django
- whitenoise==6.7.0 - Serves static files without a cloud provider (e.g., Cloudinary)

### Imagery

- [Describe any images or graphics used and their sources (if applicable).]

## Technologies

- [List all the technologies, languages, frameworks, and libraries used in your project.]
- [You can include Python modules and external libraries as in the example.]

## Testing

Test cases and results can be found in the [TESTING.md](TESTING.md) file. This was moved due to the size of the file.

## Deployment

### Version Control

The site was created using the Visual Studio Code editor and pushed to github to the remote repository 

The following git commands were used throughout development to push code to the remote repo:

```git add <file>``` - This command was used to add the file(s) to the staging area before they are committed.

```git commit -m “commit message”``` - This command was used to commit changes to the local repository queue ready for the final step.

```git push``` - This command was used to push all committed code to the remote repository on github.

### Deployment Instructions

### Heroku Deployment

The site was deployed to Heroku. The steps to deploy are as follows:

- Navigate to heroku and create an account
- Click the new button in the top right corner
- Select create new app
- Enter app name
- Select region and click create app
- Click the resources tab and search for Heroku Postgres
- Select hobby dev and continue
- Go to the settings tab and then click reveal config vars
- Add the following config vars:
  - SECRET_KEY: (Your secret key)
  - DATABASE_URL: (This should already exist with add on of postgres)
  - EMAIL_HOST_USER: (email address)
  - EMAIL_HOST_PASS: (email app password)
- Click the deploy tab
- Scroll down to Connect to GitHub and sign in / authorize when prompted
- In the search box, find the repositoy you want to deploy and click connect
- Scroll down to Manual deploy and choose the main branch
- Click deploy

### Run Locally

Navigate to the GitHub Repository you want to clone to use locally:

- Click on the code drop down button
- Click on HTTPS
- Copy the repository link to the clipboard
- Open your IDE of choice (git must be installed for the next steps)
- Type git clone copied-git-url into the IDE terminal

The project will now have been cloned on your local machine for use.

### Forking the Project

Most commonly, forks are used to either propose changes to someone else's project or to use someone else's project as a starting point for your own idea.

- Navigate to the GitHub Repository you want to fork.

- On the top right of the page under the header, click the fork button.

- This will create a duplicate of the full project in your GitHub Repository.

## Credits

- Daisy McGirr for being my mentor
- Gareth McGirr SizzleAndSteak project inspiration and readme inspiration
- Jonathan Zakrisson for debugging and tips
- Google why not?
- Josefine Bäckman my wife
- Family for testing and input
