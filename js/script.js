console.log('loaded');
function submitDet() {
    let imageFile = document.getElementById('imageFile');
    let name = $('#name').val();
    let regNo = $('#regNo').val();
    if(imageFile.files[0].type === 'image/png')
    {
        console.log(name,regNo,imageFile.files[0],imageFile.files[0].type);
        let formData= new FormData();
        formData.append('name',name);
        formData.append('regNo',regNo);
        formData.append('timetable',imageFile.files[0]);
        $.ajax({
            url:"http://127.0.0.1:5000/upload",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data) {
                console.log(data);
                alert(data);
            }
        })
    }
    else
    {
        alert('Please upload a PNG file');
    }
}
