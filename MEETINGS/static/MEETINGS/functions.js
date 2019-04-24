/* Handles AJAX calls  */

$(document).ready(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    //DETAIL
    var $shareForm = $('.share_ajax')
    $shareForm.submit(function(event){
        event.preventDefault()
        data = {
                form : $(this).serializeObject(),
                name : $(this).attr('name')
            };


        $.ajax({

            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            method: "POST",
            url: $(this).attr('action'),
            data: JSON.stringify(data),


            success: function(response) {
                 if(response['success']) {
                     $("#results").html("<div class='alert alert-success'>Invitations sent successfully!</div>");
                     $shareForm[0].reset();
                 }

                 if(response['error']) {
                     $("#results").html("<div class='alert alert-danger'>" + response['error']['emails'] +"</div>");
                 }
            },

            error: function(xhr, textStatus, error) {
                console.log(xhr, error, textStatus);
            }
        })
    })

    var $leaveForm = $('.leave_ajax')
    $leaveForm.submit(function(event){
        event.preventDefault()
        data = {
                form : $(this).serializeObject(),
                name : $(this).attr('name')
            };

        

        $.ajax({

            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            method: "POST",
            url: $(this).attr('action'),
            data: JSON.stringify(data),


            success: function(response) {

                 if(response['select']) {
                    $('#close_select_org').on('click', function() {
                        $("#select_form").hide();  
                    });
                    $('#select_form').show();
                    $('html, body').animate({ scrollTop: $('#select_form').offset().top }, 'slow');
                 }else{
                    $('#close_alert').on('click', function() {
                        $("#leave_error").hide();  
                    });
                    $("#leave_error").show();
                    $('html, body').animate({ scrollTop: $('#leave_error').offset().top }, 'slow');
                 }

            },

            error: function(xhr, textStatus, error) {
                console.log(xhr, error, textStatus);
            }
        })
    })

    
    //SEARCH
    $(document).on("keyup", "#search_ajax", function() {

        /*data = {
                name : $('#search_ajax').name,
                //search_text : $('#search_ajax').val()
            };*/

        $.ajax({

            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            method: "GET",
            url: $(this).attr('action'),
            data: {
                name : 'myquery',
                search_text : $('#search_ajax').val()
            },


            success: function(data, textStatus, jqHXR) {

                var $result = $('<div />').append(data).find('#search_results').html();
                $("#search_results").html($result);

            },

            error: function(xhr, textStatus, error) {
                console.log(xhr, error, textStatus);
            }

        });

    });

    $(document).on("click", "#search_filters_btn", function() {

        var x = document.getElementById("filter_options");

        if (x.style.display === "none") {
            x.style.display = "block";
            $("#search_filters_btn").text("Hide");
        } else {
            x.style.display = "none";
            $("#search_filters_btn").text("Add Filters");
        }

    });

    var $filterForm = $('.filter_options')
    $filterForm.submit(function(event){
        event.preventDefault()
        
        $.ajax({

            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            method: "GET",
            data: {
                name : $(this).attr('name'),
                form : JSON.stringify($(this).serializeObject())

            },


            success: function(data) {

                var $result = $('<div />').append(data).find('#search_results').html();
                $("#search_results").html($result);

            },

            error: function(xhr, textStatus, error) {
                console.log(xhr, error, textStatus);
            }
        })
    })
    

    //CALENDAR 
    $(document).on("click", "#prev_btn", function() {

        event.preventDefault()
        $prevUrl = $(this).attr('href')

        $.ajax({

            url: $prevUrl,

            success: function (data) {

                var $result = $('<div />').append(data).find('#cal_row').html();
                $("#cal_row").html($result);
            }

         })
    })

    $(document).on("click", "#next_btn", function() {

        event.preventDefault()
        $prevUrl = $(this).attr('href')

        $.ajax({

            url: $prevUrl,

            success: function (data) {

                var $result = $('<div />').append(data).find('#cal_row').html();
                $("#cal_row").html($result);
            }

         })
    })

})

