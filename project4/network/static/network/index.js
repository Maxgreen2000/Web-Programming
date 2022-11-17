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

  //Display all the posts for a particular user
  fetch(`/loadposts/${userid}/${page}`)
  .then(response => response.json())
  .then(posts => {

    paginateby = 10;
    pagenumber = document.getElementById('pagenumber').innerHTML;

    slicedposts = posts.slice(((pagenumber-1) * paginateby), (pagenumber * paginateby));
    // Print emails by looping through them all and follow the hint given
    slicedposts.forEach(singlePost => {

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

        fetch(`/determinebutton/${singlePost.id}`)
        .then(response => response.json())
        .then(buttontext => {
            likeButton = document.createElement("button"); 
            likeButton.innerHTML =`${buttontext.text}`;  
            likeButton.addEventListener('click', function() {
                
                fetch(`/likeposts/${singlePost.id}`)
                .then(response => response.json())
                .then(result => {
                    // Print result
                    (load_posts(userid, page))
                    console.log(result)
                })
                
            })
            newPost.append(likeButton);
        })


        document.querySelector('#posts-view').append(newPost);
        if (document.getElementById("currentusername")){
            editButton = document.createElement("button");
            editButton.innerHTML =`Edit`;   
            if( document.querySelector('#currentusername').innerHTML == `${singlePost.poster}` ){
                
                    editButton.addEventListener('click', function() {

                        var editform = document.createElement("form");
                        editform.setAttribute("method", "post");
                        
                    
                        var FN = document.createElement("input");
                        FN.value = `${singlePost.body}`
                        FN.setAttribute("type", "textarea");
                        FN.setAttribute("name", "body");
                        FN.setAttribute("placeholder", "Full Name");
                    
                        var s = document.createElement("input");
                        s.setAttribute("type", "submit");
                        s.setAttribute("value", "Submit");

                        s.addEventListener('click', function() {
                            fetch(`/editposts/${singlePost.id}`,{
                                method: 'POST',
                                body: JSON.stringify({
                                    body: FN.value, 
                                })
                            })  
                            .then(response => response.json())
                            .then(result => {
                                console.log(result);
                            }) 
                            
                        })
                        const editformelement = document.getElementById('editform_id');
                        if (!(editformelement)){
                            editform.appendChild(FN);
                            editform.appendChild(s);
                            newPost.appendChild( editform );
                            editform.id = 'editform_id' ;
                        }
                    
                    });
                
                newPost.append(editButton);
            }

        }
    })
    
    
});
}



