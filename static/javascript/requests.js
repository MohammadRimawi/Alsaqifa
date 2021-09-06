// const

var host = window.location.host


function is_logged_in(mute = false){
    try {
        if (USER_TOKEN){
            console.log('pass')
        }

        
    }
    catch{
        if (!mute) add_snackbar('عليك بالتسجيل لاستخدام هذه المييزة!');        
        return false;
    }

    return true;
}

const sendHttpRequest = (method,url,data,header=true) => {
    const promise = new Promise( (resolve,reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method,url);


        if (header){
            xhr.setRequestHeader("Content-Type", "application/json");
        }

        xhr.onload = () => {
            if(xhr.status >= 400){
                reject(xhr.response);
            }
            else{
                resolve(xhr.response);
            }
        };
        // console.log(data)
        if(data instanceof FormData){
            xhr.send(data);
        }
        else{
            xhr.send(JSON.stringify(data));
        }

    });

    return promise;

};

function like_post_toggle(post_id,elm){

    if (!is_logged_in()) return;

    console.log("started",USER_TOKEN)
    add_snackbar('pending');
    // add_snackbar(host)
    const res = sendHttpRequest("POST","http://"+host+"/like_post",{
        user_id : USER_ID,
        token : USER_TOKEN,
        post_id : post_id
    }).then(responseData => {
        console.log(responseData)
        let res = JSON.parse(responseData)
        add_snackbar(res['response']['message'],'ok')
        if (res['liked']){
            elm.classList.add('post-liked');
            count = document.getElementById('post_likes')
            count.innerText = count.innerText*1 + 1
        }
        else{
            elm.classList.remove('post-liked');
            count = document.getElementById('post_likes')
            count.innerText = count.innerText*1 - 1
        }
    }).catch(err => { 
        add_snackbar(responseData,'warning')
        console.log(err)
    });

    // add_snackbar('pending');
}


function like_comment_toggle(comment_id,elm){
    if (!is_logged_in()) return;
    // add_snackbar(host)
    const res = sendHttpRequest("POST","http://"+host+"/like_comment",{
        user_id : USER_ID,
        token : USER_TOKEN,
        comment_id : comment_id
    }).then(responseData => {
        console.log(responseData)
        let res = JSON.parse(responseData)
        add_snackbar(res['response']['message'],'ok')
        if (res['liked']){
            elm.classList.add('comment-liked');
            count = document.getElementById('comment_'+comment_id)
            count.innerText = count.innerText*1 + 1
        }
        else{
            elm.classList.remove('comment-liked');
            count = document.getElementById('comment_'+comment_id)
            count.innerText = count.innerText*1 - 1
        }
    }).catch(err => { 
        add_snackbar(responseData,'warning')
        console.log(err)
    });

    // add_snackbar('pending');
}

comments_added = 0
function add_post_comment(post_id){

    if (!is_logged_in()) return;

    var content = document.getElementsByClassName("comment-editor")[0].parentElement.getElementsByClassName("ck-editor__editable")[0];
    // var content = edirorObj.getData()
    if( content.innerText.trim() == "" ){
        add_snackbar('comment field is empty!');
        return 0;
    }
    pending = add_snackbar('<div class="loader"></div>');

    comments_count = document.getElementsByClassName('comments-count')[0]
    const res = sendHttpRequest("POST","http://"+host+"/add_post_comment",{
        text : content.innerHTML,
        post_id : post_id,
        token: USER_TOKEN,

    }).then(responseData => {
        comments_added++;
        
        let res = JSON.parse(responseData)
        // console.log(res)
        remove_snackbar(pending,'function');
        add_snackbar(res['server message'],'ok')
        append_to_class('comments',res['data'])
        update_mh_value()
        comment_wd.editor.setData("");
        comments_count.innerHTML = (comments_count.innerText.split('/')[0]*1 +1 )+" / "+(comments_count.innerText.split('/')[1]*1 +1 );


    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)
    });
}


comment_page = 1
function get_comments(post_id,self){
    
    if(!is_logged_in(mute=true)) USER_ID =-1
    comment_page++;

    parent = self.parentElement;
    loader = parent.getElementsByClassName('loader')[0];

    self.classList.add('hidden');
    loader.classList.remove('hidden');
    comments_count = parent.getElementsByClassName('comments-count')[0];
    

    const res = sendHttpRequest("POST","http://"+host+"/get/comments"+"?page="+comment_page,{
        user_id : USER_ID,
        post_id:post_id,
  
    }).then(responseData => {
        
        let res = JSON.parse(responseData)
        console.log(res)
        prepend_to_class('comments',res['data'])
        update_mh_value()
        loader.classList.add('hidden');
        shown = (res['pages']['number_of_comments_shown']*1+comments_added);
        total = (res['pages']['number_of_comments']*1);

        comments_count.innerText = Math.min(shown,total)+" / "+(total);

        if(res['pages']['current_page']*1 < (res['pages']['number_of_pages']*1-1) ){
            self.classList.remove('hidden');
        }
    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)
        loader.classList.add('hidden');
    });   
}

function update_post(){

    




    location.reload()
}

function add_post(event){
    console.log(event)
    event.preventDefault();

    var new_post_form = document.getElementById("post_control_form");
    var formData = new FormData(new_post_form);

    var content = document.getElementsByClassName("editor")[0].parentElement.getElementsByClassName("ck-editor__editable")[0];
  

    if( content.innerText.trim() == "" ){
        add_snackbar('text field is empty!');
        return 0;
    }

    
    formData.append("tags_count",document.querySelectorAll('input[type="checkbox"]').length)
    formData.append("text",content.innerHTML)
    formData.append("token",USER_TOKEN)
    formData.append("user_id",USER_ID)
    
    
    const res = sendHttpRequest("POST","http://"+host+"/add_new_post",formData,false).then(responseData => {
        let res = JSON.parse(responseData)
        add_snackbar(res['server message'],"ok")
        add_snackbar(res['uploader message'],res['uploader status'])
        window.location.replace("/posts/"+document.querySelector('input[name="title"]').value.replace(new RegExp(' ', 'g'),'-'));

        
    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)
    });
    
    console.log(Array.from(formData))


}

function edit_post(post_id){
    if (!is_logged_in()) return;

    const res = sendHttpRequest("POST","http://"+host+"/get/edit_post",{
        post_id : post_id,
  
    }).then(responseData => {

        elm = document.createElement('div')
        elm.innerHTML = responseData
        document.body.append(elm)
        ckeditor_init('.editor','full');
        document.body.classList.add('modal-visiable');

        // console.log(responseData)
      

    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)

    });  

}

function delete_post(post_id){
    if (!is_logged_in()) return;
    if (!disaster_prevention())return;

    const res = sendHttpRequest("DELETE","http://"+host+"/delete/delete_post",{
        post_id : post_id,
        token:USER_TOKEN,
    }).then(responseData => {


        let res = JSON.parse(responseData)
        add_snackbar(res['response']['message'],"ok")
        // console.log(responseData)
        setTimeout(()=>{
            window.location.replace("/");
        },2000)

    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)

    });  

}

function delete_comment(comment_id){
    if (!is_logged_in()) return;
    if (!disaster_prevention())return;

    const res = sendHttpRequest("DELETE","http://"+host+"/delete/delete_comment",{
        comment_id : comment_id,
        token:USER_TOKEN,
    }).then(responseData => {


        let res = JSON.parse(responseData)
        add_snackbar(res['server message'],"ok")
        // console.log(responseData)
        setTimeout(()=>{
            location.reload();
        },2000)

    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)

    });  

}


function update_post(event){
    console.log(event)
    event.preventDefault();

    var new_post_form = document.getElementById("post_control_form");
    var formData = new FormData(new_post_form);
    post_wd.editor.updateSourceElement()
    var content = document.getElementsByClassName("editor")[0].parentElement.getElementsByClassName("ck-editor__editable")[0];
  

    if( content.innerText.trim() == "" ){
        add_snackbar('text field is empty!');
        return 0;
    }

    
    formData.append("tags_count",document.querySelectorAll('input[type="checkbox"]').length)
    formData.append("text",content.innerHTML)
    formData.append("token",USER_TOKEN)
    formData.append("user_id",USER_ID)
    
    const res = sendHttpRequest("PUT","http://"+host+"/update_post",formData,false).then(responseData => {
        
    let res = JSON.parse(responseData)
        add_snackbar(res['server message'],"ok")
        add_snackbar(res['uploader message'],res['uploader status'])

        window.location.replace("/posts/"+document.querySelector('input[name="title"]').value.replace(new RegExp(' ', 'g'),'-'));
        
    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)
    });
    
    console.log(Array.from(formData))


}




function edit_comment(comment_id){
    if (!is_logged_in()) return;

    const res = sendHttpRequest("POST","http://"+host+"/get/edit_comment",{
        comment_id : comment_id,
  
    }).then(responseData => {

        elm = document.createElement('div')
        elm.innerHTML = responseData
        document.body.append(elm)
        ckeditor_init('.editor','comment');
        document.body.classList.add('modal-visiable');

        // console.log(responseData)
      

    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)

    });  

}


function update_comment(event){
    event.preventDefault();

    if (!is_logged_in()) return;

    post_wd.editor.updateSourceElement()
    var content = document.getElementsByClassName("editor")[0].parentElement.getElementsByClassName("ck-editor__editable")[0];
    comment_id = document.querySelector('input[name="comment_id"]').value
    if( content.innerText.trim() == "" ){
        add_snackbar('comment field is empty!');
        return 0;
    }
    // pending = add_snackbar('<div class="loader"></div>');

    comments_count = document.getElementsByClassName('comments-count')[0]
    const res = sendHttpRequest("PUT","http://"+host+"/update_comment",{
        text : content.innerHTML,
        comment_id : comment_id,
        token: USER_TOKEN,

    }).then(responseData => {
     
        add_snackbar(res['server message'],'ok')
        location.reload();
     
    }).catch(err => { 
        add_snackbar(err,'warning')
        console.log(err)
    });
}