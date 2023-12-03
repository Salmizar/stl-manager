var scrollInterval;
var files2upload = [];
function scrollObj(obj, leftScroll, rightScroll, distance) {
    let obj2Scroll = document.getElementById(obj);
    clearInterval(scrollInterval);
    if (obj2Scroll) {
        let result = obj2Scroll.scrollLeft + distance;
        if (distance>0 && result+distance > (obj2Scroll.scrollWidth - obj2Scroll.clientWidth)) {
            result = obj2Scroll.scrollWidth - obj2Scroll.clientWidth;
        } else if (distance<0 && result+distance < 0) {
            result = 0;
        }
        scrollInterval = setInterval(() => {
            if (distance > 0 && Math.round(obj2Scroll.scrollLeft) < result || distance < 0 && Math.round(obj2Scroll.scrollLeft) > result) {
                obj2Scroll.scrollLeft = obj2Scroll.scrollLeft + ((distance>0)?2:-2);
            } else {
                clearInterval(scrollInterval);
            }
            let scrollBtn = document.getElementById(leftScroll);
            if (scrollBtn) {
                scrollBtn.style.display = ((obj2Scroll.scrollLeft > 0)?"block":"none")
            }
            scrollBtn = document.getElementById(rightScroll);
            if (scrollBtn) {
                scrollBtn.style.display = ((Math.round(obj2Scroll.scrollLeft + obj2Scroll.clientWidth) >= obj2Scroll.scrollWidth)?"none":"block")
            }
        }, 1);
    }
}
function selectThumb(thumb, objId, src) {
    document.getElementById(objId).src = src;
    Array.from(document.getElementsByClassName('thumbnail')).forEach(
        (elm) => {
            elm.classList.remove('selected');
        }
    )
    thumb.classList.add('selected');
}
function addFiles(e, folder_name) {
    document.getElementById('new_files').innerHTML = '';
    files2upload = [];
    Object.keys(e.currentTarget.files).forEach(key=>{
        let file = e.currentTarget.files[key];
        if (document.getElementById('title').value === '') {
            document.getElementById('title').value = file.name.substring(0,file.name.lastIndexOf('.'));
        }
        let id = Math.round(Math.random()*1000);
        files2upload.push({"id":'new'+id, "name":file.name, "extension":file.name.substring(file.name.lastIndexOf('.')+1)});
        let url = "/file?file_id=new"+id+"&file_name="+file.name+"&file_size="+Math.round(file.size/1024)+"&folder_name="+folder_name;
        setTimeout(() => {
            htmx.ajax('GET', url, {target:'#new_files', swap:'beforeend'});
        }, key*20);
    })
}
function prepareUpload(event) {
    event.target.classList.add('save_btn_disabled');
    let numberOfSTLFiles = 0;
    let files = '';
    files2upload.forEach((file) => {
        if (file.extension === "stl") {
            numberOfSTLFiles++;
        }
        if (document.getElementById("file"+file.id)) {
            files += ((files==='')?'':',') + file.name
        }
    });
    document.getElementById('newfiles2add').value = files;
    files = '';
    filesArray = document.getElementById('files2remove').value.split(',');
    for (let x = 0; x < filesArray.length; x++) {
        if (document.getElementById('file'+(x+1)) === null) {
            files += ((files==='')?'':',') + filesArray[x]
        } else if (filesArray[x].substring(filesArray[x].lastIndexOf('.')+1) === "stl") {
            numberOfSTLFiles++;
        }
    }
    document.getElementById('files2remove').value = files;
    if (numberOfSTLFiles > 0 ) {
        return true;
    }
    alert('You must have at least one STL file')
    return false;
}