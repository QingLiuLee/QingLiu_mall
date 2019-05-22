import React, { Component } from 'react';
import { Route, Link } from 'react-router-dom'

import Login from '../../containers/login/login'
import Home from "../../component/home";
import Shops from '../../component/shops/shops';
import Goods from '../../component/goods/goods';

export default class RightBar extends Component {
    constructor(props){
        super(props);
        this.state = {
            route:[
                {exact:true, path:'/login', component:Login},
                {path:'/home', component:Home},
                {path:'/shops/1', component:Shops},
                {path:'/goods/1', component:Goods},
            ]
        }
    }

    render() {
        return (
            <div className="lee-rightBar-bot">
                <div className="lee-rightBar-bot-bot" >
                    {
                        this.state.route.map(item=>{
                            return <Route key={item.path} exact={item.exact ? true:false} path={item.path} component={item.component}/>
                        })
                    }
                </div>
            </div>
        );
  }
}

