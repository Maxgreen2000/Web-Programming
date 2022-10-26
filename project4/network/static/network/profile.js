document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#followButton").addEventListener('click', addFollow);

});

profile_name = document.querySelector('#profile-name').value;


function addFollow() {
    fetch('/addFollow', {
        method: 'POST',
        profile_name: profile_name
    })
    .then(() => {
        window.location.reload();      //This reloads the page thus clearing out the new post box , brings the new post up to the top as well as anyone elses.
    })
}