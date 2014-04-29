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
                        if(!elre.test(el.val())) {
                            return el;
                        } else {
                            zdw.removeError(el);
                        }
                    }
                }
            }
            return true;
        },
        checkPasswords: function(fm){
            var pwds = fm.find('[type=password]');
            if(pwds.length === 2) {
                return pwds[0].value === pwds[1].value;
            }
            return false;
        },
        focusError: function(el){
            el.closest('.control-group').addClass('error');
            el.siblings('.help-block').show();
        },
        removeError: function(el){
            var help = el.siblings('.help-block'), group;
            if(help.length) {
                help.hide();
                el.closest('.control-group').removeClass('.error');
            }
        }
    };

    window.zdw = zdw;
})();
$(function(){
    $('#reg-submit,#login-submit').click(function(){
        var me = $(this),
            fm = me.closest('.modal').find('form'),
            validateRuslt = zdw.checkForm(fm[0]);
        if(this.id === "reg-submit") {
            validateRuslt = zdw.checkPasswords(fm);
            if(!validateRuslt) {
                $(fm.find('[type=password]')).each(function(){
                    zdw.focusError($(this));
                });
                return ;
            }
        }
        if(validateRuslt === true) {
            fm.submit();
        } else {
            zdw.focusError(validateRuslt);
            return false;
        }
    });
    $('#loginwin,#registerwin').on('hidden', function(){
        var fm = $(this).find('form'), i, len, elements;
        elements = fm[0].elements;
        for(i=0,len=elements.length;i<len;i++) {
            if(elements[i].name) {
                $(elements[i]).off('focus');
            }
        }
    }).on('show', function(){
        var fm = $(this).find('form'), i, len, elements;
        elements = fm[0].elements;
        for(i=0,len=elements.length;i<len;i++) {
            if(elements[i].name) {
                $(elements[i]).focus(function(){
                    var me = $(this),
                        help = me.siblings('.help-block'),
                        group = me.closest('.control-group');
                    help.length && help.hide();
                    group.removeClass('error');
                });
            }
        }
        fm.find('#reg-password2').blur(function(){
            var r = zdw.checkPasswords($(this.form));
            if(!r) {
                zdw.focusError($(this));
            }
        });
    });
});