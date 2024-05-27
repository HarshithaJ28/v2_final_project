document.addEventListener("DOMContentLoaded",function(){
    console.log("DOM LOADED");
        var requestdiv = document.getElementById('requestinfo')

        var xhr = new XMLHttpRequest();
        xhr.open("GET" , "http://localhost:8000/",true);
        xhr.onreadystatechange = function(){
            if (xhr.readyState === XMLHttpRequest.DONE){
                if (xhr.status === 200){
                    let p=document.createElement('p')
                    p.innerHTML = "<span class=red>[*]</span> "
                    p.innerHTML += xhr.responseText
                    // console.log(this.responseText);
                    requestdiv.append(p)
                }
                else{
                    console.error("ERROR occured in fetching")
                }
            }
        }
        xhr.send();

});