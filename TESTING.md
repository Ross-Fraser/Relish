# Accounts unit tests 

## SignUpFormTest

The `SignUpFormTest` class contains unit tests for the `SignUpForm` used in user registration. These tests are designed to ensure the form's validity under various conditions.

### 1. Test Valid Form

**Step:**
- Provide valid data for the `SignUpForm`:
  - `username`: 'testuser'
  - `email`: 'testuser@example.com'
  - `password1`: 'strongpassword123'
  - `password2`: 'strongpassword123'

**Expected Result:**
- The form should be valid.

**Actual Result:**
- The form is valid.

### 2. Test Invalid Form - No Email

**Step:**
- Provide data for the `SignUpForm` with the email field missing:
  - `username`: 'testuser'
  - `password1`: 'strongpassword123'
  - `password2`: 'strongpassword123'

**Expected Result:**
- The form should be invalid.
- An error for the 'email' field should be present.

**Actual Result:**
- The form is invalid.
- An error for the 'email' field is present.

### 3. Test Invalid Form - Password Mismatch

**Step:**
- Provide data for the `SignUpForm` with mismatched passwords:
  - `username`: 'testuser'
  - `email`: 'testuser@example.com'
  - `password1`: 'strongpassword123'
  - `password2`: 'weakpassword123'

**Expected Result:**
- The form should be invalid.
- An error for the 'password2' field should be present.

**Actual Result:**
- The form is invalid.
- An error for the 'password2' field is present.

### 4. Test Invalid Form - Existing User

**Step:**
- Create a user with the username 'existinguser'.
- Provide data for the `SignUpForm` with an existing username:
  - `username`: 'existinguser'
  - `email`: 'newuser@example.com'
  - `password1`: 'strongpassword123'
  - `password2`: 'strongpassword123'

**Expected Result:**
- The form should be invalid.
- An error for the 'username' field should be present.

**Actual Result:**
- The form is invalid.
- An error for the 'username' field is present.



## RegisterViewTestCase

### 1. Test Register View - GET Request

**Step:**
- Send a GET request to the registration URL.

**Expected Result:**
- The response status code should be 200.
- The response should use the 'registration/register.html' template.

**Actual Result:**
- The response status code is 200.
- The response uses the 'registration/register.html' template.

### 2. Test Register View - POST Request with Valid Form

**Step:**
- Send a POST request to the registration URL with valid form data:
  - `username`: 'testuser'
  - `password1`: 'testpassword123'
  - `password2`: 'testpassword123'

**Expected Result:**
- The response status code should be 302 (redirect).
- The response should redirect to the 'home' URL.
- The user with username 'testuser' should be created.

**Actual Result:**
- The response status code is 302.
- The response redirects to the 'home' URL.
- The user with username 'testuser' is created.

### 3. Test Register View - POST Request with Invalid Form

**Step:**
- Send a POST request to the registration URL with missing form data.

**Expected Result:**
- The response status code should be 200.
- The form should have errors indicating that 'username', 'password1', and 'password2' are required.

**Actual Result:**
- The response status code is 200.
- The form errors indicate that 'username', 'password1', and 'password2' are required.

### 4. Test Register View - POST Request with Password Mismatch

**Step:**
- Send a POST request to the registration URL with mismatched passwords:
  - `username`: 'testuser'
  - `password1`: 'testpassword123'
  - `password2`: 'testpassword321'

**Expected Result:**
- The response status code should be 200.
- The form should have an error message indicating that the two password fields didn’t match.

**Actual Result:**
- The response status code is 200.
- The form has an error message indicating that the two password fields didn’t match.

### 5. Test Register View - Authenticated User

**Step:**
- Authenticate a user with username 'existing_user' and password 'password123'.
- Send a GET request to the registration URL.

**Expected Result:**
- The response status code should be 302 (redirect).
- The user should be redirected to the home page.

**Actual Result:**
- The response status code is 302.
- The user is redirected to the home page.

# Roastery unit tests

## PurchaseEnquiryFormTest

### 1. Test Valid Form

**Step:**
- Provide valid form data for `PurchaseEnquiryForm`:
  - `product_name`: (HiddenInput widget)
  - `product_price`: (HiddenInput widget)
  - `name`: 'John Doe'
  - `address`: '123 Main St'
  - `contact_number`: '+1234567890'
  - `email_address`: 'john.doe@example.com'
  - `grind`: GRIND_CHOICES[0][0]

**Expected Result:**
- The form should be valid.

**Actual Result:**
- The form is valid.

### 2. Test Invalid Contact Number

**Step:**
- Provide form data for `PurchaseEnquiryForm` with an invalid contact number:
  - `product_name`: 'Coffee'
  - `product_price`: '10.00'
  - `name`: 'John Doe'
  - `address`: '123 Main St'
  - `contact_number`: '123456'  (invalid phone number)
  - `email_address`: 'john.doe@example.com'
  - `grind`: GRIND_CHOICES[0][0]

**Expected Result:**
- The form should be invalid.
- An error for the 'contact_number' field should be present.

**Actual Result:**
- The form is invalid.
- An error for the 'contact_number' field is present.

### 3. Test Missing Required Fields

**Step:**
- Provide incomplete form data for `PurchaseEnquiryForm`:
  - `product_name`: 'Coffee'
  - `product_price`: '10.00'
  - `name`: 'John Doe'
  - (Missing `address`, `contact_number`, `email_address`, `grind`)

**Expected Result:**
- The form should be invalid.
- Errors for 'address', 'contact_number', 'email_address', and 'grind' should be present.

**Actual Result:**
- The form is invalid.
- Errors for 'address', 'contact_number', 'email_address', and 'grind' are present.

## ProductFormTest

### 1. Test Valid Form with Image

**Step:**
- Provide valid form data for `ProductForm` including an image:
  - `category`: (valid category ID)
  - `origin_id`: (valid origin ID)
  - `grind_id`: (valid grind ID)
  - `size_id`: (valid size ID)
  - `manufacturer`: 'Acme Corp'
  - `name`: 'Premium Coffee'
  - `description`: 'The best coffee in town.'
  - `price`: '20.00'
  - `currency`: 'USD'
  - `image`: (a valid image file)

**Expected Result:**
- The form should be valid.

**Actual Result:**
- The form is valid.

### 2. Test Invalid Price

**Step:**
- Provide form data for `ProductForm` with an invalid price:
  - `category`: (valid category ID)
  - `origin_id`: (valid origin ID)
  - `grind_id`: (valid grind ID)
  - `size_id`: (valid size ID)
  - `manufacturer`: 'Acme Corp'
  - `name`: 'Premium Coffee'
  - `description`: 'The best coffee in town.'
  - `price`: 'invalid-price'
  - `currency`: 'USD'
  - `image`: (a valid image file)

**Expected Result:**
- The form should be invalid.
- An error for the 'price' field should be present.

**Actual Result:**
- The form is invalid.
- An error for the 'price' field is present.

### 3. Test Missing Required Fields

**Step:**
- Provide incomplete form data for `ProductForm`:
  - `category`: (valid category ID)
  - `origin_id`: (valid origin ID)
  - (Missing `grind_id`, `size_id`, `manufacturer`, `name`, `description`, `price`, `currency`, `image`)

**Expected Result:**
- The form should be invalid.
- Errors for 'grind_id', 'size_id', 'manufacturer', 'name', 'description', 'price', 'currency' should be present.

**Actual Result:**
- The form is invalid.
- Errors for 'grind_id', 'size_id', 'manufacturer', 'name', 'description', 'price', 'currency' are present.

## ProductViewTests

### 1. Test Create Product View - GET Request

**Step:**
- Send a GET request to the 'create_product' URL.

**Expected Result:**
- The response status code should be 200.
- The response should use the 'roastery/product_form.html' template.

**Actual Result:**
- The response status code is 200.
- The response uses the 'roastery/product_form.html' template.

### 2. Test Create Product View - POST Request

**Step:**
- Send a POST request to the 'create_product' URL with form data:
  - `product_id`: 2
  - `category`: 1
  - `origin_id`: 1
  - `grind_id`: 2
  - `size_id`: 0
  - `manufacturer`: "Acme Corp"
  - `name`: "Premium Coffee"
  - `description`: "The best coffee in town."
  - `price`: Decimal("7.54")
  - `currency`: "GBP"
  - `image`: ""

**Expected Result:**
- The response should redirect to 'manage_products' with a success message: "Product created successfully!"

**Actual Result:**
- The response redirects to 'manage_products' with the success message: "Product created successfully!"

### 3. Test Update Product View - GET Request

**Step:**
- Send a GET request to the 'update_product' URL with the product ID.

**Expected Result:**
- The response status code should be 200.
- The response should use the 'roastery/product_form.html' template.

**Actual Result:**
- The response status code is 200.
- The response uses the 'roastery/product_form.html' template.

### 4. Test Update Product View - POST Request

**Step:**
- Send a POST request to the 'update_product' URL with form data:
  - `name`: "Updated Product"
  - `price`: Decimal("10.99")

**Expected Result:**
- The response should redirect to 'manage_products' with a success message: "Product updated successfully!"

**Actual Result:**
- The response redirects to 'manage_products' with the success message: "Product updated successfully!"

## Button Tests

### 1. Button Click to Create Product

**Step:**
- Click the "Create Product" button on the manage products page.

**Expected Result:**
- The user should be redirected to the product creation form page.

**Actual Result:**
- The user is redirected to the product creation form page successfully.

### 2. Button Click to Delete Product

**Step:**
- Click the "Delete" button for a specific product in the product list.

**Expected Result:**
- A confirmation dialog should appear, asking if the user is sure they want to delete the product.

**Actual Result:**
- A confirmation dialog appears as expected.


### 3. Button Click to Update Product

**Step:**
- Click the "Update" button next to a specific product in the product list.

**Expected Result:**
- The user should be redirected to the product update form page for the selected product.

**Actual Result:**
- The user is redirected to the product update form page successfully.

### 4. Button Click to Submit Product Form

**Step:**
- Fill in the product form and click the "Submit" button.

**Expected Result:**
- The user should see a success message indicating the product was created successfully, and they should be redirected to the product list page.

**Actual Result:**
- A success message is displayed, and the user is redirected to the product list page as expected.


