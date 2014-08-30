$(document).ready(function(){

    setInterval(refresh_cpu, 2000);
    setInterval(refresh_ram, 10000);
    setInterval(refresh_uptime, 1000);
    setInterval(refresh_network, 10000);
    setInterval(refresh_processes, 15000);
    setInterval(refresh_disks, 60000);

    $('#refresh-disks').click(function () {
        refresh_disks();
    });

    $('#refresh-process').click(function () {
        refresh_processes();
    });

    $('#refresh-cpu').click(function () {
        refresh_cpu();
    });

    $('#refresh-ram').click(function () {
        refresh_ram();
    });

    $('#refresh-network').click(function () {
        refresh_network();
    });

    $('#refresh-uptime').click(function () {
        refresh_uptime();
    });
});

function get_progress_bar_color_class(percentage) {
    var bar_class;
    percentage = percentage.substring(0, percentage.length - 1);
    if (percentage > 90) {
        bar_class = "progress-bar progress-bar-danger";
    } else if (percentage > 70) {
        bar_class = "progress-bar progress-bar-warning";
    } else {
        bar_class = "progress-bar progress-bar-success";
    }
    return bar_class;
}

function refresh_cpu(){
    var api_call = "/api/cpu/usage";
    $.ajax({
        url: api_call
    }).done(function (data) {
        $('#cpu_usage').text(data.cpu_usage);
        $('#cpu_usage_bar').attr('class', get_progress_bar_color_class(data.cpu_usage))
            .css({'width': data.cpu_usage});
    });
}

function refresh_ram(){
    var api_call = "/api/ram/usage";
    $.ajax({
        url: api_call
    }).done(function (data) {
        $('#ram_usage').text(data.ram_usage);
        $('#ram_usage_bar').attr('class', get_progress_bar_color_class(data.ram_usage))
            .css({'width': data.ram_usage});
    });
}

function refresh_uptime(){
    var api_call = "/api/uptime";
    $.ajax({
        url: api_call
    }).done(function (data) {
        $('#uptime').text(data.uptime);
    });
}

function refresh_disks(){
    var api_call = "/api/disks/";
    $.ajax({
        url: api_call
    }).done(function (data) {
        var count = 1;
        for(var disk in data){
            var disk_data = data[disk];

            $('#disk-name' + count).text(disk);
            $('#disk-capacity' + count).text(disk_data.capacity);
            $('#disk-free' + count).text(disk_data.free);
            $('#disk-used' + count).text(disk_data.used);
            $('#disk-bar' + count).attr('class', get_progress_bar_color_class(disk_data.percent))
                .css({'width': disk_data.percent});

            count += 1;
        }
    });
}

function refresh_network(){
    var api_call = "/api/network/";
    $.ajax({
        url: api_call
    }).done(function (data) {
        $('#network-download').text(data.download);
        $('#network-upload').text(data.upload);
    });
}

function refresh_processes(){

    function get_row_class_name(cpu_percent, ram_percent){
        cpu_percent = cpu_percent.substring(0, cpu_percent.length - 1);
        ram_percent = ram_percent.substring(0, ram_percent.length - 1);

        var max_percent = Math.max(cpu_percent, ram_percent);

        var row_class = "";
        if (max_percent >= 90) {
            row_class = "danger";
        } else if (max_percent >= 70) {
            row_class = "warning";
        }
        return row_class;
    }

    var api_call = "/api/process/";
    $.ajax({
        url: api_call
    }).done(function (data) {
        $('#processes').html("<tr><th>Name</th><th>PID</th><th>CPU Usage</th><th>RAM Usage</th></tr>");
        for(var process in data){
            process = data[process];
            var name_col = '<td>' + process.name + '</td>';
            var pid_col = '<td>' + process.pid + '</td>';
            var cpu_col = '<td>' + process.cpu_usage + '</td>';
            var ram_col = '<td>' + process.ram_usage + '</td>';
            $('#processes').append('<tr class="' + get_row_class_name(process.cpu_usage, process.ram_usage) +
                '">' + name_col + pid_col + cpu_col + ram_col + '</tr>');
        }
    });
}