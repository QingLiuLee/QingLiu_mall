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

    // 售货类型
    changeSaleType = () =>{

    }

    // 商铺图片
    changeImgList = () =>{

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
                    </Form>
                </div>
            </div>
        )
    }
}
export default Form.create({ name: 'addShop' })(CategoryModal)