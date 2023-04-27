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
      <li class="list-group-item"><a href="#" id="manuscriptlink">${email.manuscripttitle}</a></li>
      <li class="list-group-item">Time: ${email.timestamp}</li>
      <li class="list-group-item"><p>${email.body}</p></li>
    </ul>`
    manuscriptlink = document.getElementById('manuscriptlink')
    manuscriptlink.addEventListener('click', function() {
      view_manuscript(email.manuscriptid)
    })
  });


}

function view_manuscript(id) {
  manuscriptview = document.getElementById('manuscript-view')
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#manuscript-view').innerHTML = "";
  document.querySelector('#manuscript-view').style.display = 'block'

  //Add a link that goes back to search filters
  const returntoresults = document.createElement('button');
  returntoresults.innerHTML = "Back to Email"
  returntoresults.addEventListener('click', function() {
      document.querySelector('#manuscript-view').style.display = 'none';
      document.querySelector('#email-content-view').style.display = 'block';
  })

  fetch(`/manuscript/${id}`)
  .then(response => response.json())
  .then(manuscript => {
    manuscriptview.innerHTML = `
      <img src="${manuscript.imageurl}" alt="${manuscript.title}" height="450px">
      <ul class="list-group">
          <li class="list-group-item">id: ${manuscript.poster}</li>
          <li class="list-group-item">id: ${manuscript.id}</li>
          <li class="list-group-item">title: ${manuscript.title}</li>
          <li class="list-group-item">location: ${manuscript.location}</li>
          <li class="list-group-item">Date Range: ${manuscript.yearfrom} - ${manuscript.yearto}</li>
          <li class="list-group-item">tags: ${manuscript.tags}</li>
          <li class="list-group-item"><p>Transcript: ${manuscript.transcript}</p></li>
      </ul>`
  manuscriptview.prepend(returntoresults)
  })

}