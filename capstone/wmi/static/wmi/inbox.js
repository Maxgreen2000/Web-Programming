document.addEventListener('DOMContentLoaded', function() {
  // By default, load the inbox
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
          //SET THE VALUE OF COMPOSE FORM TO THIS CONVO PARTICPANT ID FOR THE RECIPIENT OF THE EMAIL
          conversation.participants_id.forEach((item) => {
            if(document.getElementById('useridreference').innerHTML != item){
              document.getElementById('compose_recipient_id').value = item
            }
          });
          document.getElementById('compose_manuscript_id').value = conversation.manuscript_id
          view_conversation(conversation.id)
        });
        document.querySelector('#conversations_view').append(createdconversation);
      })
  });

}

function conversation_view() {
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-new-email-view').style.display = 'block';
  document.querySelector('#conversations_view').style.display = 'none';
 }

function view_conversation(id) {
  conversation_view()

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

function send_email(manuscript_id) {
    
  manuscript_id = document.getElementById('manuscript_id').value
  poster_id = document.getElementById('poster_id').value

  //Save values from each input in the compose form
  const recipient = document.querySelector('#compose-recipient-id').value;
  const body = document.querySelector('#compose-body').value;

  //Send data to the back-end
  fetch(`/createmessage/${manuscript_id}/${poster_id}`, {
    method: 'POST',
    body: JSON.stringify({
      recipient: recipient,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      view_conversation()
  });
}
