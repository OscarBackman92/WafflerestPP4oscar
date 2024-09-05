# Functional Testing

| Description      | Steps                                                                                                                                           | Expected                                                                       | Actual                                                                         | Pass |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ---- |
| open website     | open website                                                                                                                                    | Homepage                                                                       | Homepage                                                                       | Pass |
| View menu        | Press menu in navbar                                                                                                                            | Menu view                                                                      | Menu view                                                                      | Pass |
| Book a table     | Press book a table in navbar                                                                                                                    | Booking form                                                                   | Booking form                                                                   | Pass |
| Make a booking   | Select a table, Select date, time and number of guests, Press sumbit booking                                                                    | See booking comfirmed message, booking details, and recive confim booking mail | See booking comfirmed message, booking details, and recive confim booking mail | Pass |
| Edit a booking   | Go to my bookings in navbar, select the booking you want to edit, Press actions and select edit, edit what you want and submit                  | See booking updated message and booking details, recive booking updated mail   | See booking updated message and booking details, recive booking updated mail   | Pass |
| Delete a booking | Go to my bookings in navbar, select the booking you want to delete, Press actions and select delete, press OK on alert message and delete again | See delete message and recive cancellation main                                | See delete message and recive cancellation mail                                | Pass |
| Make account     | Press login, click on sign up link, type in your preferred username and password. Email is optional                                             | See message on home page Successfully signed in as username                    | See message on home page Successfully signed in as username                    | Pass |
| logout           | Press logout in navbar then sign out                                                                                                            | See message you have signed out                                                | See message you have signed out                                                | Pass |

## Navigation links

Testing was performed to ensure all navigation links on the respective pages, navigated to the correct pages as per design. This was done by clicking on the navigation links on each page.

- See markdown testing above for navigation links and how they work

All navigation links directed to the correct pages as expected.

## Footer

Testing was performed on the footer links by clicking the font awesome icons and ensuring that the facebook icon opened facebook in a new tab and the twitter icon opened twitter and the linkedin icon opened linkedin in a new tab. These behaved as expected.

## Negative Testing

Tests were performed on the create booking to ensure that:

1. A customer cannot book a date in the past. need to check
2. A customer cannot book if no tables are available for the amount of guests
3. A customer cannot edit a booking with an increased guest size if no tables have capacity
4. Forms cannot be submitted when required fields are empty.

## Unit Testing

Unit tests were created to test some basic functionality such as templates used and redirects. These can be found in the tests.py files in the respective apps.

Results:

![unit tests](docs/readme_images/unit_test.png)

## Accessibility

[Wave Accessibility](https://wave.webaim.org/) tool was used throughout development and for final testing of the deployed website to check for any aid accessibility testing.

Testing was focused to ensure the following criteria were met:

- All forms have associated labels or aria-labels so that this is read out on a screen reader to users who tab to form inputs
- Color contrasts meet a minimum ratio as specified in [WCAG 2.1 Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- Heading levels are not missed or skipped to ensure the importance of content is relayed correctly to the end user
- All content is contained within landmarks to ensure ease of use for assistive technology, allowing the user to navigate by page regions
- All not textual content had alternative text or titles so descriptions are read out to screen readers
- HTML page lang attribute has been set
- Aria properties have been implemented correctly
- WCAG 2.1 Coding best practices being followed

## Validator Testing

All pages were run through the [w3 HTML Validator](https://validator.w3.org/). Initially there were some errors due to stray script tags, misuse of headings within spans and some unclosed elements. All of these issues were corrected and all pages passed validation. There is an Error on line 55 in base.html that i cant seem to fix, but it works.

Due to the django templating language code used in the HTML files, these could not be copy and pasted into the validator and due to the secured views, pages with login required or a secured view cannot be validated by direct URI. To test the validation on the files, open the page to validate, right click and view page source. Paste the raw html code into the validator as this will be only the HTML rendered code.

![HTML Validator](/docs/readme_images/homepage_validation.png)

![HTML Validator](/docs/readme_images/home_logged_in.png)

![HTML Validator](/docs/readme_images/menu_validation.png)

![HTML Validator](/docs/readme_images/menu_logged_in.png)

![HTML Validator](/docs/readme_images/book_a_table_validation.png)

![HTML Validator](/docs/readme_images/book_a_table_success_validation.png)

![HTML Validator](/docs/readme_images/edit_booking_validation.png)

![HTML Validator](/docs/readme_images/edit_booking_success_validation.png)

![HTML Validator](/docs/readme_images/delete_booking_validation.png)

![HTML Validator](/docs/readme_images/delete_booking_success_validation.png)

![HTML Validator](/docs/readme_images/my_booking_validation.png)

![HTML Validator](/docs/readme_images/)

## Styling

CSS was run through the offical [jigsaw_validator] to ensure that the styling is correct and working all throughout the site.

![jigsaw](docs/readme_images/css_validation.png)

All pages were run through the Code institute's [Pep8](https://pep8ci.herokuapp.com/#) validator to ensure all code was pep8 compliant. Some errors were shown due to blank spacing and lines too long, 1 line instead of 2 expected. All of these errors were resolved and code passed through validators with the exception of the settings.py file.

The django auto generated code for AUTH_PASSWORD_VALIDATORS were showing up as lines too long. I could not find a way to split these lines but since they were auto generated and not my own custom code, I hope this is acceptable.

![PEP8](docs/readme_images/bookin_urls_validation.png)

![PEP8](docs/readme_images/booking_admin_validation.png)

![PEP8](docs/readme_images/booking_forms_validation.png)

![PEP8](docs/readme_images/booking_models_validation.png)

![PEP8](docs/readme_images/booking_tests_validation.png)

![PEP8](docs/readme_images/booking_utils_validation.png)

![PEP8](docs/readme_images/booking_view_validation.png)

![PEP8](docs/readme_images/booking_widget_validation.png)

![PEP8](docs/readme_images/home_urls_validation.png)

![PEP8](/docs/readme_images/home_view_validation.png)

## Lighthouse Report

Lighthouse report showed areas for improvement on SEO. Could add more meta tags for this.

![Lighthouse v1](/docs/readme_images/lighthouse.png)

## Responsiveness

All pages were tested to ensure responsiveness on screen sizes from 360px and upwards as defined in WCAG 2.1 Reflow criteria for responsive design on Chrome, Edge, Firefox and Opera browsers.

Steps to test:

- Open browser and navigate to [Waffle](https://oscarwaffle-be7490c12beb.herokuapp.com/)
- Open the developer tools (right click and inspect)
- Set to responsive and decrease width to 360px
- Set the zoom to 50%
- Click and drag the responsive window to maximum width

Expected:

Website is responsive on all screen sizes and no images are pixelated or stretched. No horizontal scroll is present. No elements overlap.

Actual:

Website behaved as expected.

Website was also opened on the following devices and no responsive issues were seen:

Iphone 13
iPhone 15

## Bugs
