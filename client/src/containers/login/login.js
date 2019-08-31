import React,{Component} from 'react';
import { Input,Icon,Button,message } from 'antd';
import logo from 'assert/images/logo/logo2.png';
import { post } from '../../utils/axiosUtil'
import { setLocalStorage } from '../../utils/localStorage'
import Register from './register';

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
            password: "10241026",
            isLogin: true,
        }
    }

    // 登录
    login = ()=>{
        const { account, password } = this.state;
        // loginin
        post(this.state.loginUrl,{ account, password }, null).then(res => {
            // if(res.code === 200){
            if(res.msg == "请求成功"){
                setLocalStorage('auth_token', res.data.token);
                setLocalStorage('staff_code', res.data.staff_code);
                message.success('登录成功！');
                setTimeout(() => {
                    this.props.history.push('/user');
                }, 500);
            }
        })
    }

    //隐藏显示登录 | 注册
    toggle = ()=>{
        this.setState({
            isLogin: !this.state.isLogin
        });
    }

    render (){
        const { account, password, isLogin } = this.state;
        return (
            <div className="ql-mask">
                {
                    isLogin ?
                        <div className="ql-login">
                            <div className="ql-login-all">
                                {/* <div className="ql-login-all-close" onClick={()=>this.props.toggleLogin(false,false)}>
                                    <span><i className='icon-close' /></span>
                                </div> */}
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
                                    <p>还未注册? <span onClick={this.toggle}>注册</span></p>
                                </div>
                            </div>
                        </div>
                        :
                        <Register
                            toggle={this.toggle}
                        />
                }
            </div>
        )
    }
}