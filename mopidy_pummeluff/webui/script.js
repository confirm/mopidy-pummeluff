/*
 * API class which communicates with the Pummeluff REST API.
 */

class API {

    /*
     * Send AJAX request to REST API endpoint.
     */

    request(endpoint, data, callback)
    {
        let init = {}
        if(data)
            init = { method: 'POST', body: data }

        fetch(endpoint, init).then(function(response) {
            let obj = response.json()
            if(response.status == 200)
                return obj
            else
                window.alert(obj.message)
        }).then(callback)

    }

    /*
     * Refresh the registry.
     */

    refreshRegistry()
    {
        let callback = function(response)
        {
            let cardsContainer = document.getElementById('cards')
            while(cardsContainer.firstChild)
                cardsContainer.removeChild(cardsContainer.firstChild)

            for(let card of response.cards)
            {
                let cardElement = document.createElement('div')
                cardElement.setAttribute('class', 'card')

                let args = new Array('alias', 'uid', 'type', 'parameter')
                for(let arg of args)
                {
                    let spanElement = document.createElement('span')
                    let value = card[arg] ? card[arg] : '-'
                    spanElement.setAttribute('class', arg)
                    spanElement.innerHTML = value
                    cardElement.appendChild(spanElement)
                }

                cardsContainer.appendChild(cardElement)
            }
        }

        this.request('/pummeluff/registry/', false, callback)
    }

    /*
     * Refresh the card types.
     */

    refreshTypes()
    {
        let callback = function(response)
        {
            let select = document.getElementById('type');
            while(select.firstChild)
                select.removeChild(select.firstChild)

            for(let type in response.types)
            {
                let option = document.createElement('option')
                option.setAttribute('value', type)
                option.innerHTML = type + ': ' + response.types[type]
                select.appendChild(option)
            }
        }

        this.request('/pummeluff/types/', false, callback)
    }

    /*
     * Register a new card.
     */

    register()
    {
        let form = document.getElementById('register-form')
        let data = new FormData(form)

        let callback = function(response)
        {
            api.refreshRegistry()
        }

        this.request('/pummeluff/register/', data, callback)
    }

    /*
     * Get latest scanned card.
     */

    get_latest_card(callback)
    {
        this.request('/pummeluff/latest/', false, callback)
    }

}

api = new API();

api.refreshRegistry();
api.refreshTypes();

document.getElementById('register-form').onsubmit = function()
{
    api.register()
    return false;
}


