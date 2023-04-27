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
                document.location = `/manuscript/${singleManuscript.id}`;
            });
            mymanuscripts.append(manuscriptResult)
        })
    })
}



