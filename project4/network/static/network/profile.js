document.addEventListener('DOMContentLoaded', function() {

    userid = document.querySelector('#profile-userid').innerHTML
    load_posts(userid, 'profile')

    //document.querySelector('#follow_button').addEventListener('click', () => addFollow(userid));
  
    var element = document.querySelector("#follow_button");

    if (element)
    element.addEventListener('click', () => addFollow(userid));

});
document.querySelector('#posts-view').innerHTML = "";


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

        fetch(`/determinebutton/${singlePost.id}`)
        .then(response => response.json())
        .then(buttontext => {
            likeButton = document.createElement("button"); 
            likeButton.innerHTML =`${buttontext.text}`;  
            likeButton.addEventListener('click', function() {
                fetch(`/likeposts/${singlePost.id}`)
                likeButton.value = "hello"                   //LIKING WORKS BUT CANT GET THE INNERHTML OF THE BUTTON TO CHANGE
            })
            newPost.append(likeButton);
        })




        
       // likeButton = document.createElement("button"); 
        //likeButton.innerHTML ="Like";           //NEED TO FIND WHAT THE INNERHTML SHOULD BE???
        //likeButton.addEventListener('click', function() {
            //fetch(`/likeposts/${singlePost.id}`)
            //likeButton.innerHTML = "Unlike";

        //})
        //newPost.append(likeButton);
        

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
                            editform.id = 'editform_id';
                        }
                    
                    });
                
                newPost.append(editButton);
            }

        }




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