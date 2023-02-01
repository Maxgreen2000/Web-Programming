document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            load_projects()
        }
    })
    
});

function load_projects() {
    document.querySelector('#projects-view').style.display = 'block';
    document.querySelector('#add_project_button').style.display = 'block';
    projectsview = document.getElementById('projects-view')
    projectsview.innerHTML = ""
    document.querySelector('#add_project_button').innerHTML = ""

    //Add a button to start  new project
    const addProject = document.createElement('button');
    addProject.innerHTML = "Add Project"
    addProject.addEventListener('click', function() {
        document.querySelector('#add_project_button').style.display = 'none';
        add_project()
    })
    add_project_button = document.querySelector('#add_project_button')
    add_project_button.append(addProject)


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
                view_project(singleProject.id)
            });
            projectsview.append(projectResult)
        })
    })
}

function view_project(id) {
    projectview = document.getElementById('singleproject-view')
    document.getElementById('add_project_button').style.display = 'none';
    document.querySelector('#singleproject-view').innerHTML = "";
    document.querySelector('#projects-view').style.display = 'none';
    document.querySelector('#singleproject-view').style.display = 'block';

    //Add a link that goes back to search filters
    const returntoresults = document.createElement('button');
    returntoresults.innerHTML = "Back to projects"
    returntoresults.addEventListener('click', function() {
        document.querySelector('#singleproject-view').style.display = 'none';
        document.querySelector('#citations-view').style.display = 'none';
        document.querySelector('#projects-view').style.display = 'block';
        document.getElementById('add_project_button').style.display = 'block';
    })

    //Add a button that deletes the selected project
    const deleteproject = document.createElement('button');
    deleteproject.innerHTML = "Delete Project"
    deleteproject.addEventListener('click', function() {
        projectsview.innerHTML = ""
        fetch(`/delete_project/${id}`)
        returntoresults.click()
        location.reload();
    })


    fetch(`/project/${id}`)
    .then(response => response.json())
    .then(project => {
      projectview.innerHTML = `
        <ul class="list-group">
            <li class="list-group-item">ID: ${project.id}</li>
            <li class="list-group-item">TITLE: ${project.title}</li>
            <li class="list-group-item">AUTHOR: ${project.user}</li>
            <li class="list-group-item">YEAR: ${project.timestamp}</li>
        </ul>`
    projectview.prepend(deleteproject)
    projectview.prepend(returntoresults)
    })

    //LIST ALL CITATIONS WITH A LINK TO EACH
    citationsview = document.getElementById('citations-view')
    fetch(`/citations/${id}`)
    .then(response => response.json())
    .then(citations => {
        citations.forEach(singleProjectCitation => {
            const citationResult = document.createElement('div');
            citationResult.className="list-group-item";
            citationResult.innerHTML =`
            <span>${singleProjectCitation.article}</span>
              <span>${singleProjectCitation.user}</span>
              <span>${singleProjectCitation.article}</span>
              <span>${singleProjectCitation.pagefrom}</span>
              <span>${singleProjectCitation.pageto}</span>
            `;
            citationResult.addEventListener('click', function() {
                view_article(singleProjectCitation.article)
            });
            citationsview.append(citationResult)
        })
    })
}

function add_project() {
    document.getElementById('add_project_div').innerHTML = ""
    document.getElementById('add_project_div').style.display = 'block';
    const name_project = document.createElement('input');

    //Add a link that goes back to search filters
    const create_project = document.createElement('button');
    create_project.innerHTML = "Create Project"
    create_project.addEventListener('click', function() {
        document.querySelector('#add_project_button').style.display = 'block';
        document.querySelector('#add_project_div').style.display = 'none';
        title = name_project.value
        fetch('/create_project', {
            method: 'POST',
            body: JSON.stringify({
                title: title,
            })
        })
    })

    addprojectdiv = document.getElementById('add_project_div')
    addprojectdiv.append(name_project)
    addprojectdiv.append(create_project)
}

function view_article(id) {
    articleview = document.getElementById('article-view')
    document.querySelector('#article-view').innerHTML = "";
    document.querySelector('#add_project_div').style.display = 'none';
    document.querySelector('#projects-view').style.display = 'none';
    document.querySelector('#singleproject-view').style.display = 'none'
    document.querySelector('#citations-view').style.display = 'none';
    document.querySelector('#article-view').style.display = 'block'

    //Add a link that goes back to search filters
    const returntoresults = document.createElement('button');
    returntoresults.innerHTML = "Back to Project"
    returntoresults.addEventListener('click', function() {
        document.querySelector('#article-view').style.display = 'none';
        document.querySelector('#singleproject-view').style.display = 'block'
        document.querySelector('#citations-view').style.display = 'block';
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
    articleview.prepend(returntoresults)
    })

}