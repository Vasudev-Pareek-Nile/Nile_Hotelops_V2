AddFollowTask = function () {
    var t = $("[name='I']").val();
    $("#FollowTaskModel [name='Responsibility']").empty(),
        $("#FollowTaskModel [name='ResponsibilityUserID']").val(""),
        $("#FollowTaskModel [name='ro']").val($("[name='I'].srI").val()),
        $("#FollowTaskModel [name='Responsibility']").removeAttr("readonly"),
        $("#FollowTaskModel [name='I']").val(t),
        $("#FollowTaskModel [name='FollowUpDate']").val(""),
        $("#FollowTaskModel [name='ActionDate']").val(""),
        $("#FollowTaskModel [name='Task']").val(""),
        $("#FollowTaskModel [name='Header']").val(""),
        $("#FollowTaskModel [name='priority']").val(""),
        $("#FollowTaskModel [name='TaskUpdate']").val(""),
        $("#FollowTaskModel [name='Status']").val("Pending"),
        $("#FollowTaskModel [name='FollowUpID']").val(0),
        $(".datepicker").datepicker({ format: "dd-MM-yy" }),
        $("#FollowTaskModel").modal("show"),
        BindUserAutoComplete();
}

BindUserAutoComplete = function () {
    var t = $("#FollowTaskModel [name='I']").find("option:selected").val();
    $.ajax({
        async: !1,
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: "/api/FollowUpsAPI/UserList?O=" + t,
        dataType: "json",
        success: function (t) {
            if (void 0 != t && null != t) {
                t = JSON.parse(t);
                try {
                    $("#FollowTaskModel [name='Responsibility']").empty(),
                        $("#FollowTaskModel [name='ResponsibilityUserID']").val(""),
                        $("#FollowTaskModel [name='Responsibility']").removeAttr("readonly"),
                        $("#FollowTaskModel [name='Responsibility']").append("<option value='' data-ResponsibilityID='0'  data-usertype='0' >Select</option>"),
                        $(t).each(function (t, e) {
                            $("#FollowTaskModel [name='Responsibility']").append(
                                "<option value='" + e.UserName + "' data-ResponsibilityID='" + e.UserID + "'  data-usertype='" + e.UserType + "' " + ("GM" == e.UserType ? "selected" : "") + " >" + e.FullName + "</option>"
                            );
                        }),
                        $("#FollowTaskModel [name='ResponsibilityUserID']").val($("#FollowTaskModel [name='Responsibility'] option:selected").data("responsibilityid"));
                } catch (e) { }
            }
        },
    });
}
