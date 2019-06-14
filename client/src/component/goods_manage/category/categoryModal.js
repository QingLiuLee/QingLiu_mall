import React,{Component} from 'react';
import {
    Form,
    Input,
    Select
} from 'antd';
const { Option } = Select;

/**
 * @author hui
 * @date 2019/6/12
 * @Description: 商铺管理 - 品类模块 -> 创建|修改
*/
class CategoryModal extends Component{
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
        console.log(datas);
        return (
            <div className="ql-modal">
                <div className="ql-search">
                    <Form {...formItemLayout}>
                        <Form.Item label="品类名称" hasFeedback>
                            {getFieldDecorator('category_name', {
                                initialValue: datas ? datas.category_name : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入品类名称',
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
                        <Form.Item label="员工编码" hasFeedback>
                            {getFieldDecorator('staff_code', {
                                initialValue: datas ? datas.staff_code : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入员工编码',
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
Form.create({
    name: 'addShop',
    onFieldsChange(props, changedFields) {   //监听修改是否可保存
        props.onChange(changedFields);    //onChange对应监听值改变就执行父组件方法
    }
})(CategoryModal)