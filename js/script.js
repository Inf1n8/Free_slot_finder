console.log('loaded');

$(document).ready(function () {
    console.log('ready');

});
document.body.addEventListener('click', function (e) {
    e.target.update && e.target.update();
});

if (!window.customElements || !document.head.attachShadow) {
    document.querySelector('html').className += ' oldie'
}

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
                window.location.reload();
            }
        })
    }
    else {
        alert('Please upload a PNG file');
    }
}

var tabId = [];
var day = '';

function removetabId(ele) {
    console.log(ele);
    var index = tabId.indexOf(parseInt(ele, 10));
    console.log(index);
    tabId.splice(index, 1);
    console.log(tabId);
    if (!tabId.length) {
        day = '';
    }
}

function pushtabId(ele, dayDet) {
    tabId.push(parseInt(ele, 10));
    console.log(tabId);
    if (tabId.length) {
        day = dayDet
    }
}

$('td').on('click', function () {
    var ele = $(this).attr('tabId');
    if ($(this).hasClass('tdSelected')) {
        console.log(ele);
        removetabId(ele);
    }
    else {
        pushtabId(ele, $(this).parent().attr('id'));
    }
    $(this).toggleClass('tdSelected');
    console.log($(this).attr('tabId'), $(this).parent().attr('id'));
});

function findMembers() {
    var data = {day, tabId};
    console.log(data);
    $.ajax({
        url: 'http://127.0.0.1:5000/findMembers',
        data: JSON.stringify(data),
        cache: false,
        processData: false,
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function (data) {
            listMembers(data);
        }

    })
}

function searchMember() {
    var name = $('#memberName').val();
    var day = $('#days').val();
    var data = {name, day};
    $.ajax({
        url: 'http://127.0.0.1:5000/searchMember',
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
var nameDetails;
function setColor(name)
{
    $('td').removeClass('available');
    console.log(name);
    const index=nameDetails.findIndex((ele)=>  ele.name.toUpperCase()=== name  );
    console.log(index);
    let cno=nameDetails[index].timings.container_nos;
    cno.forEach(e=>{
        console.log(e);
        $(`td[tabId='${e}']`).addClass('available')
    });
}

function listMembers(data) {
    console.log(data);
    nameDetails=data;
    var t = '<ul class="collapsible">';
    data.map(ele => {
        let timings = '<ul>';
        ele["timings"]["time_slots"].forEach(e => {
            timings += `<li>${e}</li>`;
        });
        timings += '</ul>';
        t += `<li class="names" onclick="setColor(event.target.textContent)">
      <div class="collapsible-header">${ele["name"].toUpperCase()}</div>
      <div class="collapsible-body"><span><h6><b>Free hours: ${ele["free_hrs"]}</b></h6><h6><b>Free Timings</b></h6> ${timings}</span></div>
    </li>`
    });
    t += '</ul>';
    $(".nameList").html(t);
    $(".nameList").css({"display":"block","align-self":"center"});
    $('.collapsible').collapsible();

}


//
// <div class="card">
//     <div class="card-content">
//     <span class="card-title">${ele["name"].toUpperCase()}</span>
//     <h6><b>Free hours: ${ele["free_hrs"]}</b></h6>
// <h6><b>Free Timings</b></h6>
// ${timings}
// </div>
// </div>