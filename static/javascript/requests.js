var host = window.location.host

const sendHttpRequest = (method,url,data) => {
    const promise = new Promise( (resolve,reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method,url);


        if (data){
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

        xhr.send(JSON.stringify(data));

    });

    return promise;

};

function likePostToggle(userToken,post){

    console.log("started")
    add_snackbar('pending');
    // add_snackbar(host)
    const res = sendHttpRequest("POST","http://"+host+"/like_post",{
        user_id : "1",
        post_id : "1"
    }).then(responseData => {
        
        console.log(responseData)
        add_snackbar(responseData,'ok')
    }).catch(err => { 
        add_snackbar(responseData,'warning')
        console.log(err)
    });

    // add_snackbar('pending');


    
}