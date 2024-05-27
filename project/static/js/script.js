arr=["Dos Detected [host unreachable]..." , "Dos Detected [host unreachable]..." ,"Dos Detected [host unreachable]..." , "Detecting IP..." , "Detecting IP..." , "IP Detected [10.0.15.24]..." , "Blocking IP [10.0.15.24]..." , "host back to normal ..." , "Listening for DOS..."]


function addeachLetter(j ,p,a){
    if (j=='['){
        p.innerHTML+= "<span class='red'>"
    }
    p.innerHTML+=j;
    a.append(p);

    if(j==']'){
        p.innerHTML+= "</span>"
    }
}

async function displayText(i){
    let p = document.createElement("p");
    p.innerHTML="<span class='green'>abch@linux:</span><span class='blue'> ~/ </span>"
    var a = document.getElementById('content');

    for (const j of i){
        await new Promise(resolve => setTimeout(resolve, 50));
        addeachLetter(j, p, a);
    }

    // p.innerHTML=i
    // a.append(p)

}

async function main(){
    for (const i of arr){
        await displayText(i)
    }
}

main()



document.getElementById('up').addEventListener("click",()=>{
    alert("Yes that button doesnt work :(");
})

















