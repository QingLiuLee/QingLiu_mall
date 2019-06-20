import React from 'react';
import { Route } from 'react-router-dom'

import Login from '../../containers/login/login'
import Users from '../../component/shops_manage/users/users'
import Shops from '../../component/shops_manage/shops/shops'
import Category from '../../component/goods_manage/category/category'
import Goods from '../../component/goods_manage/goods/goods'

export default class RightBar extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            route:[
                {path:'/login', component:Login},
                {path:'/user', component: Users},
                {path:'/shops', component:Shops},
                {path:'/category', component:Category},
                {path:'/goods', component:Goods},
            ]
        }
    }

    render() {
        return (
            <div className="lee-rightBar-bot">
                <div className="lee-rightBar-bot-bot" >
                    {
                        this.state.route.map( item =>{
                            return <Route key={item.path} path={item.path} component={item.component}/>
                        })
                    }
                </div>
            </div>
        );
  }
}

