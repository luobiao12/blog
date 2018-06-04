/**
 * Created by 59321 on 2018/4/13.
 */

   $(".login_btn").on("click", function () {

        $.ajax({
            url: "",
            type: "post",
            data: {
                user: $("#user").val(),
                pwd: $("#pwd").val(),
                valid_code: $("#valid_code").val()
            },
            success: function (data) {
                console.log(data);
                if (data.state) {
                    location.href = "/index/"
                }
                else {
                    $(".error").text(data.msg)
                }
            }
        })

    });
    $('#valid_img').on('click',function () {
        $(this)[0].src+='?'
    });
