/*
 * Settings / constants.
 */

const defaultAction = 'Tracklist'
let latestTag       = null


/**
 * Evaluate code with a clean context.
 */

const cleanContextEval = (code, context) => new Function(  // eslint-disable-line no-new-func
    ...Object.keys(context),    // Function arguments
    code,                       // Function body
)(...Object.values(context))    // Call w/ arguments

/**
 * Render a HTML <template> tag found in the HTML DOM#.
 */

const renderTemplate = (id, context) => {
    const template     = document.querySelector(`template#${id}`).cloneNode(true)
    template.innerHTML = cleanContextEval(`return \`${template.innerHTML.trim()}\``, context)
    return template.content
}

/**
 * Send an API request.
 */

const requestApi = (endpoint, data) => {
    let options = {}

    if(data) {
        options = {
            'body': data,
            'method': 'POST',
        }
    }

    return fetch(endpoint, options)
        .then(response => response.json())
}

/**
 * Refresh the registry.
 */

const refreshActionClasses = () => {
    requestApi('/pummeluff/actions/').then(response => {
        const select = document.getElementById('action')
        select.options.length = 0
        for(const [action, description] of Object.entries(response.actions))
            select.appendChild(renderTemplate('action-template', {action, description}))
        select.value = defaultAction
    })
}

/**
 * Refresh the registry.
 */

const refreshRegistry = () => {
    requestApi('/pummeluff/registry/').then(response => {
        const tbody = document.querySelector('#tags tbody')
        tbody.innerHTML = ''
        for(const tag of response.tags)
            tbody.appendChild(renderTemplate('tag-template', tag))
    })
}

/**
 * Callback to read the latest tag.
 */

const readTag = () => {
    requestApi('/pummeluff/latest/').then(response => {
        const {uid, alias, parameter, action, success, scanned} = response

        if(!latestTag)
            latestTag = response

        if(!success || (success && scanned === latestTag.scanned))
            return

        document.getElementById('uid').value       = uid
        document.getElementById('alias').value     = alias ? alias : ''
        document.getElementById('parameter').value = parameter ? parameter : ''
        document.getElementById('action').value    = action !== 'Action' ? action : defaultAction

        latestTag = response
    })
}

/**
 * Submit form.
 */

const submitForm = event => {
    event.preventDefault()

    const data = new FormData(event.target)

    requestApi(`/pummeluff/${event.submitter.id}/`, data).then(response => {
        const error  = document.getElementById('error')
        error.hidden = response.success
        if(!response.success) {
            error.textContent = response.message
            return
        }

        document.getElementById('uid').value          = ''
        document.getElementById('alias').value        = ''
        document.getElementById('parameter').value    = ''
        document.getElementById('action').selectIndex = 0

        refreshRegistry()
    })
}

/*
 * Initialise everything after DOM is loaded.
 */

document.addEventListener('DOMContentLoaded', () => {
    refreshActionClasses()
    refreshRegistry()

    const readTagInterval = 1000
    readTag()
    setInterval(readTag, readTagInterval)

    document.querySelector('form').addEventListener('submit', submitForm)
})
