window.onload = function() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })

    //Login form
    $('#showToggle').on("click", function(e){
        e.preventDefault();
        if($('#passInput').attr("type") == "text")
        {
            $('#passInput').attr('type','password');
            $('#showToggle i').removeClass('fa-eye');
            $('#showToggle i').addClass('fa-eye-slash');
        }
        else{
            $('#passInput').attr('type','text');
            $('#showToggle i').addClass('fa-eye');
            $('#showToggle i').removeClass('fa-eye-slash');
        }
    })

    //Registeration form
    $('#showToggle1').on("click", function(e){
        e.preventDefault();
        if($('#pass1Input').attr("type") == "text")
        {
            $('#pass1Input').attr('type','password');
            $('#showToggle1 i').removeClass('fa-eye');
            $('#showToggle1 i').addClass('fa-eye-slash');
        }
        else{
            $('#pass1Input').attr('type','text');
            $('#showToggle1 i').addClass('fa-eye');
            $('#showToggle1 i').removeClass('fa-eye-slash');
        }
    })

    $('#showToggle2').on("click", function(e){
        e.preventDefault();
        if($('#pass2Input').attr("type") == "text")
        {
            $('#pass2Input').attr('type','password');
            $('#showToggle2 i').removeClass('fa-eye');
            $('#showToggle2 i').addClass('fa-eye-slash');
        }
        else{
            $('#pass2Input').attr('type','text');
            $('#showToggle2 i').addClass('fa-eye');
            $('#showToggle2 i').removeClass('fa-eye-slash');
        }
    })
}

//Registeration Form Validation
$('#registerSubmit').on('click', function(e){
    e.preventDefault();
    first_name = $('#firstName').val();
    last_name = $('#lastName').val();
    email = $('#emailInput').val();
    pass1 = $('#pass1Input').val();
    pass2 = $('#pass2Input').val();
    gender = $("input[name='gender']:checked").val();
    dob = $('#datepicker').val();
    pic = $('#profilePic').val();

    if(first_name == '')
    {
        $('#firstName').addClass('is-invalid');
    }
    else{
        $('#firstName').removeClass('is-invalid');
    }
    if(last_name == '')
    {
        $('#lastName').addClass('is-invalid');
    }
    else{
        $('#lastName').removeClass('is-invalid');
    }
    if(email == '')
    {
        $('#emailInput').addClass('is-invalid');
    }
    else{
        $('#emailInput').removeClass('is-invalid');
    }
    if(pass1 == '')
    {
        $('#pass1Input').addClass('is-invalid');
    }
    else{
        $('#pass1Input').removeClass('is-invalid');
    }
    if(pass2 == '')
    {
        $('#pass2Input').addClass('is-invalid');
    }
    else{
        $('#pass2Input').removeClass('is-invalid');
    }
    if(!gender)
    {
        $('#genderHidden').addClass('is-invalid');
    }
    else{
        $('#genderHidden').removeClass('is-invalid');
    }
    if(dob == '')
    {
        $('#datepicker').addClass('is-invalid');
    }
    else{
        $('#datepicker').removeClass('is-invalid');
    }
    if(pic == '')
    {
        $('#profilePic').addClass('is-invalid');
    }
    else{
        $('#profilePic').removeClass('is-invalid');
    }

    if ( first_name && last_name && email && pass1 && pass2 && gender && dob && pic)
    {
        if( pass1 != pass2)
        {
            $('#errorMessage').removeClass('d-none');
            $('#errorMessage').html('Passwords do not match');
        }
        else{
            var formDataRaw = $('#registrationForm')[0];
            var form_data = new FormData(formDataRaw);
            $.ajax({
                type: 'POST',
                cache: false,
                data: form_data,
                dataType: 'json',
                url: '/register',
                contentType: false,
                processData: false,
                success: function(response) {
                    if (response.message == "success")
                    {
                        window.location.href = '/login'
                    }
                    else{
                        if ($('#errorMessage').hasClass('d-none')){
                            $('#errorMessage').removeClass('d-none');
                        }
                        $('#errorMessage').html(response.message);
                    }
                },
                error: function(error) {
                    if ($('#errorMessage').hasClass('d-none')){
                        $('#errorMessage').removeClass('d-none');
                    }
                    $('#errorMessage').html(error.message);
                }
            });
        }
    }
})

//Login Form Validation
$('#loginSubmit').on('click',function(e){
    e.preventDefault();
    if( $('.login_form #emailInput').val() == ''){
        $('.login_form #emailInput').addClass('is-invalid');
    }
    else{
        $('.login_form #emailInput').removeClass('is-invalid');
    }
    if( $('.login_form #passInput').val() == ''){
        $('.login_form #passInput').addClass('is-invalid');
    }
    else{
        $('.login_form #passInput').removeClass('is-invalid');
    }
    if ( ( $('.login_form #emailInput').val() != '') && ($('.login_form #passInput').val() != ''))
    {
        var formDataRaw = $('#loginForm')[0];
        var form_data = new FormData(formDataRaw);
        $.ajax({
            type: 'POST',
            cache: false,
            data: form_data,
            dataType: 'json',
            url: '/login',
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.message == "invalid login")
                {
                    if ($('#errorMessage').hasClass('d-none')){
                        $('#errorMessage').removeClass('d-none');
                    }
                    $('#errorMessage').html('Invalid login details');
                }
                else{
                    window.location.href = '/'
                }
            },
            error: function(error) {
                if ($('#errorMessage').hasClass('d-none')){
                    $('#errorMessage').removeClass('d-none');
                }
                $('#errorMessage').html(error.message);
            }
        });
    }
})

//Post Form Validation
$('#postButton').on('click', function(e){
    e.preventDefault();
    $('#successMessage').addClass('d-none');
    $('#errorMessage').addClass('d-none');
    if ( $('#postText').val() == '' && $("#postPhoto").val() == '')
    {
        if ($('#errorMessage').hasClass('d-none')){
            $('#errorMessage').removeClass('d-none');
        }
    } else {
        var formDataRaw = $('#postForm')[0];
        var form_data = new FormData(formDataRaw);
        $.ajax({
            type: 'POST',
            cache: false,
            data: form_data,
            dataType: 'json',
            url: '/post',
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.message == 'success')
                {
                    $('#errorMessage').addClass('d-none')
                    $('#successMessage').removeClass('d-none');
                    $('#postPhoto').val('');
                    $('#postText').val(''); 
                    $.ajax({
                        url: "/get_posts",
                        success: function(response) {
                          $("#posts").html(response);
                        },
                    });
                }
            },
            error: function(error) {
                if ($('#errorMessage').hasClass('d-none')){
                    $('#errorMessage').removeClass('d-none');
                }
                $('#errorMessage').html(error.message);
            }
        })   
    }
})

//Send Request
$('.sendRequest').on('click', function() {
    if ($(this).hasClass('btn-success'))
    {
        btn = $(this);
        friend_id = $(this).parent().find('input').val();
        $.post("/sent_request", {friend_id:friend_id},
        function(response, status){
            if (status=='success')
            {
                btn.parent().parent().parent().parent().fadeOut();
            }
        });
    }
})

//Cancel Request
$('.cancelRequest').on('click', function() {
    btn = $(this);
    request_id = $(this).parent().find('input').val();
    $.post("/cancel_request", {request_id:request_id},
    function(response, status){
        if (status=='success')
        {
            btn.parent().parent().parent().parent().fadeOut();
        }
    });
})

//Delete Request
$('.deleteRequest').on('click', function() {
    btn = $(this);
    request_id = $(this).parent().find('input').val();
    $.post("/remove_request", {request_id:request_id},
    function(response, status){
        if (status=='success')
        {
            btn.parent().parent().parent().parent().fadeOut();
        }
    });
})

//Confirm Request
$('.confRequest').on('click', function(){
    btn = $(this);
    request_id = $(this).parent().find('input').val();
    $.post("/accept_request", {request_id:request_id},
    function(response, status){
        if (status=='success')
        {
            btn.parent().parent().parent().parent().fadeOut();
        }
    });
})

//Remove Friend
$('.unfriend').on('click', function(){
    btn = $(this);
    friend_id = $(this).parent().find('input').val();
    $.post("/remove_friend", {friend_id:friend_id},
    function(response, status){
        if (status=='success')
        {
            btn.parent().parent().parent().parent().fadeOut();
            var count = document.getElementById('friendsCount').innerHTML;
            count = parseInt(count);
            count -= 1;
            document.getElementById('friendsCount').innerHTML = "" + count + "";
        }
    });
})

//Delete Post
$('.deletePost').on('click', function() {
    btn = $(this);
    post_id = $(this).parent().find('input').val();
    $.post("/delete_post", {post_id:post_id},
    function(response, status){
        if (status=='success')
        {
            btn.parent().parent().parent().parent().fadeOut();
        }
    });
})

//Like Button
$('.likePost').on('click', function() {
    btn = $(this)
    var count = btn.find('.likesCount').html();
    count = parseInt(count);
    if (btn.find('i').hasClass('far'))
    {
        post_id = btn.parent().find('input').val();
        $.post("/like_post", {post_id:post_id},
        function(response, status){
            if (status=='success')
            {
                btn.find('i').removeClass('far');
                btn.find('i').addClass('fas');
                count += 1;
                btn.find('.likesCount').html(count);
            }
        });
    } else {
        post_id = btn.parent().find('input').val();
        $.post("/unlike_post", {post_id:post_id},
        function(response, status){
            if (status=='success')
            {
                btn.find('i').addClass('far');
                btn.find('i').removeClass('fas');
                count -= 1;
                btn.find('.likesCount').html(count);
            }
        });
    }
})