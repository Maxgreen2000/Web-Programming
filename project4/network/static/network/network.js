document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#newpostform").addEventListener('submit', new_post);
    document.querySelector('#allpostsbutton').addEventListener('click', () => load_posts('0','allposts'));
    document.querySelector('#profilebutton').addEventListener('click', () => load_posts('1','profile'));

    // By default, load the inbox
    indexpage('0', 'allposts');

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

function indexpage(userid, page) {

    document.querySelector('#posts-view').style.display = 'block';
    document.querySelector('#following-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#following-view').style.display = 'none';

    load_posts('0','allposts')

}



function load_posts(userid, page) {        //RENAME THIS TO LOAD POSTS , WE ARE NOT LOADING THE PAGES SIMPLY POSTING A SET AMOUNT OF POSTS TO YOUR SELECTED PAGE

    document.querySelector('#pageselected').innerHTML = `<h3>${page.charAt(0).toUpperCase() + page.slice(1)}</h3>`;
    document.querySelector('#posts-view').innerHTML = "";

  //Display all the posts for a particular user
  fetch(`/load/${userid}/${page}`)
  .then(response => response.json())
  .then(posts => {
    // Print emails by looping through them all and follow the hint given
    posts.forEach(singlePost => {

      console.log(singlePost);

      //creates a div for each email for any of the views we are on
      
      const newPost = document.createElement('div');
      newPost.className="list-group-item";
      newPost.innerHTML =`
        <a href="#" id="postername">Poster: ${singlePost.poster}</a>
        <h5>Body: ${singlePost.body}</h5>
        <h5>Likes: ${singlePost.likes}</h5>
        <p>${singlePost.timestamp}</p>    
      `;

      newPost.addEventListener('click', function() {
        alert(`${singlePost.poster}`);
      });

      document.querySelector('#posts-view').append(newPost);



    })
    
});
}

function view_profile(userid) {


    load_posts('profile')

}