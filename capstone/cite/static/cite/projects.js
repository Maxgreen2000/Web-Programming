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
    projectsview = document.getElementById('projects-view')

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
    document.querySelector('#singleproject-view').innerHTML = "";
    document.querySelector('#projects-view').style.display = 'none';
    document.querySelector('#singleproject-view').style.display = 'block';

    //Add a link that goes back to search filters
    const returntoresults = document.createElement('button');
    returntoresults.innerHTML = "Back to projects"
    returntoresults.addEventListener('click', function() {
        document.querySelector('#singleproject-view').style.display = 'none';
        document.querySelector('#projects-view').style.display = 'block';
    })


    fetch(`/project/${id}`)
    .then(response => response.json())
    .then(project => {
      projectview.innerHTML = `
        <ul class="list-group">
            <li class="list-group-item">ID: ${project.id}</li>
            <li class="list-group-item">TITLE: ${project.title}</li>
            <li class="list-group-item">AUTHOR: ${project.user}</li>
            <li class="list-group-item">PUBLISHER: ${project.citations}</li>
            <li class="list-group-item">YEAR: ${project.timestamp}</li>
        </ul>`
    projectview.prepend(returntoresults)
    })
}