import React,{Component} from 'react';
import { Button } from 'antd';
import ComTable from '../common/ComTable';
import ComModal from '../common/ComModal';
import SearchForm from '../search';
import AddShopModal from './addShopModal';

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理
*/
const storge = window.localStorage;
let staff_code = '';
if(storge.getItem('staff_code')){
    staff_code = storge.getItem('staff_code')
}
export default class Profile extends Component{
    constructor(props){
        super(props);
        this.state = {
            shopUrl: '/v1/merchant/organization/create/info',
            addShopUrl: '/v1/merchant/organization/create/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam: {
                org_name: "商家名2",
                explain: "简介",
                img_list: ["logo3","logo2"],
                sale_type: ["美妆","家电"],
                owner_code: staff_code
            },
            getParam: {},
            dataSource: [],
            visible: false,
            imgs: 'logo2'
        }
    }

    componentDidMount = () => {
        // import logo from 'assert/images/logo/logo2.png';
        // this.onSearch(null)
    }

    // 查询
    onSearch = (val)=>{
        this.setState({
            refresh:1
        },()=>{
            this.setState({
                refresh:0
            })
        })
    }

    // 创建商铺
    addModal = () =>{
        this.setState({
            visible:true
        })
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
                render: text => {
                    {/*<img src={imgs == undefined ? default_admin : require(`../../assert/images/${imgs}.png`)} alt=""/>*/}
                    return <img style={{maxWidth: 100,height: 'auto'}} src={require(`assert/images/logo/${imgs}.png`)} alt=""/>
                }
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

        const { shopUrl, refresh, postParam, getParam, visible,imgs } = this.state

        const data = [{
            key: '1',
            name: 'John Brown',
            age: 32,
            address: 'New York No. 1 Lake Park',
        }, {
            key: '2',
            name: 'Jim Green',
            age: 42,
            address: 'London No. 1 Lake Park',
        }, {
            key: '3',
            name: 'Joe Black',
            age: 32,
            address: 'Sidney No. 1 Lake Park',
        }];

        return (
            <div className="ql-home">
                {/*创建商铺*/}
                <ComModal
                    visible={visible}
                    onCancel={()=>this.setState({visible:false})}
                    onSubmit={this.addModal}
                    title='创建商铺'
                >
                    <AddShopModal />
                </ComModal>

                <div className="ql-home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-home-btn">
                    <Button onClick={this.addModal}>创建商铺</Button>
                </div>

                <div className="ql-home-table">
                    <ComTable
                        columns={columns}
                        url={shopUrl}
                        refresh={refresh}
                        postParam={postParam}
                        getParam={getParam}
                        newDatas={data}
                    />
                </div>
            </div>
        )
    }
}