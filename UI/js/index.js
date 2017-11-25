var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
    $messages.mCustomScrollbar();
    setTimeout(function() {
        fakeMessage();
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    setTimeout(function() {
        realMessage(msg);
    }, 0);
}

$('.message-submit').click(function() {
    insertMessage();
});

$(window).on('keydown', function(e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
})

var FailMessage = [
    'GOTHAM的蝙蝠灯亮了，我要去拯救世界了！一会聊！',
    '企鹅人把我蝙蝠洞电脑炸了，现在无法提供聊天服务！',
    'WHY SO SERIOUS? Joker把我电脑炸了！现在无法提供聊天服务!',
    'DO YOU BLEED? 现在无法提供聊天服务!'
];

function fakeMessage() {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();
    setTimeout(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + '你好，我是BATBOT，你可以在这里问我问题' + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
    }, 10);

}
function realMessage(msg){
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();
    var url = "http://127.0.0.1:5000/chatbot";
    $.post( url, { query: msg },function(data){
        setTimeout(function() {
            $('.message.loading').remove();
            $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + data + '</div>').appendTo($('.mCSB_container')).addClass('new');
            setDate();
            updateScrollbar();
        }, 500);
    }).fail(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + FailMessage[Math.floor(Math.random()*FailMessage.length)] + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();  });
}

