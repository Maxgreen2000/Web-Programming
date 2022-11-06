document.addEventListener('DOMContentLoaded', function() {

    document.querySelector("#newpostform").addEventListener('submit', new_post);
    document.querySelector('#allpostsbutton').addEventListener('click', () => load_posts('0','allposts'));
    document.querySelector('#profilebutton').addEventListener('click', () => view_profile('0','currentuserprofile')); // THE NUMBER 1 HAS TO BE REPLACED WITH THE USER ID OF THE CURRENT USER.

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
      posterProfile.setAttribute("href", "#");
      posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`
      newPost.prepend(posterProfile);

      document.querySelector('#posts-view').append(newPost);

      posterProfile.addEventListener('click', function() {
        view_profile(singlePost.id)
      });


    })
    
});
}

function view_profile(id) {

  document.querySelector('#posts-view').style.display = 'block';
  document.querySelector('#following-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'block';
  document.querySelector('#newpostbar').style.display = 'none';

  fetch(`/loadprofile/${id}`)
  .then(response => response.json())
  .then(selectedProfile => {
    const profileinfo = document.createElement('div');
    profileinfo.className="list-group-item";
    profileinfo.innerHTML =`
      <h5>id: ${selectedProfile.id}</h5>
      <h5>User: ${selectedProfile.profile_owner}</h5>
      <h5>Bio: ${selectedProfile.bio}</h5>
    `;
  
  document.querySelector('#profile-view').append(profileinfo);
  
  });

  fetch(`/followbtn/${id}`)
  .then(response => response.json())
  .then(followbuttoncontents => {
    const followbutton = document.createElement('button');
    followbutton.innerHTML = `${followbuttoncontents.value}`;
    document.querySelector('#profile-view').append(followbutton);
  

  });



  load_posts(id,'profile')

}



//THE NEXT THING IS TO MAKE A BOOL IN VIEWS TO SEE IF THE CURRENT USER IS FOLLOWING THE VIEWED USER