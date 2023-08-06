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
}
