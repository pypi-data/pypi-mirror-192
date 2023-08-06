const saveAction = 'saveAction'
const saveNewAction = 'saveNewAction'
const clickedBtn = 'clicked-btn'
const idModalMessages = '#messagesModal'

class Jquery {
    static refresh(idElement) {
        $(`#${idElement}`).load(window.location.href + ` #${idElement}>*`);
    }

    static refreshContainer() {
        this.refresh('container')
    }

    static refreshMessages() {
        this.refresh('messages')
    }



    static clearFormFields(formComponent) {
        $(formComponent).find('input,select,textarea').val('').end()
    }
}


