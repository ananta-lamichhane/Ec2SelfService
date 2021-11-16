$(document).ready(function(){
    var item_no=1 //keep track of how many elements are already displayed reset of each complete reload of the page.
    $('form').on('submit', function(event){ //sends POST request without refreshing the page.
    event.preventDefault();

        var name =  $('#instanceName').val(); // extract values from the form data
        var type = $('#instanceType').val();
        var keypair = $('#keyPair').val();

        $.ajax({
            data: { //send back to backend (flask)
                instance_name: name, // rating from the rating slider
                instance_type: type, //current imdb id so that we can calculate next
                key_pair: keypair, //we want to distinguish between submission of ratings and other forms
            },
            url: '/',
            type: 'POST'
        })
        .done(function(data){ //when post request was successful do the following
            window.location = '/';
            console.log("submitted form")
            console.log("name= "+name +" , type= "+type +", keypair=  "+keypair )

        });

      //prevent form being submitted automatically after pressing submit
    });

});