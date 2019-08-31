import React,{ Component } from 'react';
import axios from "axios";
import { getLocalStorage } from '../utils/localStorage'

/**
 * @author hui
 * @date 2019/6/13
 * @Description: axios封装
*/
const prefix = '/api';
axios.defaults.withCredentials = true;
axios.defaults.headers.get['X-Requested-With'] = 'XMLHttpRequest';//Ajax get请求标识
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest';//Ajax post请求标识
axios.defaults.headers.post['Content-Type'] = 'application/json; charset=UTF-8';
axios.defaults.headers.put['X-Requested-With'] = 'XMLHttpRequest';//Ajax put请求标识
axios.defaults.headers.delete['X-Requested-With'] = 'XMLHttpRequest';//Ajax delete请求标识

axios.defaults.timeout = 10000;
axios.defaults.withCredentials = true;



// axios.defaults.headers.common['Authorization-token'] = token;

// http request拦截器:
axios.interceptors.request.use(config => {
    //添加token
    let token = '';
    if(getLocalStorage('auth_token') != 'null'){
        token = getLocalStorage('auth_token');
    }
    console.log('token:' + token);

    //发送请求操作，统一再请求里加上token
    config.headers.common['Authorization-token'] = token;
    return config;
}, error => {
    //发送请求错误操作
    alert('请求失败')
    return Promise.reject(error);
})

// http response拦截器 :对响应数据做操作
axios.interceptors.response.use(response => {
    //对响应数据做操作
    // token 为空，且不是登录请求
    console.log(getLocalStorage('auth_token'));
    if(getLocalStorage('auth_token') == 'null'){
        if(response.data.data.token != null){
            return response;
        }else{
            window.location.href = '/login';
        }
    }else {
        return response;
    }
}, error => {
    //对响应数据错误做操作
    console.log('请求error', error.message);
    return Promise.reject(error);
})

function query(url, params) {
    return new Promise((resolve, reject) => {
        axios.get(`${prefix}${url}`, {params: params}).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err.response.data)
        })
    })
}

//post请求会有post参数也可能有get参数
function post(url, datas, params) {
    return new Promise((resolve, reject) => {
        axios.post(`${prefix}${url}`,datas,{params:params}).then(res => {
            if(res.status === 207){
                resolve(res.data)
            }
        }).catch(err => {
            reject(err.response.data)
        })
    })
}

function requestAll(...paramsFun) {
    return new Promise((resolve, reject) => {
        axios.all(...paramsFun).then(axios.spread(function (...response) {
            let responseList = [];
            for(let res of response){
                if(!res.status && res.response){
                    responseList.push(res.response.data);
                }else{
                    responseList.push(res.data);
                }
            }
            return responseList;
        })).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err.data)
        })
    })
}

function deletes(url, params){
    return new Promise((resolve, reject) => {
        axios.post(`${prefix}${url}` + "/delete", params, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => {
            resolve(res.data)
        }).catch(err => {
            reject(err.response)
        })
    })
}

export {query, post, requestAll, deletes}