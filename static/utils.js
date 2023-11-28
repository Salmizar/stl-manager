var scrollInterval;
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