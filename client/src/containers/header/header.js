import React,{Component} from 'react';
import { Menu, Dropdown } from 'antd';
import { withRouter, Link } from 'react-router-dom';
import logo from 'assert/images/logo2.png';
import admin from 'assert/images/admin.png';

/**
 * @author hui
 * @date 2018/4/23
 * @Description: header
*/
@withRouter
export default class Header extends Component{
    constructor(props){
        super(props);
        this.state={
            active: '首页',
            menu:[{
                name:'首页',
                path:'/home'
            },{
                name:'发现',
                path:'/search'
            },{
                name:'话题',
                path:'/topics'
            }]
        }
    }

    componentDidMount(){
        let active = this.state.active;
        if(this.props.location.pathname == '/search'){
            active = '发现';
        }else if(this.props.location.pathname == '/topics'){
            active = '话题';
        }
        this.setState({active})
    }

    render (){
        const { menu,active } = this.state;
        const myList = (
            <Menu>
                <Menu.Item onClick={()=>this.props.history.push('/myDetail')}>
                    <span>我的主页</span>
                </Menu.Item>
                <Menu.Item onClick={this.props.toggleLogin}>
                    <span>我的登录</span>
                </Menu.Item>
            </Menu>
        );
        return (
            <header className='ql-card'>
                <div className="ql-header">
                    <div className="ql-header-l">
                        <div className="ql-header-logo">
                            <img src={logo}/>
                            <span>青榴</span>
                        </div>
                        <div className="ql-header-nav">
                            {
                                menu.map((item,index)=>{
                                    return <Link key={index} to={item.path} onClick={()=>this.setState({active:item.name})}>
                                                <span className={active == item.name ? 'active':''}>{item.name}</span>
                                            </Link>
                                })
                            }
                        </div>
                    </div>
                    <div className="ql-header-r">
                        <svg className="svgs" aria-hidden="true" style={{width:'1.2em' ,height:'1.2em'}}>
                            <use xlinkHref="#icontop-news"></use>
                        </svg>
                        <svg className="svgs" aria-hidden="true" >
                            <use xlinkHref="#icontop-msg"></use>
                        </svg>
                        <Dropdown overlay={myList} placement="topRight">
                            <img src={admin} alt="头像"/>
                        </Dropdown>
                    </div>
                </div>
            </header>
        )
    }
}