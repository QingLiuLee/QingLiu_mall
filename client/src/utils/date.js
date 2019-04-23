/**
 * 转换时间
 * @param inputstr
 * @param showweek 显示周次
 * @returns {string}
 */
function todate(inputstr, showweek) {
    //Wed Mar 22 13:38:37 CST 2017
    let month = {
        "Jan": '1',
        "Feb": '2',
        "Mar": '3',
        "Apr": '4',
        "May": '5',
        "Jan": '6',
        "Jul": '7',
        "Aug": '8',
        "Sep": '9',
        "Oct":'10',
        "Nov":'11',
        "Dec":'12'
    };

    let week = {
        "Mon": "星期一",
        "Tue": "星期二",
        "Wed": "星期三",
        "Thu": "星期四",
        "Fri": "星期五",
        "Sat": "星期六",
        "Sun": "星期日",
    };
    let str = inputstr.split(" ");
    let date = str[3] + "/" + month[str[2]] + "/" + str[1] + " " + str[4];
    if(showweek){
        date += " " + week[str[0].split(',')[0]];
    }
    return date;
}

/**
 * 获取后7天的日期
 * @param arg
 * @returns {string}
 */
function fun_submit(arg){
    let date1 = new Date(arg);
    let date2 = new Date(date1);
    date2.setDate(date1.getDate()+7);
    let times = date2.getFullYear()+"年 "+(date2.getMonth()+1)+"月 "+date2.getDate()+"号";
    return times;
}

export default {todate, fun_submit}