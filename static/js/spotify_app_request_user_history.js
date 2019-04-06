

user_id=document.currentScript.getAttribute('user_id')
url="http://127.0.0.1:8000/api/v1/admin_user_track_history/" + user_id

//console.log(d.getDate())
//console.log(d.getDate())

var d = new Date();

$.ajax({
    url: url,
    dataType: 'application/json',
    complete: function (data) {
        console.log(data)
        json = JSON.parse(data["responseText"]);
                    (json['results']).forEach(song => {
                        track_name = song.track_name;
                        timestamp= song.timestamp;
                        var momentDateObj = moment(timestamp);
                        var d = new Date();

                        const container = document.createElement('ul');


                        for (i = 0; i < 7; i++)
                        {
                          const app = document.getElementById('day_' + i );
                          if(momentDateObj.date() == d.getDate()- i)
                          {
                                const container = document.createElement('li');
                                container.setAttribute('class', 'single-event');
                                container.setAttribute('data-start', momentDateObj.hour() + ':' + momentDateObj.minutes());
                                container.setAttribute('data-end', momentDateObj.hour() + ':' + (momentDateObj.minutes()+10));
                                container.setAttribute('data-content', 'event-yoga-1');
                                container.setAttribute('data-event', 'event-3');
                                container.setAttribute('style', 'top:'+ (momentDateObj.hour()*30 + momentDateObj.minutes() *1 )   +'px; height:'+12 +'px;font-size:15px;');
                                container.innerHTML =
                                    '<a href="#0">' +
                                    '<em class="event-name" style="font-size: 10px">'+track_name +'</em>'+
                                    '</a>'
                                app.appendChild(container)
                          }
                          else {

                          }

                        }
                        //console.log(track_name)
                        //console.log(timestamp)




                    });
    },
});


