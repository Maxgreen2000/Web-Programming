document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            document.getElementById('ContactPoster').addEventListener('click', function() {
              view_conversation()
            })
            document.getElementById('BackToEntry').addEventListener('click', function() {
                manuscript_view()
            })
            document.getElementById('send_button').addEventListener('click', function() {
              send_email()
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

 function conversation_view() {
  document.querySelector('#emails-view').innerHTML = "";
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-new-email-view').style.display = 'block';
  document.querySelector('#manuscript-details-view').style.display = 'none';
 }

function send_email() {
    
    manuscript_id = document.getElementById('manuscript_id').value

    //Save values from each input in the compose form
    const recipient = document.querySelector('#compose-recipient-id').value;
    const body = document.querySelector('#compose-body').value;

    //Send data to the back-end
    fetch(`/createmessage/${manuscript_id}`, {
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

  function view_conversation() {

    conversation_view()

    manuscript_id = document.getElementById('manuscript_id').value
    poster_id = document.getElementById('poster_id').value


  
    fetch(`/find_conversation/${manuscript_id}/${poster_id}`)
    .then(response => response.json())
    .then(conversation => {
        conversation.participants.forEach((item) => {
          if(document.getElementById('useremail').innerHTML != item){
            createdconversation.innerHTML += `<h1>${item.id}</h1>`
          }
        });
        fetch(`/messages/${conversation.id}`)
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
        })
      })
  }
  
