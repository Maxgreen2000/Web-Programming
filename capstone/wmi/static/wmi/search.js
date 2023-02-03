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
              <span>${singleManuscript.title}</span>
              <span>${singleManuscript.location}</span>
              <span>${singleManuscript.year}</span>
            `;
            manuscriptResult.addEventListener('click', function() {
                view_manuscript(singleManuscript.id)
            });
            resultsview.append(manuscriptResult)
        })
    })
}

function view_manuscript(id) {
    articleview = document.getElementById('manuscript-view')
    document.querySelector('#manuscript-view').innerHTML = "";
    document.querySelector('#searchform').style.display = 'none';
    document.querySelector('#results-view').style.display = 'none';
    document.querySelector('#manuscript-view').style.display = 'block'

    //Add a link that goes back to search filters
    const returntoresults = document.createElement('button');
    returntoresults.innerHTML = "Back to results"
    returntoresults.addEventListener('click', function() {
        document.querySelector('#manuscript-view').style.display = 'none';
        document.querySelector('#results-view').style.display = 'block';
    })

    fetch(`/article/${id}`)
    .then(response => response.json())
    .then(article => {
      articleview.innerHTML = `
        <ul class="list-group">
            <li class="list-group-item">ID: ${article.id}</li>
            <li class="list-group-item">TITLE: ${article.title}</li>
            <li class="list-group-item">AUTHOR: ${article.author}</li>
            <li class="list-group-item">PUBLISHER: ${article.publisher}</li>
            <li class="list-group-item">YEAR: ${article.year}</li>
            <li class="list-group-item"><p>Content: ${article.content}</p></li>
        </ul>`
    articleview.prepend(selectproject)
    articleview.prepend(returntoresults)
    })

}

function load_projects(article_id) {
    document.querySelector('#projects-view').style.display = 'block';
    projectsview = document.getElementById('projects-view')
    projectsview.innerHTML = "<h1>Select Project To Add Citation<h1>"
    fetch('/loadprojects')
    .then(response => response.json())
    .then(projects => {
        projects.forEach(singleProject => {
            const projectResult = document.createElement('div');
            projectResult.className="list-group-item";
            projectResult.innerHTML =`
            <span>${singleProject.title}</span>
            <span>${singleProject.user}</span>
            `;
            projectResult.addEventListener('click', function() {
                add_citation(article_id, singleProject.id)
            });
            projectsview.append(projectResult)
        })
    })
}

function add_citation(article_id, project_id) {
    fetch(`/add_citation/${article_id}/${project_id}`)
    document.querySelector('#searchform').style.display = 'none';
    document.querySelector('#manuscript-view').style.display = 'block';
    document.querySelector('#projects-view').style.display = 'none';
}