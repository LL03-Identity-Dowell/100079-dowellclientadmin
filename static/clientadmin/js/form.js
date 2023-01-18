$('#createportfolio').click(function(e){
    e.preventDefault();
   var member1=$('#form-field-member').val();
   console.log(typeof(member1))
    $.ajax({
       type : "POST",
       url: "portfolioadd",
       data: {
        form:"portfolio1",
        member_type:$('#membertype').val(),
        member:JSON.stringify(member1),

        product:$('#form-field-product').val(),
        data_type:$('#form-field-data_type').val(),
        op_rights:$('#form-field-op_rights').val(),
        role:$('#form-field-role').val(),
        portfolio_name:$('#form-field-portfolio_name').val(),
        portfolio_code:$('#form-field-portfolio_code').val(),
        portfolio_spec:$('#form-field-portfolio_spec').val(),
        portfolio_u_code:$('#form-field-portfolio_u_code').val(),
        portfolio_det:$('#form-field-portfolio_det').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        dataType: "json",


        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
       success: function(data){
           $('#image-container').css("display", "none");
        $('#portfolio_output').html("");
        $("#portfolio_output").prepend('<div class="col-md-6">'+
            '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
                '<div class="col p-4 d-flex flex-column position-static">' +
                    '<h3  class="mb-auto" style="color:green;" align="center">' + data.resp + '</h3>' +

                '</div>' +
            '</div>' +
        '</div>'
        )
       },
       failure: function() {
        $('#output').html("Noo")
       }});});

$('#role1').on('submit', function(e){
e.preventDefault();
$.ajax({
    type : "POST",
    url: "addroles",
    data: {
    form:"role1",
    itemlevel1:$('#form-field-itemlevel1').val(),
    itemlevel2:$('#form-field-itemlevel2').val(),
    itemlevel3:$('#form-field-itemlevel3').val(),
    itemlevel4:$('#form-field-itemlevel4').val(),
    itemlevel5:$('#form-field-itemlevel5').val(),
    selectlayerforroles:$('#form-field-selectlayerforroles').val(),
    role_name:$('#form-field-role_name').val(),
    role_code:$('#form-field-role_code').val(),
    role_spec:$('#form-field-role_spec').val(),
    role_u_code:$('#form-field-role_u_code').val(),
    role_det:$('#form-field-role_det').val(),
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    // csrfmiddlewaretoken: '{{ csrf_token }}',
    dataType: "json",
    },
    beforeSend: function() {
    $('#image-container').css("display", "block");
  },
    success: function(data){
    $('#image-container').css("display", "none");
    $('#role_output').html("");
    $("#role_output").prepend('<div class="col-md-6">'+
        '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
            '<div class="col p-4 d-flex flex-column position-static">' +
                '<h3  class="mb-auto" style="color:green;" align="center">' + data.resp + '</h3>' +
            '</div>' +
        '</div>' +
    '</div>'
    )
    },
    failure: function() {
    $('#image-container').css("display", "none");
    $('#output').html("Noo")
    }});});

$('#level').on('submit', function(e){
e.preventDefault();
$.ajax({
    type : "POST",
    url: "addroles",
    data: {
    form:"role1",
    itemlevel1:$('#form-field-itemlevel1').val(),
    itemlevel2:$('#form-field-itemlevel2').val(),
    itemlevel3:$('#form-field-itemlevel3').val(),
    itemlevel4:$('#form-field-itemlevel4').val(),
    itemlevel5:$('#form-field-itemlevel5').val(),
    selectlayerforroles:$('#form-field-selectlayerforroles').val(),
    role_name:$('#form-field-role_name').val(),
    role_code:$('#form-field-role_code').val(),
    role_spec:$('#form-field-role_spec').val(),
    role_u_code:$('#form-field-role_u_code').val(),
    role_det:$('#form-field-role_det').val(),
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    // csrfmiddlewaretoken: '{{ csrf_token }}',
    dataType: "json",
    },
    beforeSend: function() {
    $('#image-container').css("display", "block");
  },
    success: function(data){
    $('#image-container').css("display", "none");
    $('#role_output').html("");
    $("#role_output").prepend('<div class="col-md-6">'+
        '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
            '<div class="col p-4 d-flex flex-column position-static">' +
                '<h3  class="mb-auto" style="color:green;" align="center">' + data.resp + '</h3>' +
            '</div>' +
        '</div>' +
    '</div>'
    )
    },
    failure: function() {
    $('#image-container').css("display", "none");
    $('#output').html("Noo")
    }});});
$('#team_member1').on('submit', function(e){
    e.preventDefault();

    $.ajax({
        type : "POST",
        url: "members",
        data: {
        form:"team_member1",
        type1:$('#type').val(),
        member_name:$('#form-field-member_name').val(),
        member_code:$('#form-field-member_code').val(),
        member_spec:$('#form-field-member_spec').val(),
        member_u_code:$('#form-field-member_u_code').val(),
        member_det:$('#form-field-member_det').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        dataType: "json",
        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
        success: function(data){
        $('#image-container').css("display", "none");
        $('#invitation_link_member').html("");
        $('#invitation_link_member').html(data.link)
        },
        failure: function() {
        $('#output').html("Noo")
        }});});

$('#guest_member1').on('submit', function(e){
    e.preventDefault();

    $.ajax({
        type : "POST",
        url: "members",
        data: {
        form:"guest_member1",
        type1:$('#type').val(),
        user_name:$('#form-field-user_name').val(),
        user_code:$('#form-field-user_code').val(),
        user_spec:$('#form-field-user_spec').val(),
        user_u_code:$('#form-field-user_u_code').val(),
        user_det:$('#form-field-user_det').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        dataType: "json",
        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
        success: function(data){
        $('#image-container').css("display", "none");
        $('#invitation_link_guest').html("");
        $('#invitation_link_guest').html(data.link)
        },
        failure: function() {
        $('#output').html("Noo")
        }});});

$('#lavinumber').on('submit', function(e){
    e.preventDefault();
    $.ajax({
        type : "POST",
        url: "members",
        data: {
        form:"lavimember",
        type1:$('#type').val(),
        public_name:$('#form-field-public_name').val(),
        autopublic:$('#form-field-autopublic').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',

        dataType: "json",
        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
        success: function(data){
        $('#image-container').css("display", "none");
        console.log(data)
        $('#invitation_link_public1').html("");
        $('#invitation_link_public2').html("");
        $('#invitation_link_public1').html(data.public_name);
        $('#invitation_link_public2').html(data.autopublic);
        },

        failure: function() {
        $('#output').html("Noo")
        }});});


$('#emailsent').on('submit', function(e){
    e.preventDefault();
    $.ajax({
        type : "POST",
        url: "invitemembers",
        data: {
        form:"temailsent",
        email:$('#form-field-emailmember').val(),
        link:$('#invitation_link_member').text(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',

        dataType: "json",
        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
        success: function(data){
        $('#image-container').css("display", "none");
        $('#msg').html("");
        $('#msg').html(data.msg);
        },

        failure: function() {
        $('#output').html("Noo")
        }});});
$('#gemailsent').on('submit', function(e){
    e.preventDefault();
    $.ajax({
        type : "POST",
        url: "invitemembers",
        data: {
        form:"gemailsent",
        email1:$('#form-field-emailuser').val(),
        link1:$('#invitation_link_guest').text(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        // csrfmiddlewaretoken: '{{ csrf_token }}',

        dataType: "json",
        },
        beforeSend: function() {
    $('#image-container').css("display", "block");
  },
        success: function(data){
        $('#image-container').css("display", "none");
        $('#msg1').html("");
        $('#msg1').html(data.msg);
        },

        failure: function() {
        $('#output').html("Noo")
        }});});