document.addEventListener('DOMContentLoaded', function() {


    // By default, load the inbox
    load_posts('0', 'following')

});

function load_posts(userid, page) {        //RENAME THIS TO LOAD POSTS , WE ARE NOT LOADING THE PAGES SIMPLY POSTING A SET AMOUNT OF POSTS TO YOUR SELECTED PAGE
    document.querySelector('#pageselected').innerHTML = `<h3>${page.charAt(0).toUpperCase() + page.slice(1)}</h3>`;
    document.querySelector('#posts-view').innerHTML = "";

  //Display all the posts for a particular user
  fetch(`/loadposts/${userid}/${page}`)
  .then(response => response.json())
  .then(posts => {
    // Print emails by looping through them all and follow the hint given
    paginateby = 10;
    pagenumber = document.getElementById('pagenumber').innerHTML;

    slicedposts = posts.slice(((pagenumber-1) * paginateby), (pagenumber * paginateby));

    slicedposts.forEach(singlePost => {

        console.log(singlePost);

        //creates a div for each email for any of the views we are on
        
        const newPost = document.createElement('div');
        newPost.className="list-group-item";
        newPost.innerHTML =`
            <p>${singlePost.timestamp}</p>
            
        `;

        const likecountdiv = document.createElement('div');
        likecountdiv.innerHTML = `<h5>Likes: ${singlePost.likes}</h5>`;
        newPost.prepend(likecountdiv);

        const bodydiv = document.createElement('div');
        bodydiv.innerHTML = `<h5>Body: ${singlePost.body}</h5>`
        newPost.prepend(bodydiv);

        const posterProfile = document.createElement("a");
        posterProfile.setAttribute("href", `view_profile/${singlePost.poster}`);
        posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`
        newPost.prepend(posterProfile);

        document.querySelector('#posts-view').append(newPost);

        //Make both divs and buttons then choose which is hidden
        const likediv = document.createElement('div');
        const unlikediv = document.createElement('div');
        likeButton = document.createElement("button"); 
        likeButton.textContent = "Like";    
        likediv.style.display = "none";
        unlikeButton = document.createElement("button"); 
        unlikeButton.textContent = "Unlike"; 
        unlikediv.style.display = "none";

        likeButton.addEventListener('click', function() {
            likediv.style.display = "none";
            unlikediv.style.display = "block";
            fetch(`/likeposts/${singlePost.id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
            })
            singlePost.likes = singlePost.likes + 1;
            likecountdiv.innerHTML = "";
            likecountdiv.innerHTML =`<h5>Likes: ${singlePost.likes}</h5>`;
        })

        unlikeButton.addEventListener('click', function() {
            likediv.style.display = "block";
            unlikediv.style.display = "none";
            fetch(`/likeposts/${singlePost.id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
            })
            singlePost.likes = singlePost.likes - 1;
            likecountdiv.innerHTML = "";
            likecountdiv.innerHTML =`<h5>Likes: ${singlePost.likes}</h5>`;
        })
        likediv.append(likeButton);
        unlikediv.append(unlikeButton);
        newPost.append(likediv);
        newPost.append(unlikediv);



        fetch(`/determinebutton/${singlePost.id}`)
        .then(response => response.json())
        .then(buttontext => {
            if(`${buttontext.text}` == "Like" ){
                likediv.style.display = "block";
            }
            if(`${buttontext.text}` == "Unlike" ){
                unlikediv.style.display = "block";
            }
        })



    })
    
});
}