// JavaScript Document
$(document).ready(function (e) {
    /*绑定登录连接*/
    $('[command="login"]').click(function () {
        //App.user.openLoginWin();
    });

    $('[command="register"]').click(function () {
       // App.user.openRegisterWin();
    });


    $('#modalwin').on('show',function(e,w){
        console.log(e);
        console.log(w);

    });

});


var App = {
    users: {
        modalWinConfig : {
            login : {

            },
            register : {

            }
        },
        openLoginWin: function () {
//            $('.modal-title').text('用户登录');
//            $('#modalwin').modal({
//                remote : true
//            });
////            $('.modal-body').html('<form>' +//
////                '用&nbsp;&nbsp;户&nbsp;&nbsp;名：<input type="text" name="username" placeholder="用户名/邮箱" autocomplete="off"/><br />' +//
////                '密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码：<input type="password" name="password" placeholder="" autocomplete="off"/><br />' +//
////                '</form>');
//            $('.modal-footer').html('<button class="btn btn-link" data-dismiss="modal" aria-hidden="true">忘记密码？</button>' +//
//                '<button class="btn btn-success">登录</button>');
//            $('#modalwin').modal('show');

        },
        openRegisterWin: function () {
            $('.modal-title').text('注册新用户');
            $('.modal-body').html('<form>' +//
                '用&nbsp;&nbsp;户&nbsp;&nbsp;名：<input type="text" name="username", placeholder="请输入用户名" /><br />' +//
                '昵&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;称：<input type="text" name="username", placeholder="请输显示的昵称" /><br />' +//
                '密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码：<input type="password" name="password", placeholder="请输入登录密码" /><br />' +//
                '确认密码：<input type="password" name="validate_password", placeholder="请确认登录密码" /><br />' +//
                '电子邮箱：<input type="email" name="validate_password", placeholder="请输入电子邮箱" /><br />' +//
                '</form>');
            $('.modal-footer').html('<button class="btn btn-link" data-dismiss="modal" aria-hidden="true">已有帐号，请登录</button> <button class="btn btn-success">注册</button>');
            $('#modalwin').modal('show');
        }
    },
    assistFns: {
    }
}