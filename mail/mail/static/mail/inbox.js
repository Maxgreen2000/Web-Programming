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
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#emails-detail-view').style.display = 'block';

      document.querySelector('#emails-detail-view').innerHTML = `
        <ul class="list-group">
          <li class="list-group-item"><strong>From:</strong> ${email.sender}</li>
          <li class="list-group-item"><strong>From:</strong> ${email.recipients}</li>
          <li class="list-group-item"><strong>Subject:</strong> ${email.subject}</li>
          <li class="list-group-item"><strong>Time:</strong> ${email.timestamp}</li>
          <li class="list-group-item"><p>${email.body}</p></li>
        </ul>
        `

      //Change the value of read? to read.
      if(!email.read){
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }

      //Archive the email?
      const archive_button = document.createElement('button');
      archive_button.innerHTML = !email.archived ? "Archive" : "Unarchive";
      archive_button.className= email.archived ? "btn btn-outline-danger btn-lg" : "btn btn-outline-primary btn-lg";
      archive_button.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => { load_mailbox('archive')})
      });
      document.querySelector('#emails-detail-view').append(archive_button);

      //REPLY BUTTON
      const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply"
      reply_button.className= "btn btn-outline-primary btn-lg m-3";

      reply_button.addEventListener('click', function() {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if(subject.split(' ',1)[0] != "Re:"){
          subject = "Re: " + email.subject;
        }
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      });


      document.querySelector('#emails-detail-view').append(reply_button);
  });

}


















function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Display all the emails for a particular user
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails by looping through them all and follow the hint given
    emails.forEach(singleEmail => {

      console.log(singleEmail);

      //creates a div for each email for any of the views we are on
      const newEmail = document.createElement('div');
      newEmail.className="list-group-item";
      newEmail.innerHTML =`
        <h6>From: ${singleEmail.sender}</h6>
        <h5>Subject: ${singleEmail.subject}</h5>
        <p>${singleEmail.timestamp}</p>
        <hr>
      
      `;

      //Change colour when read. Below is an if statement that can be used for boolean values. if true use the first style, if false use the second.
      newEmail.className = singleEmail.read ? 'read': 'unread';


      newEmail.addEventListener('click', function() {
        view_email(singleEmail.id)
      });
      document.querySelector('#emails-view').append(newEmail);

    })

    
});
}

function send_email(event) {
  event.preventDefault();


  //Save our values for each section of composing the email 
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

