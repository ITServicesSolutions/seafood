var updateBtns = document.getElementsByClassName('update-panier')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var produit_id = this.dataset.produit
        var action = this.dataset.action
        console.log('produit_id:', produit_id, 'action:', action)

        console.log('USER:', user)

        if (user === 'AnonymousUser') {
            var url = '/login/'
            console.log('Redirecting')
            location.replace(url)
        } else {
            updateUserPanier(produit_id, action)
        }
    })
}

function updateUserPanier(produit_id, action) {
    console.log('User is logged in, sending data..')

    var url = '/update_detail/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'produit_id': produit_id, 'action': action })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}