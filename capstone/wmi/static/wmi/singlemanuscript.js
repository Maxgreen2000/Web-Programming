document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            document.getElementById('ContactPoster').addEventListener('click', function() {
              view_conversation()
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
    fetch('/createmessage', {
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

  function view_conversation() {

    manuscript_id = document.getElementById('manuscript_id').value
    poster_id = document.getElementById('poster_id').value

    document.querySelector('#emails-view').innerHTML = "";
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-new-email-view').style.display = 'none';
    document.querySelector('#manuscript-details-view').style.display = 'none';
  
    fetch(`/find_conversation/${manuscript_id}/${poster_id}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => { 
          const createdemail = document.createElement('div');
          createdemail.className="list-group-item";
          createdemail.innerHTML =`
            <h1>${email.sender}</h1>
            <p>${email.timestamp}</p>
            <h2>${email.body}</h2>
          `;
  
          document.querySelector('#emails-view').append(createdemail);
        })
    });
  
  }
  
