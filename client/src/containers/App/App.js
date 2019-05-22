import React, { Component } from 'react';
import { Icon,Input,Badge,Menu, Dropdown,Divider } from 'antd';
import { Link,withRouter } from 'react-router-dom';

import LeftBar from '../Bar/LeftBar';
import RightBar from '../Bar/RightBar';
import adminImg from '../../assert/images/admin.jpg';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            toggle: false,
            avatarDefault: adminImg,
            search: false,   //搜索
            showSkin: false,  //皮肤
            skinColor: 'themsSVGLFZ',
            skinNormal: [
                {color: 'themsBlack', name: '夜间'},
                // {color: 'themsPurple', name: '紫色'},
            ],
            skinSvg: [
                {color: 'themsSVGL', name: '蓝色'},
                {color: 'themsSVGLF', name: '蓝粉色'},
                {color: 'themsSVGLFZ', name: '蓝粉紫色'},
                {color: 'themsSVGF', name: '粉色'},
                {color: 'themsSVGFZ', name: '粉紫色'},
                {color: 'themsSVGGF', name: '橘粉色'},
            ],
        };
    }

    componentDidMount() {}

    //更改皮肤svg
	setSkin = (item)=>{
        this.setState({skinColor: item.color});
	}

	render() {
        const Search = Input.Search;
        const {
        	avatarDefault, search,toggle,
            skinColor, skinNormal, skinSvg,
        } = this.state;

        const menu  =
            <Menu>
                <Menu.SubMenu title="基础色皮肤">
                    {skinNormal.map((item,index)=> {
                        return <Menu.Item key={`n-${index}`} onClick={()=>this.setState({skinColor: item.color})}>{item.name}</Menu.Item>
                    })}
                </Menu.SubMenu>
                <Menu.SubMenu title="svg格式皮肤">
                    {skinSvg.map((item,index)=> {
                        return <Menu.Item key={`s-${index}`} onClick={()=>this.setSkin(item)}>{item.name}</Menu.Item>
                    })}
                </Menu.SubMenu>
            </Menu>;

        const logins = (
            <Menu>
                <Menu.Item>
                    <div className="login-in"  onClick={()=>this.props.history.push('/login')}>
                        <Icon type="smile" />登录
                    </div>
                </Menu.Item>
            </Menu>
        );
		return(
			<div className="lee-admin" style={{position:'absolute'}}>
				<div className={`thems ${skinColor} ${toggle ? 'lee-in':''}`}>
                    <LeftBar toggle={toggle}/>
					<div className="lee-rightBar">
						<div className="lee-rightBar-top">
                            <div className="lee-rightBar-toogle"
                                 onClick={()=>{this.setState({toggle:!toggle})}}
                            >
                                <Icon type={toggle ? 'menu-unfold':'menu-fold'} theme="outlined" />
                            </div>
							<div className="lee-rightBar-search">
								<Search
									style={{display:search ? null:'none'}}
									placeholder="input search text"
									onSearch={value => console.log(value)}
								/>
								<span>
									<Icon
										type="search"
										onClick={()=>this.setState({search:!search})}
									/>
									搜索
								</span>
							</div>
							<div className="lee-rightBar-top-r">
								<div>
									<Badge dot>
										<Icon type="bell" />
									</Badge>
								</div>
                                <div>
									<Dropdown overlay={menu} trigger={['click']} placement='bottomRight'>
										<span><Icon type="skin" style={{fontSize:20}} /></span>
									</Dropdown>
								</div>
                                <Divider type="vertical" />
                                <div className="user">
                                    <Dropdown overlay={logins} overlayClassName="login-opera">
                                        <a className="ant-dropdown-link" href="#">
                                            <img src={avatarDefault} alt=""/>
                                        </a>
                                    </Dropdown>
                                </div>
                                <div className="name">慧慧</div>
							</div>
						</div>
                        <RightBar/>
					</div>
				</div>
			</div>
			)
	}
}

export default App;
