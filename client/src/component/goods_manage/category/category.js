import React,{Component} from 'react';
import { Button,message } from 'antd';
import ComTable from '../../common/ComTable';
import ComModal from '../../common/ComModal';
import SearchForm from '../../search';
import CategoryModal from './categoryModal';
import { post } from '../../../utils/axiosUtil'

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商品管理 - 品类模块
*/
export default class Category extends Component{
    constructor(props){
        super(props);
        this.state = {
            categoryUrl: '/v1/commodity/category/get/info/list',
            refresh: 0,
            postParam: {
                org_code: "M2019061320011857"
            },
            getParam: {},

            addCategoryUrl: '/v1/commodity/category/create/info',
            editCategoryUrl: '/v1/commodity/category/update/info',
            visible: false,
            isAdd: true,

            categoryDatas: {}
        }
    }

    componentDidMount = () => {
        this.onSearch(null)
    }

    // 查询
    onSearch = (val)=>{
        this.setState({
            refresh: 1
        },()=>{
            this.setState({
                refresh: 0
            })
        })
    }

    handleFormChange = () => {
        this.setState({disabled:false});
    }

    // 创建商铺
    addModal = () =>{
        this.setState({
            visible: true,
            isAdd: true
        })
    }

    // 更新商铺
    editModal = (val) =>{
        console.log(val);
        this.setState({
            visible: true,
            isAdd: false,
            categoryDatas: val
        })
    }

    // 创建 | 保存
    onSubmit = () =>{
        this.refs.categoryform.validateFields((err, formData) => {
            if (!err) {
                console.info('success');
                const { isAdd, addCategoryUrl, editCategoryUrl, categoryDatas} = this.state
                const url = isAdd ? addCategoryUrl : editCategoryUrl
                if(!isAdd){
                    formData.category_code = categoryDatas.category_code
                }
                post(url,formData,null).then(res =>{
                    if(!isAdd){
                        message.success(res.data)
                    }
                    this.setState({
                        visible: false,
                        categoryDatas: [],
                        refresh:1
                    },()=>{
                        this.setState({
                            refresh:0
                        })
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
            categoryUrl, visible, isAdd,
            categoryDatas,
            refresh, postParam, getParam
        } = this.state

        const columns = [
            {
                title: '品类名称',
                dataIndex: 'category_name',
                key: 'category_name',
                render: text => <a href="#">{text}</a>
            },
            {
                title: '创建时间',
                dataIndex: 'create_time',
                key: 'create_time'
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
                {/* 创建|修改 品类*/}
                <ComModal
                    visible={visible}
                    onCancel={()=>this.setState({visible:false})}
                    onSubmit={this.onSubmit}
                    title={isAdd ? '创建品类':'修改品类'}
                >
                    <CategoryModal
                        onChange={this.handleFormChange}
                        ref="categoryform"
                        datas={categoryDatas}
                    />
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button onClick={this.addModal}>创建品类</Button>
                </div>

                <div className="ql-main-table home-table">
                    <ComTable
                        columns={columns}
                        url={categoryUrl}
                        refresh={refresh}
                        postParam={postParam}
                        getParam={getParam}
                    />
                </div>
            </div>
        )
    }
}