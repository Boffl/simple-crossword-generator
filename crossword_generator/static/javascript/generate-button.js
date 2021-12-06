function getHints(word){
    // delete the hint button and display the hint
    const hint_id = 'hint_display_for_' + word;
    const button_id = 'hint_button_for_' + word;
    console.log(hint_id);
    const display = document.getElementById(hint_id);
    const button = document.getElementById(button_id);
    button.remove()
    display.hidden = false;

}

function showSolution(){
    console.log('show solutions')
    const solution = document.getElementById("crossword_solution")
    console.log(solution)
    var solution_button = document.getElementById("solution_button")
    if (solution.hidden === true){
        solution_button.textContent = "Hide Solution"
        solution.hidden = false
    }else{
        solution_button.textContent = "Show Solution"
        solution.hidden = true

    }

}



function CWFunction() {
  document.getElementById("crossword_grid").innerHTML = "CROSSWORD <br> :)";
}