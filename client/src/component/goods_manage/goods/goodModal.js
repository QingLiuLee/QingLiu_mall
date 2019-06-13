import React,{Component} from 'react';
import {
    Form,
    Input,
    Select
} from 'antd';
const { Option } = Select;

/**
 * @author hui
 * @date 2019/6/13
 * @Description: 商铺管理 - 商品模块 -> 创建|修改
*/
class GoodModal extends Component{
    constructor(props){
        super(props);
        this.state = {
            img_list: ['img1','img2'],
            sale_type: ["美妆","家电"],
        }
    }

    // 售货类型
    changeSaleType = () =>{

    }

    // 商铺图片
    changeImgList = () =>{

    }

    render (){
        const { img_list, sale_type } = this.state
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
                        <Form.Item label="商铺名称" hasFeedback>
                            {getFieldDecorator('org_name', {
                                initialValue: datas ? datas.org_name : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺名称',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="商铺简介" hasFeedback>
                            {getFieldDecorator('explain', {
                                initialValue: datas ? datas.explain : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺简介',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="商铺图片" hasFeedback>
                            {getFieldDecorator('img_list', {
                                initialValue: datas ? datas.img_list : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺图片名称',
                                    },
                                ]
                            })(
                                <Select
                                    mode="multiple"
                                    style={{ width: '100%' }}
                                    placeholder="Please select"
                                    onChange={this.changeSaleType}
                                >
                                    {
                                        img_list.length > 0 && img_list.map(item => {
                                            return <Option key={item}>{item}</Option>
                                        })
                                    }
                                </Select>
                            )}
                        </Form.Item>
                        <Form.Item label="售货类型" hasFeedback>
                            {getFieldDecorator('sale_type', {
                                initialValue: datas ? datas.sale_type : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入售货类型',
                                    },
                                ]
                            })(
                                <Select
                                    mode="multiple"
                                    style={{ width: '100%' }}
                                    placeholder="Please select"
                                    onChange={this.changeSaleType}
                                >
                                    {
                                        sale_type.length > 0 && sale_type.map(item => {
                                            return <Option key={item}>{item}</Option>
                                        })
                                    }
                                </Select>
                            )}
                        </Form.Item>
                        <Form.Item label="商铺管理员编码" hasFeedback>
                            {getFieldDecorator('staff_code', {
                                initialValue: datas ? datas.staff_code : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入商铺管理员编码',
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
export default Form.create({ name: 'addShop' })(GoodModal)