import React from 'react';
import { Button,message } from 'antd';
import ComTable from '../../common/ComTable';
import ComModal from '../../common/ComModal';
import SearchForm from './search';
import ShopModal from './addShopModal';
import { post } from '../../../utils/axiosUtil'
import { getLocalStorage } from '../../../utils/localStorage'

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理 - 商铺模块
*/
export default class Shops extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            shopUrl: '/v1/merchant/organization/get/info/list',
            addShopUrl: '/v1/merchant/organization/create/info',
            editShopUrl: '/v1/merchant/organization/update/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam: {
                staff_code: getLocalStorage('staff_code')
            },
            getParam: {},
            dataSource: [],
            visible: false,
            isAdd: true,
            imgs: 'logo2',
            shopDatas: {
                staff_code: getLocalStorage('staff_code')
            },
            disabled: false
        }
    }

    componentDidMount = () => {
        // import logo from 'assert/images/logo/logo2.png';
        this.onSearch(null)
    }

    handleFormChange = () => {
        this.setState({disabled: false});
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
            isAdd: true,
            disabled: false,
            shopDatas: {
                staff_code: getLocalStorage('staff_code')
            }
        })
    }

    // 更新商铺
    editModal = (val) =>{
        this.setState({
            visible:true,
            isAdd: false,
            disabled: true,
            shopDatas:val
        })
        console.log(val);
    }

    // 创建 | 保存
    onSubmit = () =>{
        this.refs.shopform.validateFields((err, formData) => {
            if (!err) {
                const { isAdd, addShopUrl, editShopUrl,shopDatas } = this.state
                const url = isAdd ? addShopUrl : editShopUrl

                if(!isAdd){
                    formData.org_code = shopDatas.org_code
                }
                post(url,formData,null).then(res =>{
                    if(!isAdd){
                        message.success(res.data)
                    }
                    this.setState({
                        visible: false,
                        shopDatas: {
                            staff_code: getLocalStorage('staff_code')
                        },
                        refresh:1
                    },()=>{
                        this.setState({
                            refresh:0
                        })
                    })
                }).catch(err =>{
                    message.warning(err.data)
                })
            }
        });
    }

    render (){
        const {
            shopUrl, visible, isAdd, imgs,
            shopDatas, disabled,
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
                    return <img style={{maxHeight: 50}} src={require(`assert/images/logo/${imgs}.png`)} alt=""/>
                }
            },
            {
                title: '售货类型',
                dataIndex: 'sale_type',
                key: 'sale_type'
            },
            {
                title: '操作',
                dataIndex: 'opera',
                key: 'opera',
                render: (text,record) =>{
                    return <a onClick={()=>this.editModal(record)}>修改</a>
                }
            }
        ];

        return (
            <div className="ql-main home">
                {/* 创建|修改 商铺*/}
                <ComModal
                    visible = {visible}
                    title = {isAdd ? '创建商铺':'修改商铺'}
                    disabled = {disabled}
                    onCancel = {()=>this.setState({visible:false})}
                    onSubmit = {this.onSubmit}
                >
                    <ShopModal
                        ref="shopform"
                        datas={shopDatas}
                        onChange={this.handleFormChange}
                    />
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button type="primary" onClick={this.addModal}>创建商铺</Button>
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