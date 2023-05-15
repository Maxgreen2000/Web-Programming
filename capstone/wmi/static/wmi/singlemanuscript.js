document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            document.getElementById('ContactPoster').addEventListener('click', function() {
                document.querySelector('#manuscript-details-view').style.display = 'none';
                document.querySelector('#ContactPoster').style.display = 'none';
                document.querySelector('#compose-new-email-view').style.display = 'block';
            })
            document.querySelector("#compose-form").addEventListener('submit', send_email);
        }
    })
});

function send_email(event) {
    event.preventDefault(); // STOP THE SUBMITTING OF THE FORM RELOADING PAGE. SHOULD TAKE US TO THE SEND PAGE
    
    //Save values from each input in the compose form
    const recipients = document.querySelector('#compose-recipient').value;
    const manuscript = document.querySelector('#compose-manuscript').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    //Send data to the back-end
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        manuscript: manuscript,
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent');
    });
  }