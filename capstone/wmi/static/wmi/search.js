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
}



