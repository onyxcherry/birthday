const arrowAnim = document.getElementById('arrowAnim')

arrowAnim.addEventListener('click', () => {
    document.cookie = "ilovecats=undefined";
    console.log("Legenda głosi, że Płonący Lis ma lepsze wsparcie...")
    window.location.reload()
})