document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            document.getElementById('ContactPoster').addEventListener('click', function() {
                compose_view()
            })
            document.querySelector("#compose-form").addEventListener('submit', send_email);
            document.getElementById('BackToEntry').addEventListener('click', function() {
                manuscript_view()
            })
        }
    })
});

function manuscript_view() {
    document.querySelector('#compose-subject').value = "";
    document.querySelector('#compose-body').value = "";
    document.querySelector('#compose-new-email-view').style.display = 'none';
    document.querySelector('#manuscript-details-view').style.display = 'block';
    document.querySelector('#ContactPoster').style.display = 'block';
 }

 function compose_view() {
    document.querySelector('#compose-subject').value = "";
    document.querySelector('#compose-body').value = "";
    document.querySelector('#compose-new-email-view').style.display = 'block';
    document.querySelector('#manuscript-details-view').style.display = 'none';
    document.querySelector('#ContactPoster').style.display = 'none';
 }

function send_email(event) {
    event.preventDefault(); // STOP THE SUBMITTING OF THE FORM RELOADING PAGE. SHOULD TAKE US TO THE SEND PAGE
    
    //Save values from each input in the compose form
    const recipient = document.querySelector('#compose-recipient-id').value;
    const manuscript = document.querySelector('#compose-manuscript').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    //Send data to the back-end
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        manuscript: manuscript,
        recipient: recipient,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        manuscript_view()
    });
  }


