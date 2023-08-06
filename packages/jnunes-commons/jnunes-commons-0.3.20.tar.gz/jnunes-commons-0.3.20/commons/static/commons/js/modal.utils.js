class Modal {
    static open(idModal) {
        $(`#${idModal}`).modal('show');
    }

    static close(idModal) {
        $(`#${idModal}`).modal('hide');
    }

    static closeAndRemove(idModal, idContainerModal) {
        this.close(idModal);
        $(`#${idModal}`).remove()
    }

    static appendChildToBody(idContainerModal, idModal, idForm, titleModal, modalBody, cancelFuncName, confirmFuncName) {
        let divContainerModal = document.createElement('div')
        divContainerModal.id = idContainerModal
        divContainerModal.innerHTML = this.baseContainer(idModal, idForm, titleModal, modalBody, cancelFuncName, confirmFuncName)
        document.body.appendChild(divContainerModal)
    }

    static addMessages(html) {
        $(idModalMessages).empty().append(html)
    }

    static handlePostForm(idModal, idForm, url) {
        $(`#${idForm}`).on('submit', function (event) {
            event.preventDefault();
            SpinnerUtils.showSpinner();

            const jsonRequest = JSUtils.formToJSON(this);

            // add clicked button(save&New or Save) to json
            jsonRequest['button'] = $(this).find(`.${clickedBtn}`).attr('id')

            fetch(url, {
                method: 'POST',
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                    "X-CSRFToken": DjangoUtils.getCookie("csrftoken"),
                },
                body: JSON.stringify(jsonRequest)
            }).then(res => res.json())
                .then(json_response => {


                    if (json_response.status === 1) {
                        let html = null

                        $(idModalMessages).empty();
                        Object.entries(json_response.data).forEach(ret => {
                            html = `<div class="alert alert-danger" role="alert"><strong>${ret[0]}:</strong> ${ret[1]}</div>`
                            Modal.addMessages(html)
                        });
                    } else {
                        if (jsonRequest.button === saveAction) {
                            Modal.close(idModal)
                            Jquery.refreshContainer()
                        }

                        if (jsonRequest.button === saveNewAction) {
                            let html = `<div class="alert alert-success" role="alert">${json_response.data}</div>`
                            Modal.addMessages(html)
                            Jquery.clearFormFields(this)
                        }
                    }
                })
                .catch(err => console.log(err))
                .finally(() => {
                    $(this).find(`.${clickedBtn}`).removeClass(clickedBtn);
                    SpinnerUtils.hideSpinner()
                })
        })
    }

    /**
     *
     * @param idModal String
     * @param idForm String
     * @param titleModal String
     * @param modalBody htmlContent
     * @param cancelFuncName functionName();
     * @param confirmFuncName functionName();
     * @returns {string}
     */
    static baseContainer(idModal, idForm, titleModal, modalBody, cancelFuncName, confirmFuncName) {
        return `<div class="modal fade" id="${idModal}" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                    data-focus-on="input:first">
                    <form id="${idForm}" name="${idForm}">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 id="title_modal" class="modal-title">${titleModal === null ? '' : titleModal}</h5>
                                </div>
                                <div class="modal-body">${modalBody}</div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" href="#${idModal}"
                                     ${cancelFuncName == null ? '' : 'onclick="' + cancelFuncName + '"'}>Cancelar</button>
                                    <button type="button" class="btn btn-sm btn-primary" onclick="${confirmFuncName}">Confirmar</button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>`
    }
}
