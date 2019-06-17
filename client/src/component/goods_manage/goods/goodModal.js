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
 * @Description: 商品管理 - 商品模块 -> 创建|修改
*/
class GoodModal extends Component{
    constructor(props){
        super(props);
        this.state = {
            img_list: ['img1','img2']
        }
    }

    // 商品图片
    changeImgList = () =>{

    }

    render (){
        const { img_list } = this.state
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
                        <Form.Item label="品类编码" hasFeedback>
                            {getFieldDecorator('category_code', {
                                initialValue: datas ? datas.category_code : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入品类编码',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="产品名称" hasFeedback>
                            {getFieldDecorator('product_name', {
                                initialValue: datas ? datas.product_name : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入产品名称',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="产品简介" hasFeedback>
                            {getFieldDecorator('explain', {
                                initialValue: datas ? datas.explain : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入产品简介',
                                    },
                                ]
                            })(
                                <Input />
                            )}
                        </Form.Item>
                        <Form.Item label="产品图片" hasFeedback>
                            {getFieldDecorator('img_list', {
                                initialValue: datas ? datas.img_list : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请选择产品图片名称',
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
                        <Form.Item label="销售单价" hasFeedback>
                            {getFieldDecorator('sale_price', {
                                initialValue: datas ? datas.sale_price : undefined,
                                rules: [
                                    {
                                        required: true,
                                        message: '请输入销售单价',
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
    name: 'goodsModal',
    onFieldsChange(props, changedFields) {
        props.onChange(changedFields);
    }
})(GoodModal)