/**
 * @author hui
 * @date 2019/6/19
 * @Description: 获取元素距离可视区域:顶部,左部的距离
*/
export const offset = (ele) => {
    var top = ele.offsetTop;
    var left = ele.offsetLeft;
    while (ele.offsetParent) {
        ele = ele.offsetParent;
        if (window.navigator.userAgent.indexOf('MSTE 8') > -1) {
            top += ele.offsetTop;
            left += ele.offsetLeft;
        } else {
            top += ele.offsetTop + ele.clientTop;
            left += ele.offsetLeft + ele.clientLeft;
        }
    }
    return {
        left: left,
        top: top
    };
};

/**
 * @author hui
 * @date 2019/6/19
 * @Description: 获取窗口：宽，高，内容宽，内容高，距离顶部高
*/
export const getSize = () => {
    let windowW, windowH, contentH, contentW, scrollT;
    windowH = window.innerHeight;
    windowW = window.innerWidth;
    scrollT = document.documentElement.scrollTop || document.body.scrollTop;
    contentH =
        document.documentElement.scrollHeight > document.body.scrollHeight
            ? document.documentElement.scrollHeight
            : document.body.scrollHeight;
    contentW =
        document.documentElement.scrollWidth > document.body.scrollWidth
            ? document.documentElement.scrollWidth
            : document.body.scrollWidth;
    return {windowW, windowH, contentH, contentW, scrollT};
};