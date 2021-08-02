last_x = 0;
document.addEventListener("scroll", myFunction);

function myFunction() {
    var x = document.documentElement.scrollTop;
    // console.log(x)
    setTimeout(100);
    if(x!=last_x){
        
        console.log("in");
        if(x>last_x){
            if(Math.abs(x-last_x)>20)
            document.getElementById("nav_menu").classList.remove("sticky_show");
        }
        else{
            document.getElementById("nav_menu").classList.add("sticky_show");
        }
        last_x=x;
   }
}

function toggle_nav(){
    var header = document.getElementById("nav_menu");
    if (header.classList.contains("expand")){
        header.classList.remove("expand");
    }
    else{
        header.classList.add("expand");
    }

//     items = header.getElementsByTagName("li");
//     var i=0;
//   timer = setInterval(() => {
//       i-=4;
//      items[0].style.left=i+'px';

//      if( i <-1000) clearInterval(timer)
//   }, 10 );
}

function openNav() {

    if(document.getElementById("mySidenav").style.width==""||document.getElementById("mySidenav").style.width == "0px"){
        document.getElementById("side_nav_back").style.width = document.body.offsetWidth+10+"px";
        document.getElementById("mySidenav").style.width = "250px";
    }else{

        document.getElementById("side_nav_back").style.width = "0px";
        document.getElementById("mySidenav").style.width = "0";
        
    }
  }
  


  function toggle_class(selector,item,elm = null){

    if (elm != null){
        elm.parentNode.getElementsByClassName(selector)[0].classList.toggle(item);
    }
    else{
        document.getElementsByClassName(selector)[0].classList.toggle(item);
    }
    //   if(selector[0]=='.'){
    //   }
    //   else if (selector.)

  }