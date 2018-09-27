(function ($) {
    $(function () {
        $('.tooltipped').tooltip();
        $('.sidenav').sidenav();
        $('.parallax').parallax();
        $(".dropdown-trigger").dropdown();
        $('select').formSelect();
        $('.tabs').tabs();
        $('.datepicker').datepicker({
            format: 'dd/mm/yyyy'
        });
    }); // end of document ready
})(jQuery); // end of jQuery name space
