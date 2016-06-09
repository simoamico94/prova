$(document).ready( function() {

    // this code will be executed only the DOM is fully loaded

    $('form#login').submit( function(event) {
        // validate the login form

        $('div#errorbox').empty() ;
        var text_username = $("input[name='username']").val() ;
        var text_password = $("input[name='password']").val() ;
        if(text_username.length < 1 || text_password.length < 1) {
            $('div#errorbox').text("Error. Please insert username and password in a correct way.").addClass("text-danger") ;
            $("input[name='username']").parent().addClass("has-error") ;
            $("input[name='password']").parent().addClass("has-error") ;
            window.setTimeout( function() {
                $("input[name='username']").parent().removeClass("has-error") ;
                $("input[name='password']").parent().removeClass("has-error") ;
            } , 5000) ;
            event.preventDefault() ;
        }
    } ) ;

    $('form#create-account').submit(function (event) {
        // validate the create-account form

        $('div#errorpopup').empty() ;
        var text_username = $("input[name='username']").val() ;
        var text_password = $("input[name='password']").val() ;
        var text_name = $("input[name='name']").val() ;
        var text_surname = $("input[name='surname']").val() ;
        var text_data = $("input[name='bornDate']").val() ;

        if(text_username.length < 1 || text_password.length < 1 || text_name.length < 1 || text_surname.length < 1 || text_data.length < 1) {
            $('div#errorpopup').text("Error. Please insert the information in a correct way.").addClass("text-danger") ;
            $("input[name='username']").parent().addClass("has-error") ;
            $("input[name='password']").parent().addClass("has-error") ;
            $("input[name='name']").parent().addClass("has-error") ;
            $("input[name='surname']").parent().addClass("has-error") ;
            $("input[name='bornDate']").parent().addClass("has-error") ;

            window.setTimeout( function() {
                $("input[name='username']").parent().removeClass("has-error") ;
                $("input[name='password']").parent().removeClass("has-error") ;
                $("input[name='name']").parent().removeClass("has-error") ;
                $("input[name='surname']").parent().removeClass("has-error") ;
                $("input[name='bornDate']").parent().removeClass("has-error") ;
            } , 5000) ;
            event.preventDefault() ;
        }
    })
} ) ;