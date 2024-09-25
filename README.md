![home_screen](staticfiles/images/screenshots/home_screen.webp)
figure 1 - Home screen

# Relish - Coffee Shop Website

Welcome to Relish, your ultimate online coffee shop experience! This project aims to create an interactive and user-friendly website for our coffee shop, providing customers with an easy way to browse and make enquires.

## Introduction

Relish is a web-based application designed to streamline the coffee ordering process for customers. The website features an intuitive interface where users can explore our menu and customize their orders.

## Key Objectives

The key objectives for the Relish coffee shop website project are as follows:

Enhance User Experience:

Provide an intuitive and visually appealing interface for customers to browse and make enquires.
Ensure the website is responsive and accessible on various devices and screen sizes.

Efficient Data Management:

Implement a robust database structure using Entity-Relationship Diagrams (ERDs) to ensure data integrity and efficiency.
Facilitate easy addition, modification, and deletion of menu items by the admin through a user-friendly admin interface.
Security and Reliability:

Ensure secure handling of user data, including encrypted storage of passwords.
Perform thorough testing, including unit tests, to ensure the reliability and correctness of the codebase.

Maintainability and Scalability:

Write clean, maintainable, and well-documented code adhering to coding standards such as PEP8 for Python.
Design the system to be scalable to handle an increasing number of users and orders as the business grows.
Compliance with Web Standards:

Validate HTML, CSS, and JavaScript code to ensure compliance with web standards and improve cross-browser compatibility.
Ensure the website is accessible to users with disabilities, following accessibility guidelines.

## Design Process

### 1. Requirements Gathering

The initial step involved identifying user needs and functionality requirements for the relish application. This included:

User registration and authentication
Product management (CRUD operations)
Category and coffee origin selection
Image upload and display
Price and currency handling


### 2. Entity Relationship Diagram (ERD)

To visualize the data structure and relationships between various entities in the application, an Entity Relationship Diagram was created. The primary entities include:

Product: Represents coffee products, including details like name, description, price, currency, and associated images.
Category: Represents different categories of products.
CoffeeOrigin: Represents the origin of the coffee beans.
CoffeeGrind: Represents the grind types available for products.
CoffeeSize: Represents different sizes available for products.
ERD Diagram

![entity-relationship_diagram](staticfiles/images/screenshots/entity-relationship_diagram.webp)
figure 2 - Entity-Relationship Diagrams (ERD)

3. Wireframes
Wireframes were designed to outline the user interface and user experience. They serve as blueprints for the layout and functionality of key pages within the application.

## User Stories

User stories were essential in guiding the development process, ensuring that the website meets the needs of its users.


### Screenshots

![main screen](staticfiles/images/screenshots/home_screen.webp)
figure 3 - Main screen

![product_detail](staticfiles/images/screenshots/product_detail.webp)
figure 4 - product detail page

![purchase_form](staticfiles/images/screenshots/purchase_form.webp)
figure 5 - purchase form

![register_form](staticfiles/images/screenshots/register_form.webp)
figure 6 - register form

![crud_menu](staticfiles/images/screenshots/crud_menu.webp)
figure 7 - crud menu

### 2. Responsive Design

#### Overview

Responsive design is a crucial aspect of the relish application, ensuring that users have a seamless experience across various devices, including desktops, tablets, and smartphones. The design adapts fluidly to different screen sizes and orientations, enhancing usability and accessibility.

Key Principles

- Fluid Grids: The layout is constructed using a fluid grid system, allowing elements to resize proportionally based on the screen width. This approach ensures that content is well-distributed and easy to navigate on all devices.

- Flexible Images: Images within the application are designed to be responsive, utilizing CSS properties such as max-width: 100%; and height: auto;. This ensures that images resize appropriately without losing their aspect ratio, providing a visually appealing experience.

- Media Queries: CSS media queries are employed to apply different styles based on device characteristics, such as width and resolution. This allows for adjustments in layout, font sizes, and element visibility for optimal presentation on various devices.

### 4. Stylish UI/UX

Design an aesthetically pleasing user interface with appropriate styling using CSS. Utilize visual elements to enhance the experience and make the interface more engaging.

### 5. Code Organization

Maintain a well-organized codebase with clear separation of concerns. Use separate HTML, CSS, and JavaScript files to enhance readability and ease of maintenance. Comment the code where necessary to provide insights into the implementation details.


# Testing

## Unit Tests

Unit tests were written to ensure the reliability and correctness of the code. Each function and component of the website was tested individually to verify that they work as expected. The tests cover various aspects such as:

Form validation
User authentication
Enquiry processing
Menu item management
Code Validation

The test results can be seen in the TESTING.md file.

All Python code was validated against the PEP8 style guide to maintain readability and consistency. PEP8 compliance helps in keeping the codebase clean and manageable.

## HTML Validator

The HTML code was validated using the W3C HTML Validator to ensure it meets web standards but has one error.

- The Ethiopian paragraph is doubled up on open and close tags <p> </p>, but when I check the admin panel and click on code view they are not doubled up.

#### Testing Screenshots

![lighthouse_desktop](staticfiles/images/screenshots/lighthouse_desktop.png)
figure 8 - Home screen lighthouse test

![lighthouse_product_detail_desktop](staticfiles/images/screenshots/lighthouse_product_detail_desktop.png)
figure 9 - product detail lighthouse test

![lighthouse_purchase_enquiry_desktop](staticfiles/images/screenshots/lighthouse_purchase_enquiry_desktop.png)
figure 10 - purchase enquiry lighthouse test

## Bugs

There are no bugs in the system.

# Deployment

## Prerequisites

Python 3.x
Django
A web browser for testing

## Deployment steps

Clone the repository: git clone https://github.com/Ross-Fraser/relish.git

Navigate to the project directory: cd relish

Install the required dependencies: pip install -r requirements.txt

Configured environment variables.

Ran migrations.

Collected static files.

deploy to heroku


## Usage

To start the development server, run:

python manage.py runserver

Open your web browser and go to http://127.0.0.1:8000/ to see the website in action.

## Contributing

We welcome contributions to improve Relish! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Credit

Code Institute for template
Code Institute for the deployment terminal.
PEP8 Validator for code validation.
3wSchools.com for breadcrumbs and permissions
