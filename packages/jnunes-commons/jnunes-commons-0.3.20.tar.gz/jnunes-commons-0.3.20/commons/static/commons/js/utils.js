class JSUtils {
    static isJSONEmpty(json) {
        return json == null || Object.keys(json).length === 0;
    }

    static formToJSON(elements) {
        return [].reduce.call(elements, (data, element) => {
                data[element.name] = element.value;
                return data;
            }, {}
        );
    }

    static existsElement(idElement) {
        return document.contains(document.getElementById(idElement))
    }

    static setStyleDisplayById(idElement, styleDisplay) {
        if (this.existsElement(idElement)) {
            document.getElementById(idElement).style.display = styleDisplay
            return true;
        }
        return false;
    }

    static getQueryParameters() {
        return new URLSearchParams(window.location.search);
    }

    static existsElementByQS(selectors) {
        return document.contains(document.querySelector(`${selectors}`))
    }

    static getElementByQS(selectors) {
        return document.querySelector(`${selectors}`)
    }

    /**
     * Remove element from DOM by ID
     * @param elementId
     * @returns {boolean}
     */
    static removeById(elementId) {
        if (this.existsElement(elementId)) {
            document.getElementById(elementId).remove()
            return true;
        }
        return false;
    }

    /**
     *
     * @param tagName HTML Element Tag
     * @param elementId Element ID
     * @param classList List of CSS Classes
     * @param html HTML Content
     */
    static buildElement(tagName, elementId, classList, html) {
        try {
            let childElement = document.createElement(tagName);
            if (elementId != null) {
                childElement.id = elementId
            }
            if (classList != null) {
                childElement.classList.add(...classList)
            }
            childElement.innerHTML = html
        } catch (e) {
            throw new Error(e)
        }
    }

    /**
     *
     * @param tagName HTML Element Tag
     * @param elementId Element ID
     * @param classList List of CSS Classes
     * @param html HTML Content
     * @param idContainer Container ID
     * @param appendToBody Append to body or to container
     */
    static appendChild(tagName, elementId, classList, html, idContainer, appendToBody = false) {
        try {
            let childElement = document.createElement(tagName);
            if (elementId != null) {
                childElement.id = elementId
            }
            if (classList != null) {
                childElement.classList.add(...classList)
            }
            childElement.innerHTML = html
            if (idContainer != null && this.existsElement(idContainer)) {
                document.getElementById(idContainer).appendChild(childElement)
            }
            if (appendToBody && idContainer === null) {
                document.body.appendChild(childElement)
            }
        } catch (e) {
            throw new Error(e)
        }
    }

    static appendChildToExistsElement(element, html) {
        element.innerHTML = html
    }

    static replaceBrowserUrl(newUrl) {
        if (newUrl !== null) {
            window.history.pushState({path: newUrl}, '', newUrl);
        }
    }
}


class DjangoUtils {
    static getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

class SpinnerUtils {
    static showSpinner(idSpinner = 'loading', idContainer = 'container', message = 'Carregando...') {
        JSUtils.appendChild('div', idSpinner, null, HTMLUtils.getSpinner(message), idContainer)
    }

    static hideSpinner(idSpinner = 'loading') {
        JSUtils.removeById(idSpinner)
    }
}

class HTMLUtils {
    static getTimeContainerHtml() {
        return ` <div class="times">`
    }

    static getHtmlModal(json, idModal) {
        return `<!-- Modal -->
            <div class="modal fade" id="${idModal}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" >${json.title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" onclick="closeModal()"></button>
                        </div>
                        <div class="modal-body">
                            <!-- Include element with django after apend this element in DOM /-->
                        </div>
                    </div>
                </div>
            </div>`
    }

    static getInputRadio(idElement, value) {
        return `
        <label for="${idElement}">
            <input class="form-check-input" name="inputRadios" id="${idElement}" type="radio">
            <span>${value}</span>
        </label>
        `
    }

    /**
     *
     * @param toastId
     * @param bodyMsg String
     * @param showHeader Boolean
     * @param headerTitle String
     * @param headerMsg String
     * @returns {string} Html
     */
    static getHtmlToast(toastId, bodyMsg, showHeader = false, headerTitle, headerMsg) {
        let _headerHtml = `<div class="toast-header">
                                <strong class="me-auto">${headerTitle}</strong>
                                <small>${headerMsg}</small>
                                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>`

        return `<div class="toast-container position-fixed bottom-0 end-0 p-3">
                    <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                        ${showHeader ? _headerHtml : ''}
                        <div class="toast-body">
                            ${bodyMsg}
                        </div>
                    </div>
                </div>`
    }

    static getSpinner(message) {
        return `<div class="btn btn-primary position-fixed bottom-0 end-0 p-2 mb-2 me-2" style="cursor: default">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                ${message === null ? 'Loading...' : message}
            </div> `
    }
}

class FetchUtils {
    static fetchHandlerSpinnerGet(url, init, func) {
        init = init || {
            method: 'GET',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        }
        FetchUtils.fetchHandlerSpinner(url, init, func)
    }

    static fetchHandlerSpinner(url, init, func) {
        SpinnerUtils.showSpinner();

        fetch(url, init)
            .then(json => {
                SpinnerUtils.hideSpinner();
                func(json);
            }).catch(err => {
                SpinnerUtils.hideSpinner();
                console.log(err)
            }
        )
    }

    static fetchHandler(url, init, func) {
        fetch(url, init)
            .then(json => func(json)).catch(err => console.log(err))
    }

    /**
     * addEventListener for element id passed on parameter. After, call a  fetchHandlerGet function.
     * @param elementListenerId element id to add eventListener
     * @param urlPath url path used to concat no queryString
     *
     * ex: If you passed '/blog/', then the complete url was like: http://localhost:8000/blog/?query=xxxxxx
     */
    static eventListenerThenFetchHandlerGet(elementListenerId, urlPath) {
        let search = document.getElementById(elementListenerId)
        search.addEventListener('keypress', (e) => {
            if (e.code === 'Enter') {
                const searchValue = e.target.value;
                const queryString = searchValue === null ? '' : '?query=' + searchValue
                const url = `${urlPath}${queryString}`
                console.log(url)
                FetchUtils.fetchHandlerSpinnerGet(url, null, FetchUtils.afterGetEventListenerThenFetchHandlerGet)
            }
        })
    }

    static afterGetEventListenerThenFetchHandlerGet(json) {
        JSUtils.replaceBrowserUrl(json['url'])
        Jquery.refreshContainer();
    }
}