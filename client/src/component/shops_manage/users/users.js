import React from 'react';
import { Button,message } from 'antd';
import ComTable from '../../common/ComTable';
import ComModal from '../../common/ComModal';
import SearchForm from './search';
import UserModal from './usersModal';
import { post } from '../../../utils/axiosUtil'
import { getLocalStorage } from '../../../utils/localStorage'

/**
 * @author hui
 * @date 2019/4/28
 * @Description: 商铺管理 - 用户模块
*/
export default class User extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            userUrl: '/v1/merchant/staff/get/inner/list',
            addStaffUrl: '/v1/merchant/staff/create/inner/info',
            editStaffUrl: '/v1/merchant/organization/update/info',
            refresh: 0,
            postParam: {
                org_code: "M2019061403235646"
            },
            getParam: {},
            dataSource: [],
            visible: false,
            isAdd: true,
            imgs: 'admin',
            shopDatas: {
                org_code: "M2019061403235646"
            },
            disabled: false
        }
    }

    componentDidMount = () => {
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

    // 创建商铺员工
    addModal = () =>{
        this.setState({
            visible:true,
            isAdd: true,
            disabled: false,
            shopDatas: {
                org_code: "M2019061403235646"
            }
        })
    }

    // 更新商铺员工
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
        this.refs.userform.validateFields((err, formData) => {
            if (!err) {
                const { isAdd, addStaffUrl, editStaffUrl } = this.state
                const url = isAdd ? addStaffUrl : editStaffUrl
                post(url,formData,null).then(res =>{
                    if(!isAdd){
                        message.success(res.data)
                    }
                    this.setState({
                        visible: false,
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
            userUrl, visible, isAdd, imgs,
            shopDatas, disabled,
            refresh, postParam, getParam
        } = this.state

        const columns = [
            {
                title: '用户名',
                dataIndex: 'nickname',
                key: 'nickname',
                render: text => <a href="#">{text}</a>,
            },
            {
                title: '头像',
                dataIndex: 'avatar',
                key: 'avatar',
                render: (text, record) => {
                    return <div style={{padding:'5px'}}>
                        <img
                            style={{width: 35, height: 35, borderRadius: '50%',border: '1px solid #ddd'}}
                            src={require(`assert/images/${imgs}.jpg`)}
                            alt=""
                        />
                    </div>
                }
            },
            {
                title: '创建时间',
                dataIndex: 'create_time',
                key: 'create_time',
            },
            {
                title: '手机号',
                dataIndex: 'mobile',
                key: 'mobile'
            },
            {
                title: '操作',
                dataIndex: 'opera',
                key: 'opera',
                /*render: (text,record) =>{
                    return <div>
                        <a onClick={()=>this.editModal(record)}>修改</a>
                        {/!*<span style={{margin:'0 5px'}}>|</span>*!/}
                        {/!*<a onClick={()=>this.delBatch(record)}>删除</a>*!/}
                    </div>
                }*/
            }
        ];

        return (
            <div className="ql-main home">
                {/* 创建|修改 */}
                <ComModal
                    visible = {visible}
                    title = {isAdd ? '创建商铺员工':'修改商铺员工'}
                    disabled = {disabled}
                    onCancel = {()=>this.setState({visible:false})}
                    onSubmit = {this.onSubmit}
                >
                    <UserModal
                        ref="userform"
                        datas={shopDatas}
                        onChange={this.handleFormChange}
                    />
                </ComModal>

                <div className="ql-main-search home-search">
                    <SearchForm onSearch={this.onSearch}/>
                </div>

                <div className="ql-main-btns home-btn">
                    <Button type="primary" onClick={this.addModal}>创建商铺员工</Button>
                </div>

                <div className="ql-main-table home-table">
                    <ComTable
                        columns={columns}
                        url={userUrl}
                        refresh={refresh}
                        postParam={postParam}
                        getParam={getParam}
                    />
                </div>
            </div>
        )
    }
}