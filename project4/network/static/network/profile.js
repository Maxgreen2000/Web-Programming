document.addEventListener('DOMContentLoaded', function() {

    userid = document.querySelector('#profile-userid').innerHTML
    load_posts(userid, 'profile')

    document.querySelector('#follow_button').addEventListener('click', () => addFollow(userid));

});



function load_posts(userid, page) {    

    document.querySelector('#posts-view').innerHTML = "";

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
      posterProfile.setAttribute("href", "");
      posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`
      newPost.prepend(posterProfile);

      document.querySelector('#posts-view').append(newPost);

    })
    
});
}

function addFollow(userid){
    fetch(`/addFollow/${userid}`)
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }) .then(() => {
        window.location.reload();      //This reloads the page thus clearing out the new post box , brings the new post up to the top as well as anyone elses.
    })
}