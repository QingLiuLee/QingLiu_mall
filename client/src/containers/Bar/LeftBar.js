import React, { Component } from 'react';
import { Route,Link,withRouter } from 'react-router-dom'
import { Icon } from 'antd';

@withRouter
export default class LeftBar extends Component {
    constructor(props){
        super(props);
        this.state = {
            active:0,
            links:[
                { path:'/home', icon:'home', title:'首页'},
                {
                    icon:'coffee', title:'商铺管理',
                    children:[
                        { path:'/shops/1', icon:'copy', title:'用户管理',},
                        { path:'/shops/2', icon:'copy', title:'商铺管理',}
                    ]
                },
                {
                    icon:'coffee', title:'商品管理',
                    children:[
                        { path:'/goods/1', icon:'copy', title:'品类管理',},
                        { path:'/goods/2', icon:'copy', title:'商品关联',}
                    ]
                }
            ],
        }
    }

    render() {
        const { pathname } = this.props.location;
        let { links,active } = this.state;
        links.filter((item, index)=>{
            if(pathname == item.path){
                active = index;
            }
        });
        return (
            <div className="lee-leftBar">
                <div className="lee-leftBar-top">
                    <div
                        className="lee-leftBar-logo"
                        style={this.props.toggle ? {paddingLeft:5}:null}
                    >
                        {this.props.toggle ?
                            <span style={{fontSize:18,paddingLeft:20}}>
                                <Icon type="appstore" />
                            </span> : 'QING LIU'}
                    </div>
                </div>
                <div className="lee-leftBar-bot">
                    <div className="lee-leftBar-bot-bar"></div>

                    <div className="lee-leftBar-list">
                        <ul style={{paddingTop:25}}>
                            {links.map((item, index)=>{
                                let html = [];
                                if(item.children){
                                    let itemHtml = item.children.map(itemC =>{
                                        return <li className={pathname == itemC.path ? "active animated jackInTheBox":null} key={itemC.path}>
                                            <Link to={itemC.path} onClick={()=>this.setState({active:index})}>
                                                <Icon type={itemC.icon} />
                                                <span>{itemC.title}</span>
                                            </Link>
                                        </li>
                                    })
                                    html.push(<ul key={index}>
                                                <li>
                                                    <div className="links">
                                                        <Icon type={item.icon} />
                                                        <span>{item.title}</span>
                                                    </div>
                                                    <ul>
                                                        {itemHtml}
                                                    </ul>
                                                </li>
                                            </ul>);
                                    return html;
                                }else{
                                    return <li className={pathname == item.path ? "active animated jackInTheBox":null} key={index}>
                                        <Link to={item.path} onClick={()=>this.setState({active:index})}>
                                            <Icon type={item.icon} />
                                            <span>{item.title}</span>
                                        </Link>
                                    </li>
                                }
                            })}

                            {/*<div className="libar" style={{transform: `translate3d(0px, ${active * 40}px, 0px)`}}></div>*/}
                        </ul>
                    </div>
                </div>
            </div>
        );
  }
}

