// api를 테스트하기위해서 통신이 필요하고 Mock 서버인 json server로 실습
// npm install -g json-server
// json-server --watch db.json --port 3000

$(document).ready(function(){
    loadUsers();

    // CREATE 행 추가  prompt
    $("#addBtn").on('click',function(){
        const name = prompt('이름 입력');
        const email = prompt('이메일 입력');
        if(!name || !email) return;        
        const user = {name, email}
        createUser(user);
    });
});

function loadUsers(){
    $.ajax({
        url:'http://localhost:3000/users', 
        method: 'GET',
        success:function(users){
            $('#userTable').empty();
            users.forEach(user => {
                $('#userTable').append(                     
                    `
                    <tr data-id="${user.id}">
                        <td><input type="checkbox" class="chk"></td>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>
                            <button class="edit">MODIFY</button>
                            <button class="remove">REMOVE</button>
                        </td>
                    </tr>
                    `                   
                )
            });
        },
        error:function(){
            alert('목록조회 실패');
        }
    });
}

// POST 사용자 추가
function createUser(data){
    $.ajax({
        url:'http://localhost:3000/users',
        method: 'POST',
        contentType : 'application/json',
        data : JSON.stringify(data),
        success:function(){
            alert('등록되었습니다.');
            loadUsers(); // 목록 갱신
        }
    });
}