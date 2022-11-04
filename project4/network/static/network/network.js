document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#newpostform").addEventListener('submit', new_post);
    document.querySelector('#allpostsbutton').addEventListener('click', () => load_page('allposts'));

    // By default, load the inbox
    load_page('allposts');

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

function load_page(page) {
    document.querySelector('#allposts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#following-view').style.display = 'none';

    document.querySelector('#allposts-view').innerHTML = `<h3>${page.charAt(0).toUpperCase() + page.slice(1)}</h3>`;

  //Display all the emails for a particular user
  fetch(`/load/${page}`)
  .then(response => response.json())
  .then(posts => {
    // Print emails by looping through them all and follow the hint given
    posts.forEach(singlePost => {

      console.log(singlePost);

      //creates a div for each email for any of the views we are on
      const newPost = document.createElement('div');
      newPost.className="list-group-item";
      newPost.innerHTML =`
        <h6>Poster: ${singlePost.poster}</h6>
        <h5>Body: ${singlePost.body}</h5>
        <h5>Likes: ${singlePost.likes}</h5>
        <p>${singlePost.timestamp}</p>
      
      `;

      document.querySelector('#allposts-view').append(newPost);

    })

    
});
}