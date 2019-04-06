url="http://127.0.0.1:8000/api/v1/online_user_live_listenings/"
const app = document.getElementById('currently_listening');
const container = document.createElement('ul');
container.setAttribute('style', 'width:200px;display:inline');
container.innerHTML=''
$.ajax({
    url: url,
    dataType: 'application/json',
    complete: function (data) {
        console.log(data)
        json = JSON.parse(data["responseText"]);
                    (json['results']).forEach(data => {
                        user_id= data.user_id
                        track_name= data.track_name

                        container.innerHTML =
                            container.innerHTML +
                            '<li href="'+user_id+'">' +
                            '<em style="font-size: 20px">'+track_name +'</em>'+
                            '</li>'
                        console.log(container)
                        app.appendChild(container)



                    });
    },
});


