$(document).ready(function() { 
    $('#join_room_btn').click(function() {
        const roomnameVar = $(this).attr('room_name');
        $.get('/join_room/', {'room_name': roomnameVar}, 
            function(data){
                $('#body_block_content').html(data)
        })
    });

    $('#exit_room_btn').click(function() {
        $.get('/exit_room/',{},
            function(data){
                $('#body_block_content').html(data)
        })
    });

    

    $('.choose_monster_card').click(function() {
        const monsterIndexeVar = $(this).attr('monster_index');
        $.get('/choose_monster/', {'monster_index': monsterIndexeVar}, 
            function(data){
                $('#body_block_content').html(data);
        })
    });
});