import React,{Component} from 'react';
import { Button,message } from 'antd';
import ComTable from '../../common/ComTable';
import ComModal from '../../common/ComModal';
import SearchForm from '../../search';
import CategoryModal from './categoryModal';
import { post } from '../../../utils/axiosUtil'
import { getLocalStorage } from '../../../utils/localStorage'

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商品管理 - 品类模块
*/
export default class Category extends Component{
    constructor(props){
        super(props);
        this.state = {
            categoryUrl: '/v1/merchant/organization/create/info',
            refresh: 0,//table改变时对应刷新变化值
            postParam: {},
            getParam: {},

            addCategoryUrl: '/v1/commodity/category/create/info',
            editCategoryUrl: '/v1/commodity/category/update/info',
            visible: false,
            isAdd: true,
            imgs: 'logo2',
            categoryDatas: {
                category_name: undefined,
                org_code: "M201906130428176",
            }
        }
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
        this.refs.categoryform.validateFields((err, formData) => {
            if (!err) {
                console.info('success');
                const { isAdd, addCategoryUrl, editCategoryUrl, categoryDatas} = this.state
                const url = isAdd ? addCategoryUrl : editCategoryUrl
                post(url,formData,null).then(res =>{
                    if(isAdd){
                        formData.category_code = res.data
                    }else{
                        message.success(res.data)
                    }
                    console.log(formData);
                    this.setState({
                        visible: false,
                        categoryDatas: formData
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
            categoryDatas,
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
                    <CategoryModal ref="categoryform" datas={categoryDatas}/>
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button onClick={this.addModal}>创建品类</Button>
                    <Button onClick={this.editModal}>更新品类</Button>
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