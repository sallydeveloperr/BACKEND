// api를 테스트하기위해서 통신이 필요하고 Mock 서버인 json server로 실습
// json 서버용 directory를 만들고 해당 directory로 이동해서
// db.json파일을 생성하고 -- DB
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
 // 업데이트(update)
    $("#userTable").on('click','.edit',function(){
        const name = prompt('수정할 이름');
        const email = prompt('수정할 이메일');
        const id = $(this).closest('tr').data('id');
        data = {'name':name, 'email':email}
        updateUser(id,data)
    });    
    // 삭제 : 단일 행   테이블의 데이터는 동적으로 생성했기때문에 이벤트를 직접 발생시키지 못하고 위임해야 한다
    $("#userTable").on('click','.remove',function(){
        const id = $(this).closest('tr').data('id')   // 태그 안에 있는 어트리뷰트(attr) data-id
        users = users.filter(u => u.id != id)
        renderTable()
    });
    // 삭제 버튼(selected checkbox)  다중 삭제

});

function updateUser(id,data){
    $.ajax({
        url:`http://localhost:3000/users/${id}`,
        method : 'PUT',
        contentType : 'application/json',
        data : JSON.stringify(data),
        success:function(){
            alert('수정되었습니다.');
            loadUsers(); // 목록 갱신
        }
    });
}


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