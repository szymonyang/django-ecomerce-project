console.log("Hello Werld")

const updateBtn = document.getElementsByClassName("update-cart");

for (let i = 0; i <updateBtn.length; i++){
    updateBtn[i].addEventListener("click", function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log("product id:", productId, "action:", action)

        console.log("User: ", user)
        if(user === "AnonymousUser"){
            console.log("User is not authenticated")
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log("User is authenticated, sending data")
    const url = "/update_item/"
    fetch(url, {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({"productId":productId, "action": action})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        console.log("data", data)
    })
}