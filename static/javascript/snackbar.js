
snacks = []

function changeDefOver(ev) {
    const snack = ev.currentTarget;
    console.log(snack)
    timer = snack.getAttribute('data-timer');
    clearTimeout(timer)
    // console.log("over")
    
}

function changeDefOut(ev) {
    const snack = ev.currentTarget;
    id = snack.getAttribute('data-id');

    timer = setTimeout("remove_snackbar(snacks["+ (id) +"])",5000);
    snacks[id].setAttribute("data-timer",timer);

    console.log("out")

}


function load_snackbar(){
    
    let snackbar = document.querySelector('.snackbar');


}

function remove_snackbar(elm,trigger=null){

    // console.log(elm)
    if (trigger == "button"){
        elm = elm.parentElement.parentElement.parentElement.parentElement;
     
 
    }
    else if(trigger == "function"){
        console.log(elm)

        elm = document.querySelectorAll("[data-timer='"+elm+"']")[0];
        console.log(elm)
    }
    
    elm.removeEventListener('mouseover', changeDefOver);
    elm.removeEventListener('mouseout', changeDefOut);
    elm.getElementsByClassName('snackbar')[0].classList.remove('show')
    
    x = setTimeout(()=>{
    elm.remove();
    snackbar = document.querySelectorAll('.snackbar');
    console.log(elm)
    },1000);
}

function add_snackbar(content,type,actions= null){
    
    
    if ( type != null && !(typeof type === 'string' || type instanceof String)){
        if(type >= 400){
            type = "warning";
        }
        else{
            type="ok"
        }

    }
    snacks.push(document.createElement('div'));
    snacks[snacks.length-1].classList.add('flex-row');

    snacks[snacks.length-1].innerHTML = `
   
        <div class="snackbar show  `+type+` ">
        <div class = "flex-column">
            <div class="flex-row snackbar-toolbar flex-h-end">
            <button onclick="remove_snackbar(this,'button')">x</button>
            </div>
            <div class="flex-row snackbar-body">
            `
            +content+
            `
            </div>
            `
             +(actions!=null ? 
            `
            <div class="flex-row snackbar-actions">
                <button>yes</button>
                <button>no</button>
            </div>

            `
             : "")+
             `
            </div>
        </div>
 
  `;

    timer = setTimeout("remove_snackbar(snacks["+ (snacks.length-1) +"])",5000);

    snacks[snacks.length-1].setAttribute("data-timer",timer);
    snacks[snacks.length-1].setAttribute("data-id",snacks.length-1);

    snacks[snacks.length-1].addEventListener('mouseover', changeDefOver);
    snacks[snacks.length-1].addEventListener('mouseout', changeDefOut);
    
    
    document.getElementsByClassName('snackbar-container')[0].append(snacks[snacks.length-1]);

    s = setTimeout("snacks[snacks.length-1].getElementsByClassName('snackbar')[0].classList.add('show')",3000);

    return timer
}