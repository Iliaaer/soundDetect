// fetch('https://run.mocky.io/v3/8d049103-893c-497b-b273-6d8301e89140') //allnames
fetch('http://127.0.0.1:8000/audiofiles/allname?device_type=local') //allnames
    .then(function (response) {
        return response.json()
    })
    .then(function (data) {
        for (let i = 0; i < data.result.length; i++){
            let div = document.createElement('div');
            div.className = 'alert';
            div.innerHTML = "<div id='audio'><p>"+data.result[i].name+"</p><p>"+data.result[i].date+"</p><p>"+data.result[i].already+"</p><input type='button' id="+data.result[i].name+" value='Показать текст'></div>";
            document.body.append(div);
        }
        buttons = document.querySelectorAll('input');
        buttons.forEach(btn=>{
            addEventListener('click', f);
        })
        function f(e){
            console.log(e.target.id);
            // fetch('https://run.mocky.io/v3/d4d03e14-e11a-4720-a651-9275e0e82654') // get text
            // fetch("http://127.0.0.1:8000/audiofiles/download?filename="+e.target.id) // to filename
            fetch("http://127.0.0.1:8000/audiofiles/resultfile?filename="+e.target.id) // to filename            
                .then(function(response){
                    return response.json()
                })
                .then(function(data){
                    console.log(data.result.data)
                })
        }
    })

