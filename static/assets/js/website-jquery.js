$(document).ready(function() { 
    $('#join_room_btn').click(function() {
        const roomnameVar = $(this).attr('room_name');
        $.get('/join_room/', {'room_name': roomnameVar}, 
            function(data){
                $('#show_uesr_in_room').html("You now in this room.");
                $('#join_room_btn').hide();
                $('#exit_room_btn').show();
        })
    });

    $('#exit_room_btn').click(function() {
        $.get('/exit_room/', undefined,
            function(data){
                $('#show_uesr_in_room').hide();
                $('#exit_room_btn').hide();
                $('#join_room_btn').show();

        })
    });

    

    $('.choose_monster_card').click(function() {
        // const usernameVar = $(this).attr('user_name');
        const monsterIndexeVar = $(this).attr('monster_index');
        $.get('/choose_monster/', {'monster_index': monsterIndexeVar}, 
            function(data){
                // $('#show_uesr_in_room').hide();
                // $('#exit_room_btn').hide();
                // $('#join_room_btn').show();

        })
        alert('Choose monster '+monsterIndexeVar);
    });
});