let movie = document.getElementsByTagName('h1')[0].innerHTML = "Covil de Ladrões"

let summaryMovie = document.getElementsByClassName('paragraph')

let mainInformations = document.getElementById('subtitle').innerHTML = "Principais informações."

for (let index = 0; index < summaryMovie.length; index++) {
    summaryMovie[0].innerHTML = "Este filme é muito dinamico e envolvente com um final surpreendente"
    summaryMovie[0].style.fontStyle = 'italic'
    summaryMovie[1].innerHTML = "Filme produzido por Carlos, elenco: Scalambrines e souzas"    
}

let changeColor = document.getElementsByTagName('h2')

for (let index = 0; index < changeColor.length; index++) {
    changeColor[0].style.color = 'blue'
    
}