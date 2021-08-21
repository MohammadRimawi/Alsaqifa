function validate_widget(){
    var valid = true;

    var table = document.getElementsByClassName('select-table')[0];

    if(table.classList.contains('post-selected')){
        post_id = document.querySelector('select[name=post_id]').value;
        return post_id*1!=0?true:false;
    }

    else if(table.classList.contains('slider-selected')){
        number_of_cards = document.querySelector('input[name=number_of_cards]').value*1;
        tag_id = document.querySelector('select[name=tag_id]').value*1;

        if(tag_id <= 0 || number_of_cards <= 0){
            return false;
        }
        else{
            return true;
        }

    }
    else if(table.classList.contains('embeded-selected')){
        code_block = document.querySelector('textarea[name=code_block]').value;

        if(code_block.trim() != ""){
            return true;
        }
        else{
            return false;
        }
    }
    else{
        return false;
    }
}
