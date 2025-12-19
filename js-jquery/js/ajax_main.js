$(document).ready(function(){
    loadUsers();
});

function loadUsers(){
    $.ajax({
        url:'/api/users',
        method: 'GET',
        success:function(users){
            $('#userTable').empty();
        },
        error:function(){}
    });
}