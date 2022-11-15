document.addEventListener('DOMContentLoaded', function(e) {

    userid = document.querySelector('#profile-userid').innerHTML
    load_posts(userid, 'profile')

    //document.querySelector('#follow_button').addEventListener('click', () => addFollow(userid));
  
    var element = document.querySelector("#follow_button");

    if (element)
    element.addEventListener('click', () => addFollow(userid));

    e.preventDefault();

});
document.querySelector('#posts-view').innerHTML = "";


function load_posts(userid, page,) { 

    document.querySelector('#posts-view').innerHTML = "";
    pagenumber = document.getElementById("page-number").innerHTML;

    //Display all the posts for a particular user
    fetch(`/loadposts/${userid}/${page}`)
    .then(response => response.json())
    .then(posts => {
        // Print emails by looping through them all and follow the hint given
        count = posts.length;
        document.getElementById("counterposts").innerHTML = `Total: ${count}`;
        slicedposts = posts.slice((pagenumber-1)*5,pagenumber*5)
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
            posterProfile.setAttribute("href", "");
            posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`
            newPost.prepend(posterProfile);

            fetch(`/determinebutton/${singlePost.id}`)
            .then(response => response.json())
            .then(buttontext => {
                likeButton = document.createElement("button"); 
                likeButton.innerHTML =`${buttontext.text}`;  
                likeButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    
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
                editButton.setAttribute("type", "button");
                editButton.innerHTML =`Edit`;   
                if( document.querySelector('#currentusername').innerHTML == `${singlePost.poster}` ){
                    
                        editButton.addEventListener('click', function(e) {
                            e.preventDefault();

                            var editform = document.createElement("form");
                            editform.setAttribute("method", "post");
                            
                        
                            var FN = document.createElement("input");
                            FN.value = `${singlePost.body}`
                            FN.setAttribute("type", "textarea");
                            FN.setAttribute("name", "body");
                            
                        
                            var s = document.createElement("input");
                            s.setAttribute("type", "button");

                            s.addEventListener('click', function(e) {
                                e.preventDefault();
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