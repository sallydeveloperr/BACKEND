$(document).ready(function(){
    // 데이터 로드
    read_todos();

    $('#todoForm').on('submit',function(e){
        e.preventDefault()
        addTodo();        
    });
});

function addTodo(){
    const title = $('#todoTitle').val().trim();
    const description = $('#todoDescription').val().trim();
    const todoData = {
        title:title,
        description : description || null
    }
    $.ajax({
        url : 'http://localhost:8000/api/todos',
        method:'POST',
        data:JSON.stringify(todoData),
        contentType:'application/json',
        success:function(newTodo){
            console.log('추가 성공', newTodo)
            read_todos();  // 추가한 목록을 갱신
        },
        error:function(error){
            console.log('추가 실패', error)
        }
    });
}

function read_todos(){
    $.ajax({
        url:'http://localhost:8000/api/todos',
        method:'GET',
        success:function(todos){
            const $todolists = $('todoList')  //태그를 객체로 가져올때 변수명 앞에 $붙인다
            $todolists.empty();
            todos.forEach(function(todo){

                const $todoItem = `
                <div data-id = "${todo.id}">
                    <h3>${todo.title}</h3>
                    <p>${todo.description}</p>
                    <p>${todo.completed}</p>
                    <p>${todo.created_at}</p>
                </div>
                `
                $todolists.append($todoItem)
            });


        },
        error:function(error){
            console.log('읽기 실패', error);
        }
    })
}