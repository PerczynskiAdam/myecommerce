var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++){
   updateBtns[i].addEventListener('click', function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      console.log(productId, action)
      console.log(user)

      if (user == "AnonymousUser"){
         addCookieItem(productId, action)
      }else{
         updateCartUser(productId, action)
      }
   })
}

function addCookieItem(productId, action){
   // console.log("User is not logged in...")

   if(action =='add'){
      if(cart[productId] == undefined){//mozem odniesc sie do zmiennej cart, ponieważ jest w pliku main.html
         cart[productId] = {'quantity': 1} //obiekt cart wyglada {1: {'quantity': 1}, 2:{}}. Robimy access poprzez id i wpisujemy quantity jako 1
      }else{
         cart[productId]['quantity'] += 1// zwiększamy quantity o `
      }

   }
   if(action =='remove'){
      cart[productId]['quantity'] -=1

      if(cart[productId]['quantity'] <= 0){
         console.log("remove item")
         delete cart[productId]// usawa key value o zadanym id oraz elementy w nim zagniezdzone
      }
   }
   console.log('Cart:', cart)
   document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/" 
   location.reload()
}

function updateCartUser(productId, action){
   var url = '/update_cart/'

   fetch(url, {
      method:'POST',
      headers:{
         'Content-Type':'application/json',
         'X-CSRFToken':csrftoken,
      }, 
      body:JSON.stringify({'productId': productId, 'action': action})
   })
   .then((response) => {
      return response.json();
   })
   .then((data) => {
      console.log('data:', data)
      location.reload()
   });

}