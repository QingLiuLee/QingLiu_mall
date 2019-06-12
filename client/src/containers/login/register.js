import React,{Component} from 'react';
import { Input,Icon,Button,Radio } from 'antd';
import logo from 'assert/images/logo/logo2.png';
const RadioGroup = Radio.Group;

/**
 * @author hui
 * @date 2019/6/12
 * @Description: 注册
*/
export default class Register extends Component{
    constructor(props){
        super(props);
        this.state={
            account:null,
            password:null,
            gender:1
        }
    }

    //注册
    register = ()=>{
        this.props.toggleRegister(false,false)
    }

    render (){
        const { account, password, gender } = this.state;
        const style = {
            lineHeight: '30px',
            marginTop: '15px',
            width: '100%',
            textAlign: 'left',
            paddingLeft: '30px'
        }
        return (
            <div className="ql-mask">
                <div className="ql-login">
                    <div className="ql-login-all">
                        <div className="ql-login-all-close" onClick={()=>this.props.toggleRegister(false,false)}>
                            <span><i className='icon-close' /></span>
                        </div>
                        <div className="ql-login-all-l">
                            <img src={logo} alt=""/>
                            <h2>青榴</h2>
                        </div>
                        <div className="ql-login-all-r">
                            <h2>注册</h2>
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
                            {/*<Input
                                placeholder="Enter your mobile"
                                prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                value={account}
                                onChange={(e) => this.setState({ account: e.target.value })}
                            />*/}
                            <RadioGroup
                                style={style}
                                value={gender}
                                onChange={(e) => this.setState({ gender: e.target.value })}
                            >
                                <Radio value={1} style={{width:'42%'}}>男</Radio>
                                <Radio value={2}>女</Radio>
                            </RadioGroup>
                            <Button type="primary" onClick={this.register} style={{marginTop:15}}>注册</Button>
                            <p>已有帐号 ？<span onClick={()=>this.props.toggleRegister(true,false)}>立即登录</span></p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}