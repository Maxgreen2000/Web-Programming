document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#change-page').addEventListener('click', change_page);
    document.querySelector('#change-page_2').addEventListener('click', change_page_2);

    index();
});

function change_page() {
    document.querySelector('#test-div-1').style.display = 'none';
    document.querySelector('#test-div-2').style.display = 'block';
}

function change_page_2() {
    document.querySelector('#test-div-1').style.display = 'block';
    document.querySelector('#test-div-2').style.display = 'none';
}