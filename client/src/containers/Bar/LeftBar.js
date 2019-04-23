import React, { Component } from 'react';
import { Route,Link,withRouter } from 'react-router-dom'
import { Menu, Icon } from 'antd';

@withRouter
export default class LeftBar extends Component {
    constructor(props){
        super(props);
        this.state = {
            active:0,
            links:[
                { path:'/home', icon:'home', title:'首页'}
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
                    <div className="lee-leftBar-list">
                        <ul>
                            {links.map((item, index)=>{
                                return <li className={pathname == item.path ? "active animated jackInTheBox":null} key={index}>
                                            <Link to={item.path} onClick={()=>this.setState({active:index})}><Icon type={item.icon} /><span>{item.title}</span></Link>
                                       </li>
                            })}

                            <div className="libar" style={{transform: `translate3d(0px, ${active * 50}px, 0px)`}}></div>
                        </ul>
                    </div>
                </div>
            </div>
        );
  }
}

