(function(){
    var zdw = {
        checkForm: function(form){
            var i = 0, elements = form.elements, len = elements.length, el, elre;
            for(;i<len;i++) {
                el = elements[i];
                if(el.name) {
                    el = $(el);
                    elre = el.attr('data-format');
                    if(elre) {
                        elre = new RegExp(elre);
                        if(!elre.test(el.value)) {
                            return false;
                        }
                    }
                }
            }
            return true;
        },
        focusError: function(fm){}
    };

    window.zdw = zdw;
})();
$(function(){
    $('#reg-submit,#login-submit').click(function(){
        var me = $(this),
            fm = me.closest('.modal').find('form'),
            validateRuslt = zdw.checkForm(fm[0]);
        if(validateRuslt === true) {
            fm.submit();
        } else {
            zdw.focusError(fm[0]);
        }
    });

});