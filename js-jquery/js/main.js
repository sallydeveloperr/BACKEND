console.log('js 연결확인')

//  dom - html전체 구조를 객체화 한것
$(document).ready(
    function(){
        console.log('jquery 준비완료');

        $("#btn").click(function(){
            $('#text').text('버튼 클릭됨');        
        })
    }   
);