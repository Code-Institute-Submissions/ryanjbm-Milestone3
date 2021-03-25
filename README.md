# Hidden Gems: Milestone Project 3

[Live Project](http://hiddengems-milestone3.herokuapp.com/)

<img src="assets/images/responsive.png">

# Introduction
Hidden Gems is a site made so that people can join the community and share the products that they love to friends, family and strangers. The site labels products under £20 as a 'Hidden Gem' and provides people with external links to the products.

This is my second Milestone Project for my Full Stack Development Course at The Code Institute, in which I was given the instructions to make an Interactive Front End Project. In creating this website I used CSS3, HTML5 and JavaScript.

# UX

### Goals

* To make my Madrid Tourism website provide users with sufficient information about where they should eat and visit in Madrid
* To create an aesthetically pleasing and easy to navigate webpage for the user
* To use Interactive and effective features on my website
* Successful use of APIs in the webpage

### User Stories

1. I am a user looking for general tourism information about Madrid
1. I am a user looking for places to eat in Madrid
1. I am a user looking for directions to landmarks in Madrid
1. I am a user who wants to request other specific information about Madrid
1. I am a user wishing to find out information on events taking place in Madrid


### Design Process

1. I began my process by making a plan of how I wanted to layout my website. I came to the decision to do a single page website split into different sections including "Hero Section", "About Section", "Map Section", "Places to Eat & Visit" and a "Contact Form".
1. Throughout my design process I used a simple colour scheme and only a few fonts for my page, the colours I used were: <br>
  #fafafa (Background and some text)<br>
  Black (Most of text and button background)<br>
  Green (USed when hovering over menu items, card info and Map info window)<br>
  Orange  (Used for hovering and clicking buttons on page)<br>
After some experimentation and changes throughout the design and building process these were the colours that I decided look the best, the fonts I used were the following:<br>
  Righteous <br>
  Padauk <br>
  Permanent Marker <br>
1. I made a wireframe for my project using FIGMA. I made the design aesthetically pleasing and made sure it was easy to navigate through. I first made my desktop page and then made my mobile layout. Throughout the process of building my website I made a few changes and additions based off of my experience as well as input from family and friends
1. Some of the changes I made included adding images to separate sections and a few colours and where they are used.



# [Figma Wireframe](https://www.figma.com)
> This includes the wireframes for both desktop and mobile device layouts
<img src="assets/images/figma.png">

Throughout the process of coding my website and input from other people, a few improvements were made to the website to not only make it look more professional but also to include more useful features.


# Features

### Features throughout page
* Collapsible Navigation Bar which is stuck to the top of the page, once scrolling menu becomes slightly opaque
* Back to top button in bottom right corner of the page, stays on screen whole time
* Images throughout the page zoom in when mouse hovers over them
* Content fades in as scrolling down

### Nav Bar
* Collapsable Nav Bar
* Text turns green on hover
* When clicked scrolls down to section on page

### Hero Section
* Background hero image of Madrid with overlay text, event info with arrow overlay at the bottom
* Scrolling text underneath the image showing event information

### Map
* Google Map api used
* Legend showing what each custom marker image stands for, on mobile legend appears below
* When clicking each marker info window shows with name of place and link to google maps directions for the place

### Places to eat & visit
* Separating images with overlay text zoom on hover
* Card images zoom on hover
* Read more buttons show text when clicked and button changes to say Read Less, text colour changes when hovering over
* Link scrolling up to map when clicked, zooms and centers on custom marker
* When clicking on image redirects to the website of restaurant or website with information about place to visit

### Contact Form
* Email js api used
* Checks all fields are filled before allowing to submit
* Once submitted alert box opens showing message has been sent
* Page refreshes afterwards
* Functional contact form which sends email to my account, showing who sent the email

### Example of email received via contact form
<img src="assets/images/email.png">


# Technologies Used

### Languages
* HTML5
  * Base language for the project used to add content to the website
* CSS3 
  * Used to style content
* JavaScript
  * Usd to add Interactive features to webpage
  
  
### Technologies
* [Bootstrap Framework](https://getbootstrap.com)
  * Used Bootstrap's grid system and styles for buttons to help the web page be more responsive for mobile layouts as well as for my navbar
* [FontAwesome](https://fontawesome.com)
  * Used for social links in footer, hero image, navbar and back to top button
* [Google Fonts](https://fonts.google.com)
  * Used Righteous, Padauk and Permanent Marker
* [Google Images](https://www.google.co.uk/imghp?hl=en&tab=wi&authuser=0&ogbl)
  * Used for all of my images, each was checked to be copyright free
* [W3 Schools](https://www.w3schools.com)
  * Used for help with the code in my project, I found it very useful for my form and gallery page
* [W3C Markup Validation](https://validator.w3.org)
  * Used this to check that my HTML and CSS code were both valid throughout my project
* [Stack Overflow](https://stackoverflow.com)
  * I used this to help me with small issues I encountered when writing my code
* [Google Maps API](https://developers.google.com/maps/documentation)
  * Used to get the code and key to use google maps api in my website
* [Icons8](https://icons8.com/)
  * I used this website to get custom markers for my Google Maps Api
  
  
# Testing

### Testing User Stories

1. User was looking for general information about Madrid, was able to find this by reading about section at top of page, navigated to by scrolling or clicking link in the navbar
1. User looking for places to eat in Madrid, by clicking the places to eat & visit link was able to click read more button to see information about restaurants, redirect to website of place or click link to see the location in the map
1. User looking for directions to landmarks in Madrid, they scrolled down to the map and by looking at the legend found the markers marked as landmarks
1. User wanting to request specific information about Madrid scrolled down to the bottom of the website to the contact form, filled in the fields and submitted their message, alert box showed giving user confirmation that it has been sent
1. User looking to find out about events in madrid was able to read the scrolling information bar underneath the hero image to read about events coming up

### Testing Devices

My webpage was tested using Google Developer Tools to see if it's responsive. All devices were tested successfully including Iphones, Samsungs and Ipads of different screen sizes

### Validating HTML5 and CSS3 code

My code was tested on the WC3 Validation pages and passed all tests

### Different Browsers

I tested my page on the following browsers and found it worked on all

* Safari
* Chrome
* Firefox

### Issues

During my code I had issues with having custom info windows for my Google Maps API and the code for my Read More buttons did not pass the WC3 Validator. These issues were overcome by trial and error with the code myself.

# Deployment

### Deploying

I created my Milestone project using the GitPod environment and pushing it to Github after completing each section, this made sure that my project had good version control in place in case I needed to change some of the work. To create a live version of my project for people to view I did the following:

* Went to my Milestone Project repository on GitHub
* Went to settings and scrolled down to GitHub Pages
* Selected the master branch as source which then gave me the link to include in my ReadMe for people to view
* You can view my project here: [Madrid](https://ryanjbm.github.io/Milestone-Project-2/)

To run locally, you can clone this repository directly into the editor of your choice by pasting git clone https://github.com/ryanjbm/Milestone-Project-2.git into the terminal. To cut ties with this GitHub repository, type git remote rm origin into the terminal.

# Credits

### Content

The content of my website was written by me, however names and locations of places are real.

### Media

Images I used were free to use but came from the following websites:

* [Google Images](https://www.google.co.uk/imghp?hl=en&tab=wi&authuser=0&ogbl)

Code snippets that I used for my read more buttons scrolling text came from the following website:

* [StackOverflow](https://stackoverflow.com)

### Acknowledgments

# Pages for information

* [Stack Overflow](https://stackoverflow.com)
* [W3schools](https://www.w3schools.com)
* [W3c](https://validator.w3.org)
* [Bootstrap](https://getbootstrap.com)

Thank you to the following for the support on issues and for offering advice on my project throughout:
* Code Institute Mentor Brian Macharia
* Code Institute Tutor
* Code Institute Slack Community
* Family and friends for constructive criticism





  
