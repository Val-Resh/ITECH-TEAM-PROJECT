$(document).ready(function() { 
    $('#join_room_btn').click(function() {
        const usernameVar = $(this).attr('user_name');
        const roomnameVar = $(this).attr('room_name');
        $.get('/join_room/', {'username': usernameVar, 'room_name': roomnameVar}, 
            function(data){
                $('#show_uesr_in_room').html("You now in this room.");
                $('#join_room_btn').hide();
                $('#exit_room_btn').show();
        })
        alert('Join Room '+usernameVar+'  '+roomnameVar);
    });

    $('#exit_room_btn').click(function() {
        const usernameVar = $(this).attr('user_name');
        const roomnameVar = $(this).attr('room_name');
        $.get('/exit_room/', {'username': usernameVar, 'room_name': roomnameVar}, 
            function(data){
                $('#show_uesr_in_room').hide();
                $('#exit_room_btn').hide();
                $('#join_room_btn').show();

        })
        alert('Exit room '+usernameVar+'  '+roomnameVar);
    });
});