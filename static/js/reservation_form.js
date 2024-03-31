$(document).ready(function() {
    $('#id_room_type').change(function() {
        var roomType = $(this).val();
        $.ajax({
            url: '/reception/fetch_rooms/',
            data: {
                'room_type': roomType
            },
            success: function(data) {
                var roomSelect = $('#id_room');
                roomSelect.empty();
                $.each(data.rooms, function(index, room) {
                    roomSelect.append($('<option></option>').attr('value', room.id).text(room.room_num));
                });
            }
        });
    });
});

function goBack() {
    window.history.back();
}