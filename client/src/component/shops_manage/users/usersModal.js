import React from 'react';
import {
    Form,
    Input,
    Select
} from 'antd';
const { Option } = Select;

/**
 * @author hui
 * @date 2019/6/12
 * @Description: 商铺管理 - 用户模块 -> 创建|修改商铺员工
*/
class UserModal extends React.Component{
    constructor(props){
        super(props);
        this.state = {
        }
    }

    render (){
        const { datas } = this.props;
        const { getFieldDecorator } = this.props.form;

        const formItemLayout = {
            labelCol: {
                xs: { span: 18 },
                sm: { span: 6 },
            },
            wrapperCol: {
                xs: { span: 30 },
                sm: { span: 18 },
            },
        };
        return (
            <div className="ql-modal">
                <div className="ql-search">
                    <Form {...formItemLayout}>
                        <Form.Item label="昵称" hasFeedback>
                            {getFieldDecorator('nickname', {
                                initialValue: datas ? datas.nickname : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入昵称',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="手机号" hasFeedback>
                            {getFieldDecorator('mobile', {
                                initialValue: datas ? datas.mobile : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入手机号',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="角色名称" hasFeedback>
                            {getFieldDecorator('role_name', {
                                initialValue: datas ? datas.role_name : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入角色编码',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="商铺编码" hasFeedback>
                            {getFieldDecorator('org_code', {
                                initialValue: datas ? datas.org_code : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺编码',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="密码" hasFeedback>
                            {getFieldDecorator('password', {
                                initialValue: datas ? datas.password : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺员工密码',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                    </Form>
                </div>
            </div>
        )
    }
}
export default Form.create({
    name: 'userModal',
    onFieldsChange(props, changedFields) {   //监听修改是否可保存
        props.onChange(changedFields);    //onChange对应监听值改变就执行父组件方法
    }
})(UserModal)