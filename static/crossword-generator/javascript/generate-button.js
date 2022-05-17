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


function printCrossword(){

    const crossword_original = document.getElementById("crossword");
    const prompts_original = document.getElementById("wordlist");
    const solutions_original = document.getElementById("crossword_solution");
    var crossword = crossword_original.cloneNode(true);
    var prompts = prompts_original.cloneNode(true);
    var solutions = solutions_original.cloneNode(true);
    var solutions_p = solutions.getElementsByTagName("p")[0];
    solutions_p.style.transform="rotate(180deg)";

    //set attribute to absolute, dunno why but otherwise the styling gets messed up
    var inputs = crossword.getElementsByTagName("input");
    console.log(inputs)
    for(i=0; i<inputs.length; i++){
        inputs[i].style.position = "absolute";
    }

    //
    crossword.style.width="100%";
    crossword.style.width="100%";
    var spanContainers = crossword.getElementsByTagName("span");
    for (i=0; i<spanContainers.length; i++){
        spanContainers[i].style.display = "inline-block";
        spanContainers[i].style.width = "50px";
        spanContainers[i].style.height = "50px";
    }

    // make bigger numbers
    var indexNumber = crossword.getElementsByClassName("index_number");
    for(i=0; i<indexNumber.length; i++){
        indexNumber[i].style.fontSize = "larger";
    }

    // remove the check solution button
    var inputButton = crossword.getElementsByClassName("submitButton");
    inputButton[0].remove();

    // remove the hint button
    var hintButton = prompts.getElementsByClassName("hint_button");
    const len = hintButton.length;
    for(i=0; i<len; i++){
        hintButton[0].remove();
    }

    var promptlist = prompts.getElementsByTagName("ol")[0];
    promptlist.style.fontSize = "larger";

    var printwin = window.open("");
    printwin.document.write(crossword.innerHTML);
    printwin.document.write(prompts.innerHTML);
    printwin.document.write(solutions.innerHTML);
    printwin.print();

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
