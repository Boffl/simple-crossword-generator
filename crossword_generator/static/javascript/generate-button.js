function getHints(word){

    const hint_id = 'hint_display_for_' + word;
    const button_id = 'hint_button_for_' + word;
    console.log(hint_id);
    const display = document.getElementById(hint_id);
    const button = document.getElementById(button_id);
    button.remove()
    display.hidden = false;

}



function CWFunction() {
  document.getElementById("crossword_grid").innerHTML = "CROSSWORD <br> :)";
}