document.addEventListener('DOMContentLoaded', function() {

    var element = document.querySelector("#newpostform");

    if (element)
    element.addEventListener('submit', new_post);

    // By default, load the inbox
    indexpage();

});


function new_post() {
   
    const body = document.querySelector('#newpostbody').value;
    
    //Send data to the back-end
    fetch('/new_posts', {
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

function indexpage() {

    load_posts('0','allposts')

}



function load_posts(userid, page) {        //RENAME THIS TO LOAD POSTS , WE ARE NOT LOADING THE PAGES SIMPLY POSTING A SET AMOUNT OF POSTS TO YOUR SELECTED PAGE

    document.querySelector('#pageselected').innerHTML = `<h3>${page.charAt(0).toUpperCase() + page.slice(1)}</h3>`;
    document.querySelector('#posts-view').innerHTML = "";
    currentusername = document.querySelector('#currentusername').innerHTML;

  //Display all the posts for a particular user
  fetch(`/loadposts/${userid}/${page}`)
  .then(response => response.json())
  .then(posts => {
    // Print emails by looping through them all and follow the hint given
    posts.forEach(singlePost => {

        console.log(singlePost);

        //creates a div for each email for any of the views we are on
        
        const newPost = document.createElement('div');
        newPost.className="list-group-item";
        newPost.innerHTML =`
            <h5>Body: ${singlePost.body}</h5>
            <h5>Likes: ${singlePost.likes}</h5>
            <p>${singlePost.timestamp}</p>
            
        `;

        const posterProfile = document.createElement("a");
        posterProfile.setAttribute("href", `view_profile/${singlePost.poster}`);
        posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`
        newPost.prepend(posterProfile);

        document.querySelector('#posts-view').append(newPost);

        editButton = document.createElement("button");
        editButton.innerHTML =`Edit`;
        if( currentusername == `${singlePost.poster}` )
            newPost.append(editButton);
        })
    
});
}

