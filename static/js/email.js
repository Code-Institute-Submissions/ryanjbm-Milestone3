/*----------------------------------Email function*/

function sendMail(contactForm) {
    emailjs.send("gmail", "HiddenGems-email", {
            "from_name": contactForm.name.value,
            "from_email": contactForm.emailaddress.value,
            "contact_request": contactForm.projectsummary.value
        })
        .then(
            function(response) {
                console.log("Success", response);
            },
            function(error) {
                console.log("Failed", error);
            }
        );
    return false;
}


/*Allows alert to show message has been sent*/

function alertFunction() {
    alert("Message has been sent!");
}