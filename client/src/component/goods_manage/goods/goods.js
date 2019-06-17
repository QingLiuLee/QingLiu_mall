import React from 'react';
import { Button,message } from 'antd';
import ComTable from '../../common/ComTable';
import ComModal from '../../common/ComModal';
import SearchForm from './search';
import GoodModal from './goodModal';
import { post } from '../../../utils/axiosUtil'
import { getLocalStorage } from '../../../utils/localStorage'

/**
 * @author hui
 * @date 2019/6/13
 * @Description: 商品管理 - 商品模块
*/
export default class Goods extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            goodUrl: '/v1/commodity/product/get/info/list',
            refresh: 0,//table改变时对应刷新变化值
            postParam: {},
            getParam: {},

            addGoodUrl: '/v1/commodity/product/create/info',
            editGoodUrl: '/v1/commodity/product/update/info',
            delGoodUrl: '/v1/commodity/product/delete/info',
            visible: false,
            isAdd: true,
            imgs: 'logo2',
            goodDatas: {
                // category_code: "C2019061623162339",
                // explain: "光滑柔嫩",
                // img_list: ["img1"],
                // org_code: "M2019061406340968",
                // product_name: "洗面奶",
                // sale_price: "40"
            },
            product_code_list: []
        }
    }

    componentDidMount = () => {
        this.onSearch({
            org_code:'M2019061403235646'
        })
    }

    // 查询
    onSearch = (val)=>{
        this.setState({
            refresh: 1,
            postParam: {
                ...val
            }
        },()=>{
            this.setState({
                refresh: 0
            })
        })
    }

    handleFormChange = () => {
        this.setState({disabled:false});
    }

    // 创建商品
    addModal = () =>{
        this.setState({
            visible: true,
            isAdd: true,
            disabled: false,
            goodDatas: {
                org_code: 'M2019061406340968',
                category_code: 'C2019061623162339'
            }
        })
    }

    // 更新商品
    editModal = (val) =>{
        this.setState({
            visible: true,
            isAdd: false,
            disabled: true,
            goodDatas: val
        })
    }

    // 创建 | 保存
    onSubmit = () =>{
        this.goodForm.props.form.validateFields((err, formData) => {
            if (!err) {
                const { isAdd, addGoodUrl, editGoodUrl, goodDatas} = this.state
                const url = isAdd ? addGoodUrl : editGoodUrl
                if(!isAdd){
                    formData.product_code = goodDatas.product_code
                }
                post(url,formData,null).then(res =>{
                    if(!isAdd){
                        message.success(res.data)
                    }
                    console.log(formData);
                    this.setState({
                        visible: false,
                        refresh: 1,
                    },()=>{
                        this.setState({
                            refresh: 0
                        })
                    })
                }).catch(err =>{
                    message.warning(err.data)
                })
            }
        });
    }

    // 批量删除
    delBatch = (record) =>{
        let param = {}
        if(record == null){
            param = {
                org_code: 'M2019061403235646',
                product_code_list: this.state.product_code_list
            }
        }else{
            param = {
                org_code: record.org_code,
                product_code_list: [record.product_code]
            }
        }
        post(this.state.delGoodUrl, param).then(res => {
            message.success(res.msg)
            this.setState({
                refresh: 1
            },()=>{
                this.setState({
                    refresh: 0
                })
            })
        })
    }


    render (){
        const {
            goodUrl, visible, isAdd, imgs,
            goodDatas,product_code_list,
            refresh, postParam, getParam
        } = this.state

        const rowSelection = {
            product_code_list,
            onChange: (selectedRowKeys, selectedRows) => {
                this.setState({
                    product_code_list: selectedRowKeys
                });
            }
        }

        const columns = [
            {
                title: '商品名称',
                dataIndex: 'product_name',
                key: 'product_name',
                render: text => <a href="#">{text}</a>,
            },
            {
                title: '商品简介',
                dataIndex: 'explain',
                key: 'explain',
            },
            {
                title: '商品图片',
                dataIndex: 'img_list',
                key: 'img_list',
                render: text => {
                    {/*<img src={imgs == undefined ? default_admin : require(`../../assert/images/${imgs}.png`)} alt=""/>*/}
                    return <img style={{maxWidth: 50,height: 'auto'}} src={require(`assert/images/logo/${imgs}.png`)} alt=""/>
                }
            },
            {
                title: '销售单价',
                dataIndex: 'sale_price',
                key: 'sale_price'
            },
            {
                title: '操作',
                dataIndex: 'opera',
                key: 'opera',
                render: (text,record) =>{
                    return <div>
                            <a onClick={()=>this.editModal(record)}>修改</a>
                            <span style={{margin:'0 5px'}}>|</span>
                            <a onClick={()=>this.delBatch(record)}>删除</a>
                        </div>
                }
            }
        ];

        return (
            <div className="ql-main home">
                {/* 创建|修改 商品*/}
                <ComModal
                    visible={visible}
                    onCancel={()=>this.setState({visible:false})}
                    onSubmit={this.onSubmit}
                    title={isAdd ? '创建商品':'修改商品'}
                >
                    <GoodModal
                        wrappedComponentRef={(form) => this.goodForm = form}
                        datas={goodDatas}
                        isAdd={isAdd}
                        onChange={this.handleFormChange}
                    />
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button type="primary" onClick={this.addModal}>创建商品</Button>
                    <Button type="primary" onClick={this.delBatch}>批量删除</Button>
                </div>

                <div className="ql-main-table home-table">
                    <ComTable
                        columns={columns}
                        url={goodUrl}
                        refresh={refresh}
                        postParam={postParam}
                        getParam={getParam}
                        rowSelection={rowSelection}
                        rowKey={record => record.product_code}
                    />
                </div>
            </div>
        )
    }
}