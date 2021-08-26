
function exit_modal(){
//Since there will not be more than 1 modal at any given time, we can remove all .modal divs
    modals = document.getElementsByClassName("modal");
    for(i = 0;i < modals.length;i++){
        modals[i].remove();
    }
    document.body.classList.remove('modal-visiable');
}   