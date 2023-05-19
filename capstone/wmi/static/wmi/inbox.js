document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
  document.querySelector('#compose-view').style.display = 'none';
  load_conversations();
});

function openmanuscriptinnewtab(manuscriptid) {
  window.open(`/manuscript/${manuscriptid}`, '_blank');
}


function load_conversations() {
  fetch(`/conversations`)
  .then(response => response.json())
  .then(conversations => {
      conversations.forEach(conversation => { 
        const createdconversation = document.createElement('div');
        createdconversation.className="list-group-item";
        conversation.participants.forEach((item) => {
          if(document.getElementById('useremail').innerHTML != item){
            createdconversation.innerHTML += `<h1>${item}</h1>`
          }
        });
        createdconversation.innerHTML +=`
          <h2>${conversation.manuscript}</h2>
          <p>${conversation.timestamp}</p>
        `;

        createdconversation.addEventListener('click', function() {
          view_conversation(conversation.id)
        });
        document.querySelector('#conversations_view').append(createdconversation);
      })
  });
}


function view_conversation(id) {
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#conversations_view').style.display = 'none';

  fetch(`/messages/${id}`)
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

