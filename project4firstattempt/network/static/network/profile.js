document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#editform").addEventListener('submit', editPost);

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

function editPost() {

    var editform = document.createElement("form");
    editform.setAttribute("method", "post");

    var FN = document.createElement("input");
    FN.value = "hello"
    FN.setAttribute("type", "text");
    FN.setAttribute("name", "body");
    FN.setAttribute("placeholder", "Full Name");

    var s = document.createElement("input");
    s.setAttribute("type", "submit");
    s.setAttribute("value", "Submit");
     
    editform.appendChild(FN);
    editform.appendChild(s);
    editformdiv = document.getElementById( 'editformdiv' );
    editformdiv.appendChild( editform );
    editform.id = 'editform_id' ;

}