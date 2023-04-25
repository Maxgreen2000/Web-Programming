document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  load_mailbox('inbox');
});

function load_mailbox(mailbox) {
  
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => { 
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

        createdemail.addEventListener('click', function() {
          view_email(email.id)
        });
  
  
        document.querySelector('#emails-view').append(createdemail);
      })
  });

}

