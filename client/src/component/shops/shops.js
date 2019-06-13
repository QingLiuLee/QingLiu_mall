import React,{Component} from 'react';
import { Button,message } from 'antd';
import ComTable from '../common/ComTable';
import ComModal from '../common/ComModal';
import SearchForm from '../search';
import AddShopModal from './addShopModal';
import { post } from '../../utils/axiosUtil'
import { getLocalStorage } from '../../utils/localStorage'

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理
*/
export default class Profile extends Component{
    constructor(props){
        super(props);
        this.state = {
            shopUrl: '/v1/merchant/organization/create/info',
            addShopUrl: '/v1/merchant/organization/create/info',
            editShopUrl: '/v1/merchant/organization/update/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam: {},
            getParam: {},
            dataSource: [],
            visible: false,
            isAdd: true,
            imgs: 'logo2',
            shopDatas: {
                org_name: undefined,
                explain: undefined,
                img_list: undefined,
                sale_type: undefined,
                staff_code: getLocalStorage('staff_code')
            },
            shopDatas2: {
                explain: "商铺1-简介1",
                img_list: "img1",
                org_code: "M201906130428176",
                org_name: "商铺11",
                sale_type: "美妆",
                staff_code: "S2019061204090878"
            }
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
            visible:true,
            isAdd: true
        })
    }

    // 更新商铺
    editModal = () =>{
        this.setState({
            visible:true,
            isAdd: false
        })
    }

    // 创建 | 保存
    onSubmit = () =>{
        this.refs.shopform.validateFields((err, formData) => {
            if (!err) {
                console.info('success');
                const { isAdd, addShopUrl, editShopUrl, shopDatas2} = this.state
                const url = isAdd ? addShopUrl : editShopUrl

                if(!isAdd){
                    formData.org_code = shopDatas2.org_code
                    console.log(formData)
                }
                post(url,formData,null).then(res =>{
                    if(isAdd){
                        formData.org_code = res.data
                    }else{
                        message.success(res.data)
                    }
                    console.log(formData);
                    this.setState({
                        visible: false,
                        shopDatas: formData
                    })
                }).catch(err =>{
                    message.warning(err.data)
                    this.setState({
                        visible: false
                    })
                })
            }
        });
    }

    render (){
        const {
            shopUrl, visible, isAdd, imgs,
            shopDatas, shopDatas2,
            refresh, postParam, getParam
        } = this.state

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

        return (
            <div className="ql-main home">
                {/* 创建|修改 商铺*/}
                <ComModal
                    visible={visible}
                    onCancel={()=>this.setState({visible:false})}
                    onSubmit={this.onSubmit}
                    title={isAdd ? '创建商铺':'修改商铺'}
                >
                    <AddShopModal ref="shopform" shopDatas={shopDatas2}/>
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button onClick={this.addModal}>创建商铺</Button>
                    <Button onClick={this.editModal}>更新商铺</Button>
                </div>

                <div className="ql-main-table home-table">
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