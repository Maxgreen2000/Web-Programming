document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#followButton").addEventListener('click', createFollow);

});

function createFollow() {

    const body = document.querySelector('#poster-name').value;

    fetch('/createFollows', {
        method: 'POST',
        body: JSON.stringify({
            body: body,
         })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }) .then(() => {
        window.location.reload();      //This reloads the page thus clearing out the new post box , brings the new post up to the top as well as anyone elses.
    })

}