$(document).ready(function () {

    // ПОДСКАЗКИ
    $('[data-toggle="tooltip"]').tooltip();

    // РЕЙТИНГ
    var options = {
        max_value: 10,
        step_size: 1,
    };
    $(".rate").rate(options);

    // ПОИСК
    $('#show_search').click(function () {
        $('#search_form_wrapper').toggleClass('now_show');
        $('#search_form_wrapper').toggle('slide', {direction: "right"}, 300);

        if ($('#search_form_wrapper').hasClass('now_show')) {
            $('#main_menu li:not(.li_search)').animate({opacity: 0.2,}, 300,);
        } else {
            $('#main_menu li:not(.li_search)').animate({opacity: 1,}, 300,);
        }

        $(this).find('.fa').each(function () {
            $(this).toggle();
        })
    });


    $('#search_input').focus(function () {
        $('#search_suggestion').slideToggle(1000);
    });
    $('#search_input').focusout(function () {
        $('#search_suggestion').slideToggle(1000);
    });


    // ВСЕ КОММЕНТЫ
    $('#show_all_comments_btn').click(function () {
        $(this).toggle(500);
        $('.hidden_comments .s_comment').each(function () {
            $(this).slideToggle(500);
        })
    });

    // КАТАЛОГ ВЫБОРКА
    $('.show_all_dropdown').click(function (e) {
        e.stopPropagation();
        $(this).toggle();
        $(this).siblings(".hide_all_dropdown").toggle();
        var menu = $(this).data('menu');
        $(menu + ' .advanced').each(function () {
            $(this).toggle();
        })
    });

    $('.hide_all_dropdown').click(function (e) {
        e.stopPropagation();
        $(this).toggle();
        $(this).siblings(".show_all_dropdown").toggle();
        var menu = $(this).data('menu');
        $(menu + ' .advanced').each(function () {
            $(this).toggle();
        })
    });


    // LIGHTGALLERY
    $('#frames_wrapper').lightGallery({
        selector: '.wrapper',
        thumbnail: false
    });


    // MOBILE
    $('body').click(function (e) {
        if ($(e.target).closest('#mobile_menu_wrapper').length === 0) {
            $('.show_mobile_menu').each(function () {
                var menu = $(this).data('menu');
                $('#' + menu).slideUp(500);
                $(this).removeClass('open');
            });
        }
    });

    $('#search_input_mobile').focus(function () {
        $('#search_suggestion_mobile').slideToggle(1000);
    });

    $('#search_input_mobile').focusout(function () {
        $('#search_suggestion_mobile').slideToggle(1000);
    });

    $('.show_mobile_menu').click(function () {

        var current = $(this);

        $('.show_mobile_menu').each(function () {
            if (($(this).hasClass('open')) && ($(this).data('menu') != $(current).data('menu'))) {
                var menu = $(this).data('menu');
                $('#' + menu).slideUp(500);
                $(this).removeClass('open');
            }
        });

        var menu = $(this).data('menu');
        $('#' + menu).slideToggle(500);
        $(this).toggleClass('open');
    });
});







