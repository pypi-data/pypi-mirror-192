class Date {
    static date = new Date()

    /**
     * Get a month of year [0-11] and returns -1 if index out of range
     * @param index
     * @returns {number|any}
     */
    static getMonths(index) {
        const monthMap = new Map()
        monthMap.set(0, 'Janeiro');
        monthMap.set(1, 'Fevereiro');
        monthMap.set(2, 'Março');
        monthMap.set(3, 'Abril');
        monthMap.set(4, 'Maio');
        monthMap.set(5, 'Junho');
        monthMap.set(6, 'Julho');
        monthMap.set(7, 'Agosto');
        monthMap.set(8, 'Setembro');
        monthMap.set(9, 'Outubro');
        monthMap.set(10, 'Novembro');
        monthMap.set(11, 'Dezembro');
        return index < 0 || index > monthMap.size ? -1 : monthMap.get(index)
    }

    static getMonthDays(selectors) {
        return JSUtils.getElementByQS(selectors);
    }

    static getLastDay() {
        return new Date(this.date.getFullYear(), this.date.getMonth() + 1, 0).getMonth()
    }

    static getPrevLastDay() {
        return new Date(this.date.getFullYear(), this.date.getMonth(), 0).getMonth()
    }
}

