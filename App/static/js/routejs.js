$(document).ready(function(){
    
    count = 1
    count_sched = 1

    $("#location_stop").change(function(){

        var location_id = $(this).val();
        var location_name = $("#location_stop option:selected").text()
        
        $("#locations_group_select").append("<div class = 'location_check_option_wrap_"+count+" location_check_option_wrap' data-id = "+count+"><input class = 'location_check_option' name = 'locations' type = 'checkbox' value = '"+ location_id +"' checked>" + "<span>" + location_name + "</span></div>");
        count++;
    });

    $(".location_check_option_wrap").click(function(){
        location_id = $(this).attr("data-id");
        $(".location_check_option_wrap_" + location_id).remove();
    });

    $("#addSchedule").click(function(){
        
        var day = $("#day option:selected").val();
        var sched_hour = $("#sched_hour option:selected").val();
        var sched_min = $("#sched_min option:selected").val();

        $("#day_wrap").append("<div class = 'schedule_option schedule_option_"+count_sched+"'> <input type = 'text' name = 'sched_day_selected' value = '" + day + "' readonly></div>");
        $("#from_hour_wrap").append("<div class = 'schedule_option schedule_option_"+count_sched+"' > <input type = 'text' name = 'sched_hour_selected' value = '" + sched_hour + "' read-only></div>");
        $("#to_hour_wrap").append("<div class = 'schedule_option schedule_option_"+count_sched+"'> <input type = 'text' name = 'sched_min_selected' value = '" + sched_min + "' read-only></div>");

    });

});
