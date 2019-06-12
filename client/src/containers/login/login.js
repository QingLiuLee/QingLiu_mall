import React,{Component} from 'react';
import { Input,Icon,Button } from 'antd';
import logo from 'assert/images/logo/logo2.png';
import { post } from '../../utils/AxiosUtil'

/**
 * @author hui
 * @date 2019/6/12
 * @Description: 登录
*/
export default class Login extends Component{
    constructor(props){
        super(props);
        this.state={
            loginUrl: '/v1/merchant/staff/sign/in',
            account: "13512722864",
            password: "10241026"
        }
    }

    // 登录
    login = ()=>{
        const { account, password } = this.state
        post(this.state.loginUrl,{ account, password }, null).then(res => {
            debugger
            // if(res.code === 200){
            if(res.msg == "请求成功"){
                this.props.toggleLogin(false,false);
                let storage = window.localStorage;
                storage.setItem('auth_token', res.data.token);
                storage.setItem('staff_code', res.data.staff_code);
            }
        })
    }

    render (){
        const { account, password } = this.state;
        return (
            <div className="ql-mask">
                <div className="ql-login">
                    <div className="ql-login-all">
                        <div className="ql-login-all-close" onClick={()=>this.props.toggleLogin(false,false)}>
                            <span><i className='icon-close' /></span>
                        </div>
                        <div className="ql-login-all-l">
                            <img src={logo} alt=""/>
                            <h2>青榴</h2>
                        </div>
                        <div className="ql-login-all-r">
                            <h2>登录</h2>
                            <h1>QING LIU</h1>
                            <Input
                                placeholder="Enter your username"
                                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                value={account}
                                onChange={(e) => this.setState({ account: e.target.value })}
                            />
                            <Input
                                placeholder="Enter your password"
                                prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                value={password}
                                onChange={(e) => this.setState({ password: e.target.value })}
                            />
                            <Button type="primary" onClick={this.login}>登录</Button>
                            <p>还未注册? <span onClick={()=>this.props.toggleLogin(false,true)}>注册</span></p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}