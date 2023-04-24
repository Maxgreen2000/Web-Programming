document.addEventListener('DOMContentLoaded', function() {

    fetch("/userauthenicated")
    .then(response => response.json())
    .then(authenicated => {
        if(authenicated.authenticated == "True"){
            load_mymanuscripts()
        }
    })
});

function load_mymanuscripts() {
    document.querySelector('#my-manuscripts-view').style.display = 'block';
    mymanuscripts = document.getElementById('my-manuscripts-view')

    fetch('/mymanuscriptresults')
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
                view_manuscript(singleManuscript.id)
            });
            mymanuscripts.append(manuscriptResult)
        })
    })
}

function view_manuscript(id) {
    manuscriptview = document.getElementById('manuscript-view')
    document.querySelector('#manuscript-view').innerHTML = "";
    document.querySelector('#my-manuscripts-view').style.display = 'none';
    document.querySelector('#manuscript-view').style.display = 'block'

    //Add a link that goes back to search filters
    const returntoresults = document.createElement('button');
    returntoresults.innerHTML = "Back to Manuscripts"
    returntoresults.addEventListener('click', function() {
        document.querySelector('#manuscript-view').style.display = 'none';
        document.querySelector('#my-manuscripts-view').style.display = 'block';
    })

    fetch(`/manuscript/${id}`)
    .then(response => response.json())
    .then(manuscript => {
      manuscriptview.innerHTML = `
        <ul class="list-group">
            <li class="list-group-item">id: ${manuscript.poster}</li>
            <li class="list-group-item">id: ${manuscript.id}</li>
            <li class="list-group-item">title: ${manuscript.title}</li>
            <li class="list-group-item">location: ${manuscript.location}</li>
            <li class="list-group-item">Date Range: ${manuscript.yearfrom} - ${manuscript.yearto}</li>
            <li class="list-group-item">tags: ${manuscript.tags}</li>
            <li class="list-group-item"><p>Transcript: ${manuscript.transcript}</p></li>
        </ul>`
    manuscriptview.prepend(returntoresults)
    })

}


