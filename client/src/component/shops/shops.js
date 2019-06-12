import React,{Component} from 'react';
import { Button } from 'antd';
import ComTable from '../common/ComTable';
import ComModal from '../common/ComModal';
import SearchForm from '../search';
import {post} from "../../utils/AxiosUtil";

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理
*/
export default class Profile extends Component{
    constructor(props){
        super(props);
        this.state = {
            shopUrl:'/v1/merchant/organization/create/info',
            addShopUrl: '/v1/merchant/organization/create/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam:{
                "org_name":"",
                "explain":"",
                "img_list":["图片地址1","图片地址2"],
                "sale_type":["美妆","家电"],
                "owner_code":"登录获取到的staff_code"
            },
            getParam:{},
            dataSource:[]
        }
    }

    componentDidMount = () => {
        post(this.state.url,this.state.postParam, null).then(res => {
            this.setState({
                dataSource: res.data
            })
        })
    }

    onSearch = (val)=>{

    }

    render (){
        const columns = [
            {
                title: '商铺名称',
                dataIndex: 'org_name',
                key: 'org_name',
                render: text => <a href="#">{text}</a>,
            },
            {
                title: '商铺简介',
                dataIndex: 'explain',
                key: 'explain',
            },
            {
                title: '商铺图片',
                dataIndex: 'img_list',
                key: 'img_list',
            },
            {
                title: '售货类型',
                dataIndex: 'sale_type',
                key: 'sale_type'
            },
            {
                title: '商铺管理员编码',
                dataIndex: 'owner_code',
                key: 'owner_code',
            }
        ];

        const { shopUrl, refresh, postParam, getParam, visible } = this.state

        return (
            <div className="lee-home">
                {/*创建商铺*/}
                <ComModal
                    visible={visible}
                    onCancel={()=>this.setState({auditVisible:false})}
                    onSubmit={this.auditConfirm}
                    title='审核'
                >
                    <p>aaaaaaaaaaaa</p>
                </ComModal>

                <div className="lee-home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="lee-home-btn">
                    <Button>创建商铺</Button>
                </div>

                <div className="lee-home-table">
                    <ComTable
                        columns={columns}
                        url={shopUrl}
                        refresh={refresh}
                        postParam={postParam}
                        getParam={getParam}
                    />
                </div>
            </div>
        )
    }
}