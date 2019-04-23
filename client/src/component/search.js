import React,{Component} from 'react';
import { Form, Icon, Input, Button } from 'antd';
const FormItem = Form.Item;

class SearchForm extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            userName:'hui',
            password:'1111'
        }
    }

    componentDidMount() {
        this.props.form.validateFields();
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
    }

    render() {
        const { userName,password } = this.state;
        const { getFieldDecorator} = this.props.form;

        return (
            <Form layout="inline" onSubmit={this.handleSubmit}>
                <FormItem>
                    {getFieldDecorator('userName', {
                        rules: [{ required: false, message: 'Please input your username!' }],
                    })(
                        <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Username" />
                    )}
                </FormItem>
                <FormItem>
                    {getFieldDecorator('password', {
                        rules: [{ required: false, message: 'Please input your Password!' }],
                    })(
                        <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
                    )}
                </FormItem>
                <FormItem>
                    <Button type="primary" style={{marginRight:10}}>查询</Button>
                    <Button type="primary" ghost>重置</Button>
                </FormItem>
            </Form>
        );
    }
}

export default Form.create()(SearchForm);