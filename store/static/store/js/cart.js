console.log("Hello Werld, cart.js")

const updateBtn = document.getElementsByClassName("update-cart");

for (let i = 0; i <updateBtn.length; i++){
    updateBtn[i].addEventListener("click", function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log("product id:", productId, "action:", action)

        console.log("User: ", user)
        if(user === "AnonymousUser"){
            addCookieItem(productId, action)
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
            "Content-Type":"application/json",
            "X-CSRFToken": csrftoken
        },
        body:JSON.stringify({"productId":productId, "action": action})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        console.log("data", data)
        // not efficient
        location.reload()
    })
}

function addCookieItem(productId, action){
	console.log("User is not authenticated. Cart: ", cart)

	if (action == "add"){
	    // Shuold use === ?
		if (cart[productId] == undefined){
		cart[productId] = {"quantity":1}

		}else{
			cart[productId]["quantity"] += 1
		}
	}

	if (action == "remove"){
		cart[productId]["quantity"] -= 1

		if (cart[productId]["quantity"] <= 0){
			console.log("Item should be deleted")
			delete cart[productId];
		}
	}
	console.log("CART:", cart)
	document.cookie ="cart=" + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}