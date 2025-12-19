console.log('js 연결확인')

//  dom - html 전체 구조를 객체화 한것
$(document).ready(
    function(){
        // 초기 랜더링 리스트업(READ)
        let users = [
            {id:1, name:'홍길동',email:'hong@test.com'},
            {id:2, name:'김철수',email:'kim@test.com'},
        ]
        // for user in users:
        // user     
        function renderTable(){
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
                    `            )
            });
        }

        renderTable();

        // 전체 선택 해제
        $("#checkall").on('change',function(){
            $(".chk").prop('checked',this.checked)            
        });

        // 동적생성한 요소는 이벤트위임으로 부모에게 이벤트를 위임해서 처리
        $("#userTable").on('change', '.chk', function(){            
            $("#checkall").prop('checked', 
                $(".chk").length == $(".chk:checked").length
            )
        });

        // CREATE 행 추가  prompt
        $("#addBtn").on('click',function(){
            const name = prompt('이름 입력');
            const email = prompt('이메일 입력');
            if(!name || !email) return;
            const newId = users.length? users[users.length-1].id+1 : 1 ; // javascrip or java or c++ or c# 등등            
            users.push({id:newId, name, email})
            renderTable();
        });    

        // 삭제 : 단일 행   테이블의 데이터는 동적으로 생성했기때문에 이벤트를 직접 발생시키지 못하고 위임해야 한다
        $("#userTable").on('click','.remove',function(){
            const id = $(this).closest('tr').data('id')   // 태그 안에 있는 어트리뷰트(attr) data-id
            users = users.filter(u => u.id != id)
            renderTable()
        });

        // 다중 선택 삭제( remove 확장)
        $("#deleteBtn").on('click',function(){
            const ids = []
            $('.chk:checked').each(function(){
                ids.push( $(this).closest('tr').data('id')  )
            });
            users = users.filter(u=> !ids.includes(u.id))
            renderTable();
        });

        // 업데이트(update)
        $('.edit').on('click',function(){
            const name = prompt('수정할 이름');
            const email = prompt('수정할 이메일');
            const idx = $(this).closest('tr').data('id')-1;
            const user = users[idx];
            user.name = name;
            user.email = email;
            renderTable();        
        });
    }   
);