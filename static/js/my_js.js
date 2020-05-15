VANTA.DOTS({
    el: "#vantajs",
    mouseControls: true,
    touchControls: true,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00
  })



$(document).on('submit', "#img_form" , function(e){
    e.preventDefault();
    var data = new FormData($('form').get(0));
    $.ajax({
        url: "",
        type : "POST",
        data : data,
        cache: false,
        contentType: false,
        processData: false,
        success : function(json){
            console.log(json);
            document.getElementById("result").innerHTML = json.result;
        },
        failure : function(data){
            alert("Error Occured");
        },
    
    });
});
