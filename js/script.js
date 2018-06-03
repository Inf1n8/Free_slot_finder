console.log('loaded');

function submitDet() {
    let imageFile = document.getElementById('imageFile');
    let name = $('#name').val();
    let regNo = $('#regNo').val();
    if (imageFile.files[0].type === 'image/png') {
        console.log(name, regNo, imageFile.files[0], imageFile.files[0].type);
        let formData = new FormData();
        formData.append('name', name);
        formData.append('regNo', regNo);
        formData.append('timetable', imageFile.files[0]);
        $.ajax({
            url: "http://127.0.0.1:5000/upload",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function (data) {
                console.log(data);
                alert(data);
            }
        })
    }
    else {
        alert('Please upload a PNG file');
    }
}

var tabId=[];
var day='';

function removetabId(ele){
    console.log(ele);
    var index= tabId.indexOf(parseInt(ele,10));
    console.log(index);
    tabId.splice(index,1);
    console.log(tabId);
    if(!tabId.length){day='';}
}

function pushtabId(ele,dayDet){
    tabId.push(parseInt(ele,10));
    console.log(tabId);
    if(tabId.length){day=dayDet}
}

$('td').on('click', function(){
    var ele=$(this).attr('tabId');
    if($(this).hasClass('tdSelected')){
        console.log(ele);
        removetabId(ele);
    }
    else{
        pushtabId(ele,$(this).parent().attr('id'));
    }
    $(this).toggleClass('tdSelected');
    console.log($(this).attr('tabId'), $(this).parent().attr('id'));
});

function findMembers()
{
    var data={day,tabId};
    console.log(data);
    $.ajax({
        url:'http://127.0.0.1:5000/findMembers',
        data: JSON.stringify(data),
        cache: false,
        processData: false,
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function (data) {
            console.log(data);
        }

    })
}