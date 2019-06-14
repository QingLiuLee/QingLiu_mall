/**
 * @author hui
 * @date 2019/4/23
 * @Description: 登录
 * @param: registerData:注册信息 | userData:用户信息 | auth_token
 */

import axiosUtil from '../utils/axiosUtil';
const LOGIN = 'LOGIN';
const REGISTER = 'REGISTER';
const USER_LIST_DATA = 'USER_LIST_DATA';

let initState = {
    registerData:{},
    userData:{
        account:"huihui"
    },
    auth_token:'111111111111',
}

export function login(state = initState, action){
    switch (action.type){
        case REGISTER:
            return {
                ...state,
                registerData:action.payload.data
            }
        case LOGIN:
            return {
                ...state,
                userData:action.payload.data,
                auth_token:action.payload.auth_token
            }
        case USER_LIST_DATA:
            return {
                ...state,
                auth_token:action.payload.data
            }
        default:
            return state;
    }
}

//注册
export function isRegister(data) {
    return (dispatch)=>{
        axiosUtil.post('/users/create/account/info',data,null).then(res =>{
            if(res.code == 200) {
                /*"account":"admin",
                "password":"10241026",
                "avatar":"",  #头像链接
                "gender":"1",  #性别 1：男 2:女 3:未知
                "birthday":"2019-03-19",#出生日期
                "mobile":"15911111111"   #手机号*/
                dispatch(registerData(res.data));
            }
        })
    }
}

export function registerData(data) {
    return {type:REGISTER,payload:data};
}

//登录
export function isLogin(data) {
    return (dispatch)=>{
        axiosUtil.post('/users/sign/in',data,null).then(res =>{
            if(res.code === 200) {
                dispatch(loginData(data,res.data.auth_token));

                //存储token
                let storage = window.localStorage;
                 storage.setItem("auth_token",res.data.auth_token);
                 if(storage.getItem("auth_token")) {
                     //判断存储是否成功
                    console.log(storage.getItem("auth_token"));
                 }
            }
        })
    }
}

export function loginData(data,auth_token) {
    return {type:LOGIN,payload:{data,auth_token}};
}

//获取用户信息
export function getUserListData(data) {
    return (dispatch)=>{
        axiosUtil.post('users/sign/in',data,null).then(res =>{
            if(res.code === 200) {
                dispatch(userListData(res.data));
            }
        })
    }
}

export function userListData(data) {
    return {type:USER_LIST_DATA,payload:data};
}