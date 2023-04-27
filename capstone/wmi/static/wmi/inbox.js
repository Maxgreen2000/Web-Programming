document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  document.querySelector('#compose-view').style.display = 'none';
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
          <p>${email.manuscriptid}</p>
          <p>${email.manuscripttitle}</p>
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

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'block';

  fetch(`/email/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#email-content-view').innerHTML = `
    <ul class="list-group">
      <li class="list-group-item">From: ${email.sender}</li>
      <li class="list-group-item">To: ${email.recipient}</li>
      <li class="list-group-item">Subject: ${email.subject}</li>
      <li class="list-group-item"><a href="/manuscript/${email.manuscriptid}">${email.manuscripttitle}</a></li>
      <li class="list-group-item">Time: ${email.timestamp}</li>
      <li class="list-group-item"><p>${email.body}</p></li>
    </ul>`
  });


}
