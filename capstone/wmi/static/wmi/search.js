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
    document.querySelector('#manuscript-view').style.display = 'none';

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
    const location = document.querySelector('#inputLocation').value;
    const tags = document.querySelector('#inputTags').value;
    const keywords = document.querySelector('#inputKeywords').value;
    const yearfrom = document.querySelector('#inputYearFrom').value;
    const yearto = document.querySelector('#inputYearTo').value;

    fetch('/searchresult', {
        method: 'POST',
        body: JSON.stringify({
            title: title,
            location: location,
            tags: tags,
            keywords: keywords,
            yearfrom: yearfrom,
            yearto: yearto
        })
    })
    .then(response => response.json())
    .then(manuscripts => {
        manuscripts.forEach(singleManuscript => {
            const manuscriptResult = document.createElement('div');
            manuscriptResult.className="list-group-item";
            manuscriptResult.innerHTML =`
              <span>${singleManuscript.title},</span>
              <span>${singleManuscript.location},</span>
              <span>${singleManuscript.yearfrom} - ${singleManuscript.yearto}</span>
            `;
            manuscriptResult.addEventListener('click', function() {
                document.location = `/manuscript/${singleManuscript.id}`;
            });
            resultsview.append(manuscriptResult)
        })
    })
}



