document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#new-post-form").addEventListener('submit', new_post);

});

function new_post(event) {
    event.preventDefault();     
 
    const body = document.querySelector('#post-body').value;
    const poster = document.querySelector('#poster-name').value;
      
    //Send data to the back-end
    fetch('/new_posts', {
        method: 'POST',
        body: JSON.stringify({
            body: body,
            poster: poster
         })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
}
      
