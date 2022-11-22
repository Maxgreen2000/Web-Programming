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
        posterProfile.innerHTML = `<h5>Poster: ${singlePost.poster}</h5>`;
        posterProfile.id = "profile-link";
        newPost.prepend(posterProfile);

        document.querySelector('#posts-view').append(newPost);

        fetch("/userauthenicated")
        .then(response => response.json())
        .then(authenicated => {
            if(authenicated.authenticated == "True"){

                const buttondiv = document.createElement('div');
                buttondiv.id = 'buttondiv';

                //Make both divs and buttons then choose which is hidden
                const likediv = document.createElement('div');
                const unlikediv = document.createElement('div');
                likeButton = document.createElement("button"); 
                likeButton.setAttribute("class", "btn btn-outline-danger")
                likeButton.textContent = "Like";    
                likediv.style.display = "none";
                unlikeButton = document.createElement("button"); 
                unlikeButton.setAttribute("class", "btn btn-outline-danger")
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
                    likecountdiv.innerHTML =`<h5>Likes ${singlePost.likes}</h5>`;

                    
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
                    likecountdiv.innerHTML =`<h5>Likes ${singlePost.likes}</h5>`;
                })
                likediv.append(likeButton);
                unlikediv.append(unlikeButton);
                buttondiv.append(likediv);
                buttondiv.append(unlikediv);
                newPost.append(buttondiv);


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

                if (document.getElementById("currentusername")){

                    if( document.querySelector('#currentusername').innerHTML == `${singlePost.poster}` ){
                        editButtondiv = document.createElement("div");
                        
                        
                        const editButton = document.createElement("button");
                        editButton.setAttribute("class", "btn btn-outline-primary")
                        editButton.innerHTML ="Edit";
                        editButtondiv.append(editButton);
                        buttondiv.append(editButtondiv);
                        
                        editButton.addEventListener('click', function() {

                            var editform = document.createElement("form");
                            
                            var FN = document.createElement("textarea");
                            FN.value = `${singlePost.body}`
                            FN.setAttribute("class", "form-control")
                            FN.setAttribute("name", "body");
                            FN.setAttribute("placeholder", "Full Name");
                        
                            var s = document.createElement("button");
                            s.setAttribute("class", "btn btn-outline-primary");
                            s.innerHTML = "Save Edit";

                            const editformelement = document.getElementById('editform_id');
                            if (!(editformelement)){
                                editform.appendChild(FN);
                                buttondiv.innerhtml = "";
                                buttondiv.append(s);
                                bodydiv.innerHTML="";
                                bodydiv.append( editform );
                                editform.id = 'editform_id'
                            }

                            
                            if (!(editformelement)) {
                                editButton.style.display = "none";
                            }

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
                                bodydiv.innerHTML="";
                                singlePost.body = FN.value;
                                bodydiv.innerHTML = `<h5>Body: ${singlePost.body}</h5>`
                                editButton.style.display = "block";
                                s.style.display = "none";


                            })
                        
                        });

                        
                    }

                }




            }
        })
    })
    
    
});
}



