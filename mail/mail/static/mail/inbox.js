document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Need to load the appropriate emails for whatever mailbox is being viewed
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => { //We can loop through the whole array emails an email at a time using forEach
        //THIS IS SELECTED JUST ONE OF THE EMAILS
        //Make the email styling for each email in inbox
        const createdemail = document.createElement('div');
        createdemail.className="list-group-item";
        createdemail.innerHTML =`
          <h1>From: ${email.sender}</h1>
          <h2>Subject: ${email.subject}</h2>
          <p>${email.timestamp}</p>
        `;

        if(email.read == true){
          createdemail.id = 'read'
        }
        else{
          createdemail.id = 'unread'
        }

        //THIS ADDS AN EVENTLISTENER TO EACH EMAIL IN THE INBOX THAT WHEN THE DIV IS CLICKED ON IT PASSES THE ID TO VIEW EMAIL
        createdemail.addEventListener('click', function() {
          view_email(email.id)
        });
  
  
        document.querySelector('#emails-view').append(createdemail);
      })
  });

}

function send_email(event) {
  event.preventDefault(); // STOP THE SUBMITTING OF THE FORM RELOADING PAGE. SHOULD TAKE US TO THE SEND PAGE

  //Save values from each input in the compose form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  //Send data to the back-end
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
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

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-content-view').innerHTML = `
    <ul class="list-group">
      <li class="list-group-item">From: ${email.sender}</li>
      <li class="list-group-item">To: ${email.recipients}</li>
      <li class="list-group-item">Subject: ${email.subject}</li>
      <li class="list-group-item">Time: ${email.timestamp}</li>
      <li class="list-group-item"><p>${email.body}</p></li>
    </ul>`

    //NOW MARK THE EMAIL AS READ
    if(!email.read){  // THIS WILL ONLY SEND THE PUT IF THE EMAIL HASN'T BEEN READ YET, SAVING TIME IN FUTURE.
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

    //ADD ARCHIVE BUTTON AT BOTTOM OF EMAIL
    
    if(email.sender != document.getElementById('useremail').innerHTML){
      const archivebutton = document.createElement('div');
      archivebutton.className="btn btn-outline-primary m-2";
      archivebutton.innerHTML = email.archived ? "Unarchive" : "Archive";
      archivebutton.addEventListener('click', function() {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived //This will do the opposite of whatever it currently is
          })
        })
        load_mailbox('inbox')
        location.reload()
      });
      document.querySelector('#email-content-view').append(archivebutton);
    }

    //now need to add a reply button 
    const replybutton = document.createElement('button');
    replybutton.innerHTML = "Reply"
    replybutton.className= "btn btn-outline-primary m-2";

    replybutton.addEventListener('click', function() {
      //CLEAR OUT EVERYTHING
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#email-content-view').style.display = 'none';
      document.querySelector('#compose-recipients').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-body').value = '';

      document.querySelector('#compose-recipients').value = email.sender;

      //WE CAN PUT RE: IN FRONT OF THE SUBJECT BUT ONLY ONCE
      subject = email.subject;
      if(subject.split(' ',1)[0] != "Re:"){
        document.querySelector('#compose-subject').value  = "Re: " + subject;
      }
      else{
        document.querySelector('#compose-subject').value = subject;
      }
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"`;
    });


    document.querySelector('#email-content-view').append(replybutton);
  });

}