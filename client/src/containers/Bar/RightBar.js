import React from 'react';
import { Route } from 'react-router-dom'

import Login from '../../containers/login/login'
import Shops from '../../component/shops_manage/shops/shops'
import Category from '../../component/goods_manage/category/category'
import Goods from '../../component/goods_manage/goods/goods'

export default class RightBar extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            route:[
                {exact:true, path:'/login', component:Login},
                {path:'/shops_mange/user', component:Shops},
                {path:'/shops_mange/shops', component:Shops},
                {path:'/goods_mange/category', component:Category},
                {path:'/goods_mange/goods', component:Goods},
            ]
        }
    }

    render() {
        return (
            <div className="lee-rightBar-bot">
                <div className="lee-rightBar-bot-bot" >
                    {
                        this.state.route.map( item =>{
                            return <Route key={item.path} exact={item.exact ? true:false} path={item.path} component={item.component}/>
                        })
                    }
                </div>
            </div>
        );
  }
}

