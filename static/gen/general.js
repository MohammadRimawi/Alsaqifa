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


  function append_to_class(className,item){
      elm = document.createElement('div');
      elm.innerHTML = item;
      document.getElementsByClassName(className)[0].append(elm);
  }



  function prepend_to_class(className,item){
    elm = document.createElement('div');
    elm.innerHTML = item;
    document.getElementsByClassName(className)[0].prepend(elm);
}


function ckeditor_init(className,type){
    const post_wd = new CKSource.Watchdog();
    // const comment_wd = new CKSource.Watchdog();
    post_wd.setCreator( ( element, config ) => {
        return CKSource.Editor
            .create( element, config )
            .then( editor => {

                return editor;

            } )
    } );
    
    post_wd.setDestructor( editor => {

        return editor.destroy();
    } );
    
    post_wd.on( 'error', handleError );
    if (type == "full"){
        post_wd
        .create( document.querySelector( className ), {
            
            toolbar: {
                items: [
                    'fontFamily',
                    '|',
                    'fontColor',
                    'fontSize',
                    'fontBackgroundColor',
                    'heading',
                    '|',
                    'underline',
                    'bold',
                    'italic',
                    'alignment',
                    'indent',
                    'outdent',
                    'bulletedList',
                    'blockQuote',
                    '|',
                    'CKFinder',
                    'link',
                    'imageUpload',
                    'imageInsert',
                    'mediaEmbed',
                    '|',
                    'undo',
                    'redo',
                    '|',
                    'todoList',
                    '|',
                    'strikethrough',
                    'subscript',
                    'superscript',
                    'removeFormat',
                    'highlight',
                    'horizontalLine',
                    'htmlEmbed',
                    'insertTable'
                ],
                // shouldNotGroupWhenFull: true
            },
            language: 'ar',
            image: {
                styles: [
                    'alignLeft', 'alignCenter', 'alignRight'
                ],
                toolbar: [
                    'imageTextAlternative',
                    // 'imageStyle:full',
                    // 'imageStyle:side',
                    'imageStyle:alignRight',
                    'imageStyle:alignCenter',
                    'imageStyle:alignLeft',
                    
                    'linkImage'
                ]
                
            },
            table: {
                contentToolbar: [
                    'tableColumn',
                    'tableRow',
                    'mergeTableCells',
                    'tableCellProperties',
                    'tableProperties'
                ]
            },
            licenseKey: '',
            
            
        } ).then(editor => {
            window.editor = editor;
            
            handleStatusChanges( editor );
            handleSaveButton( editor );
            handleBeforeunload( editor );
        } )
        .catch( handleError );


        b = `<div class='editor-bottom-toolbar'>
        <button onclick='location.reload()'>تراجع</button>
        <button>تعديل</button>

        
        </div>`
        append_to_class("post-text",b)


    }
    else{
        post_wd
        .create( document.querySelector( className ), {
            
            toolbar: {
                items: [
                    'underline',
                    'bold',
                    'italic',
                    'strikethrough',
                    'removeFormat',
                    
                ]
            },
            language: 'ar',
       
            licenseKey: '',
            
            
        } )
        .catch(  );
    
    function handleError( error ) {
        console.error( 'Oops, something went wrong!' );
        console.error( 'Please, report the following error on https://github.com/ckeditor/ckeditor5/issues with the build id and the error stack trace:' );
        console.warn( 'Build id: 542cmi8mt16g-dexkzk5cw1y2' );
        console.error( error );
    }
    }
        
        

    

}