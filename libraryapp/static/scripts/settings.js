
document.getElementById("change-password-button").addEventListener("click", function (){
    document.querySelector(".popup").style.display = "flex";
});

document.getElementById("close-popup-button").addEventListener("click", function (){
    document.querySelector(".popup").style.display = "none";
});

var lastTime = 0;
var counter = 0;
$('#update-password-form').on('submit', function(event){
    event.preventDefault();
    var now = new Date().getTime();
    if(now-lastTime > 50) {
        counter++;
        console.log(counter);
        $('#update-password-submit').prop('disabled', true);
        console.log("form submitted!")
        changePassword();
        $('#update-password-submit').prop('disabled', false);
    }
    lastTime = now;
});

function changePassword() {
    let current_password = document.getElementById("current-password").value;
    let new_password = document.getElementById("new-password").value;
     $.ajax({
                type: 'POST',
                dataType: 'json',
                url: "settings",
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    'action': 'personal-password',
                    'current-password': current_password,
                    'new-password': new_password,
                },
                success : function(response) {
                    $('#message').html(response.success).css('color', 'green');
                },
                error : function(response) {
                    console.log(response.responseJSON)
                    $('#message').html(response.responseJSON.error).css('color', 'red');
                }
            })
}

$('#new-password, #new-repeated-password').on('keyup', function () {
    if($('#new-repeated-password').val() != "") {
        if ($('#new-password').val() == $('#new-repeated-password').val()) {
            $('#message').html('');
        } else
            $('#message').html('Hasła nie są takie same!').css('color', 'red');
    }
});