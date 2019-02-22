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

        fetch(endpoint, init)
        .then(function(response)
        {
            return response.json()
        })
        .then(callback)

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
                option.innerHTML = type + ' (' + response.types[type] + ')'
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
            if(response.success)
                api.refreshRegistry()
            else
                window.alert(response.message)
        }

        this.request('/pummeluff/register/', data, callback)
    }

    /*
     * Get latest scanned card.
     */

    getLatestCard()
    {
        let latest_card = undefined

        let uid_field       = document.getElementById('uid')
        let alias_field     = document.getElementById('alias')
        let parameter_field = document.getElementById('parameter')
        let type_select     = document.getElementById('type')

        uid_field.value         = ''
        alias_field.value       = ''
        parameter_field.value   = ''
        type_select.selectIndex = 0

        let link            = document.getElementById('read-rfid-card')
        link.classList.add('reading')

        let do_request = function()
        {
            let callback = function(response)
            {
                if(latest_card && response.success && JSON.stringify(response) != JSON.stringify(latest_card))
                {
                    uid_field.value = response.uid

                    if(response.alias)
                        alias_field.value = response.alias

                    if(response.parameter)
                        parameter_field.value = response.parameter

                    if(response.type)
                        type_select.value = response.type

                    link.classList.remove('reading')
                }
                else
                {
                    setTimeout(() => do_request(), 1000)
                }

                latest_card = response
            }

            api.request('/pummeluff/latest/', false, callback)
        }

        do_request()
    }

}

api = new API()

api.refreshRegistry();
api.refreshTypes();

document.getElementById('register-form').onsubmit = function()
{
    api.register()
    return false;
}

document.getElementById('read-rfid-card').onclick = () => api.getLatestCard()
