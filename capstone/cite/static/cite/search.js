document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            document.getElementById('searchbutton').addEventListener('click', function() {
                searchform()
            })
        }
    })
    

});

function searchform() {
    document.querySelector('#results-view').innerHTML = "";
    document.querySelector('#searchform').style.display = 'none';
    document.querySelector('#results-view').style.display = 'block';



    //Add a link that goes back to search filters
    const returntofilters = document.createElement('button');
    returntofilters.innerHTML = "Back to search filters"
    returntofilters.addEventListener('click', function() {
        document.querySelector('#searchform').style.display = 'block';
        document.querySelector('#results-view').style.display = 'none';
    })
    resultsview = document.getElementById('results-view')
    resultsview.append(returntofilters)



    const title = document.querySelector('#inputTitle').value;
    const author = document.querySelector('#inputAuthor').value;
    const publisher = document.querySelector('#inputPublisher').value;
    const yearfrom = document.querySelector('#inputYearFrom').value;
    const yearto = document.querySelector('#inputYearTo').value;

    fetch('/searchresult', {
        method: 'POST',
        body: JSON.stringify({
            title: title,
            author: author,
            publisher: publisher,
            yearfrom: yearfrom,
            yearto: yearto
        })
    })
    .then(response => response.json())
    .then(articles => {
        articles.forEach(singleArticle => {
            const articleResult = document.createElement('div');
            articleResult.className="list-group-item";
            articleResult.innerHTML =`
              <span>${singleArticle.title}</span>
              <span>${singleArticle.author}</span>
              <span>${singleArticle.year}</span>
            `;
            resultsview.append(articleResult)
            console.log(singleArticle);
        })
    })
}
   