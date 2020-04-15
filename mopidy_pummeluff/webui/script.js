/*
 * API class which communicates with the Pummeluff REST API.
 */

class API {

    /*
     * Send AJAX request to REST API endpoint.
     */

    request = (endpoint, data, callback) => {
        let init = {}
        if(data)
            init = { method: 'POST', body: data }

        fetch(endpoint, init)
        .then((response) => {
            return response.json()
        })
        .then(callback)

    }

    /*
     * Refresh the registry.
     */

    refreshRegistry = () => {
        let callback = (response) => {
            let tagsContainer = document.getElementById('tags')
            while(tagsContainer.firstChild) {
                tagsContainer.removeChild(tagsContainer.firstChild)
            }

            for(let tag of response.tags) {
                let tagElement = document.createElement('div')
                tagElement.setAttribute('class', 'tag')

                let args = new Array('alias', 'uid', 'action_class', 'parameter')
                for(let arg of args) {
                    let spanElement = document.createElement('span')
                    let value       = tag[arg] ? tag[arg] : '-'
                    spanElement.setAttribute('class', arg.replace('_', '-'))
                    spanElement.innerHTML = value
                    tagElement.appendChild(spanElement)
                }

                tagsContainer.appendChild(tagElement)
            }
        }

        this.request('/pummeluff/registry/', false, callback)
    }

    /*
     * Refresh the tags.
     */

    refreshActionClasses = () => {
        let callback = (response) => {
            let select = document.getElementById('action-class');
            while(select.firstChild)
                select.removeChild(select.firstChild)

            for(let action_class in response.action_classes) {
                let option = document.createElement('option')
                option.setAttribute('value', action_class)
                option.innerHTML = action_class + ' (' + response.action_classes[action_class] + ')'
                select.appendChild(option)
            }
        }

        this.request('/pummeluff/action-classes/', false, callback)
    }

    /*
     * Reset the form.
     */

    formCallback = (response) => {
        if(response.success) {
            this.refreshRegistry()
            document.getElementById('uid').value                = ''
            document.getElementById('alias').value              = ''
            document.getElementById('parameter').value          = ''
            document.getElementById('action-class').selectIndex = 0
        } else {
            window.alert(response.message)
        }
    }

    /*
     * Register a new tag.
     */

    register = () => {
        let form = document.getElementById('register-form')
        let data = new FormData(form)
        this.request('/pummeluff/register/', data, this.formCallback)
    }

    /*
     * Unregister an existing tag.
     */

    unregister = () => {
        let form = document.getElementById('register-form')
        let data = new FormData(form)
        this.request('/pummeluff/unregister/', data, this.formCallback)
    }

    /*
     * Get latest scanned tag.
     */

    getLatestTag = () => {
        let latest_tag = undefined

        let uid_field           = document.getElementById('uid')
        let alias_field         = document.getElementById('alias')
        let parameter_field     = document.getElementById('parameter')
        let action_class_select = document.getElementById('action-class')

        uid_field.value              = ''
        alias_field.value            = ''
        parameter_field.value        = ''
        action_class_select.selectIndex = 0

        let link = document.getElementById('read-rfid-tag')
        link.classList.add('reading')

        let do_request = () => {
            let callback = (response) => {
                if(latest_tag && response.success && JSON.stringify(response) != JSON.stringify(latest_tag)) {
                    uid_field.value = response.uid

                    if(response.alias)
                        alias_field.value = response.alias

                    if(response.parameter)
                        parameter_field.value = response.parameter

                    if(response.action_class)
                        action_class_select.value = response.action_class

                    link.classList.remove('reading')
                } else {
                    setTimeout(() => do_request(), 1000)
                }

                latest_tag = response
            }

            api.request('/pummeluff/latest/', false, callback)
        }

        do_request()
    }

}

api = new API()

api.refreshRegistry()
api.refreshActionClasses()

document.addEventListener('click', (event) => {
    let target = event.target
    let div    = target.closest('div')

    if(div && div.classList.contains('tag')) {
        for(let child of div.children) {
            document.getElementById(child.className).value = child.innerHTML.replace(/^-$/, '')
        }
    }
})

document.getElementById('register-form').onsubmit = () => {
    api.register()
    return false;
}

document.getElementById('unregister-button').onclick = () => {
    api.unregister()
    return false
}

document.getElementById('read-rfid-tag').onclick = () => api.getLatestTag()
