document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#follow_button').addEventListener('click', add_follow);

});


function add_follow() {
    profile_name = document.querySelector('#profile_name').value;

    fetch('/add_follow', {
        method: 'POST',
        body: JSON.stringify({
            profile_name: profile_name
         })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }) 
}
      