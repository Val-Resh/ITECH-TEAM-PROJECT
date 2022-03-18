$(document).ready(function() {

    //Join Room
    $('#join_room_btn').click(function() {
        const roomnameVar = $(this).attr('room_name');
        $.get('/join_room/', {'room_name': roomnameVar}, 
            function(data){
                $('#body_block_content').html(data)
        })
    });


    //Exit Room
    $('#exit_room_btn').click(function() {
        $.get('/exit_room/',{},
            function(message){
                alert(message)
                location.href="/";
        })
    });

    
    //Choose Monster
    $('.choose_monster_card').click(function() {
        const monsterIndexeVar = $(this).attr('monster_index');
        $.get('/choose_monster/', {'monster_index': monsterIndexeVar},
            function(data){
                $('#body_block_content').html(data);
        })
    });


    //Buy Items
    $('.buy_item_card').click(function() {
        const itemIdVar = $(this).attr('item_id');
        $.get('/buy_item/', {'item_id': itemIdVar}, 
            function(message){
                alert(message)
        })
    });
});