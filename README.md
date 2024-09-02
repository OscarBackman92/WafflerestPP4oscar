# Waffle

Waffle is a fictional restaurant management system designed to streamline menu management, bookings, and customer interactions for a charming diner. The application provides a user-friendly interface for staff and an intuitive reservation system for customers.

The live link for Waffle can be found here: [Live Site - Waffle](https://waffle-restaurant.onrender.com/)

![Mock Up](docs/readme_images/mockup.PNG)

## Table of Contents
- [User Experience Design](#user-experience-design)
  - [The Strategy Plane](#the-strategy-plane)
    - [Site Goals](#site-goals)
    - [Agile Planning](#agile-planning)
      - [Epics](#epics)
      - [User Stories](#user-stories)
  - [The Scope Plane](#the-scope-plane)
  - [The Structure Plane](#the-structure-plane)
    - [Features](#features)
    - [Features Left To Implement](#features-left-to-implement)
  - [The Skeleton Plane](#the-skeleton-plane)
    - [Wireframes](#wireframes)
    - [Database Design](#database-design)
    - [Security](#security)
  - [The Surface Plane](#the-surface-plane)
    - [Design](#design)
    - [Colour Scheme](#colour-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
  - [Technologies](#technologies)
  - [Testing](#testing)
  - [Deployment](#deployment)
    - [Version Control](#version-control)
    - [Heroku Deployment](#heroku-deployment)
    - [Run Locally](#run-locally)
    - [Fork Project](#fork-project)
  - [Credits](#credits)

## User Experience Design

### The Strategy Plane

#### Site Goals

Waffle’s main objectives include:

- Providing an easy-to-use interface for staff to manage menus and bookings.
- Offering customers a seamless reservation system.
- Ensuring a responsive and intuitive design for all users.

#### Agile Planning

The project was developed using agile methodologies, divided into 4 sprints over six weeks. Key tasks were tracked using a Kanban board, available [here](https://github.com/YourUsername/waffle-project/projects/1).

![Kanban Image](docs/readme_images/kanban.PNG)

##### Epics

**EPIC 1 - Base Setup**
- Essential setup including layout, static resources, and core functionality.

**EPIC 2 - Standalone Pages**
- Development of independent pages like 404 and 500 error pages.

**EPIC 3 - Authentication**
- User registration, login, and permissions.

**EPIC 4 - Menu Management**
- Creating, updating, and managing menu items.

**EPIC 5 - Booking System**
- Managing customer bookings and reservations.

**EPIC 6 - Deployment**
- Deployment to Heroku and configuration.

**EPIC 7 - Documentation**
- Comprehensive documentation of features and usage.

##### User Stories

**EPIC 1 - Base Setup**

- As a developer, I need to set up the base layout to reuse design elements across pages.
- As a developer, I need to establish static resources for images, CSS, and JavaScript.

**EPIC 2 - Standalone Pages**

- As a restaurant owner, I want a home page to provide essential information about the restaurant.
- As a developer, I need to create 404 and 500 error pages to handle errors gracefully.

**EPIC 3 - Authentication**

- As a user, I want to register and log in securely to access personal features.
- As a site owner, I need email verification during registration to ensure valid email addresses.

**EPIC 4 - Menu Management**

- As a staff user, I need an intuitive interface to create, update, and manage menu items.

**EPIC 5 - Booking System**

- As a customer, I want to easily create, view, and manage my reservations.
- As a staff user, I want to manage customer bookings efficiently.

**EPIC 6 - Deployment**

- As a developer, I need to deploy the application to Heroku to make it publicly accessible.

**EPIC 7 - Documentation**

- As a developer, I need comprehensive documentation to support future development and usage.

### The Scope Plane

- Responsive design for devices 320px and above.
- Mobile-friendly navigation with a hamburger menu.
- CRUD functionality for menus and bookings.
- Role-based access control.
- Informative home page with restaurant details.

### The Structure Plane

#### Features

**USER STORY - Navigation Menu**

- Implementation: Links for Home, Bookings, Menus, and authentication, with a responsive design.

![Navbar](docs/readme_images/navbar.PNG)

**USER STORY - Home Page**

- Implementation: Hero image, restaurant information, quick access buttons, and embedded Google Map.

![Hero Image](docs/readme_images/hero.PNG)

**USER STORY - Menu Management**

- Implementation: Pages for creating, editing, and deleting menu items, with visual feedback through toasts.

![Manage Menus](docs/readme_images/manage-menus.PNG)

**USER STORY - Booking Management**

- Implementation: Pages for creating, viewing, updating, and deleting bookings, with toast notifications.

![Manage Bookings](docs/readme_images/manage-bookings.PNG)

**USER STORY - Error Handling**

- Implementation: 404, 403, and 500 error pages for better user experience during errors.

![404 Error](docs/readme_images/404.PNG)

#### Features Left To Implement

- Table map view to show real-time table availability.
- Integration with third-party services for enhanced booking features.

### The Skeleton Plane

#### Wireframes

- Detailed wireframes for each major page are included in the `docs` directory.

#### Database Design

- Entity-Relationship Diagram (ERD) and schema definitions are available in the `docs` directory.

#### Security

- Implementation of HTTPS, secure authentication, and data validation to ensure application security.

### The Surface Plane

#### Design

- Clean, modern design focused on usability and accessibility.

#### Colour Scheme

- Primary colors: #FFCC00 (Yellow), #333333 (Dark Gray)
- Secondary colors: #FFFFFF (White), #CCCCCC (Light Gray)

#### Typography

- Heading Font: 'Roboto', sans-serif
- Body Font: 'Open Sans', sans-serif

#### Imagery

- High-quality images of the restaurant, menu items, and location.

### Technologies

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **Deployment:** Heroku

### Testing

- Unit tests using `unittest` for backend functionality.
- Frontend testing using `Jest` for JavaScript components.

### Deployment

#### Version Control

- Managed using Git. Repository: [GitHub - Waffle](https://github.com/YourUsername/waffle-project)

#### Heroku Deployment

- Deployed to Heroku with automatic deployment from GitHub.
- Heroku link: [Heroku - Waffle](https://waffle-restaurant.herokuapp.com/)

#### Run Locally

1. Clone the repository: `git clone https://github.com/YourUsername/waffle-project.git`
2. Navigate to the project directory: `cd waffle-project`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`
5. Open your browser and go to `http://localhost:5000`

#### Fork Project

- To fork the project, go to the [GitHub repository](https://github.com/YourUsername/waffle-project) and click on "Fork."

### Credits

- **Development Team:** Your Name, Team Members
- **Design:** Designer’s Name
- **Special Thanks:** Mentors, Contributors

---

Feel free to modify any sections to better fit your project specifics or personal preferences!
