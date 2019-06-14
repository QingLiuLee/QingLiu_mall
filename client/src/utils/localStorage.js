/**
 * 缓存
 * @param staff_code: 商铺管理员编码
 * @param auth_token : token
 */

const storge = window.localStorage;

// 设置
export function setLocalStorage (key, value){
    return storge.setItem(key, value)
}

// 获取
export function getLocalStorage (key){
    return storge.getItem(key)
}