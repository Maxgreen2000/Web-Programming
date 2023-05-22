createdconversation.addEventListener('click', function() {
    //SET THE VALUE OF COMPOSE FORM TO THIS CONVO PARTICPANT ID FOR THE RECIPIENT OF THE EMAIL
    conversation.participants_id.forEach((item) => {
      if(document.getElementById('useridreference').innerHTML != item){
        document.getElementById('compose_recipient_id').value = ${item}
      }
    view_conversation(conversation.id)
    });
    document.querySelector('#conversations_view').append(createdconversation);
  })