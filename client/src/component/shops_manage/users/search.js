import React from 'react';
import { Input, Button,Select } from 'antd';

class SearchForm extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            org_code: '',
            role_type:['管理员','普通员工']
        }
    }

    onSearch = ()=>{
        this.props.onSearch(this.state);
    }

    onReset = ()=>{
        this.setState({
            org_code:''
        })
    }

    render() {
        const { org_code,role_type } = this.state;

        return (
            <div className="ql-search-div">
                <div>
                    <label className="label-red">商铺编码</label>
                    <Input
                        style={{width:150}}
                        placeholder="请输入"
                        value={org_code}
                        onChange={(e)=>this.setState({org_code:e.target.value})}
                    />
                </div>

                <div>
                    <label className="label-red">角色类型</label>
                    <Select>
                        {
                            role_type.map((item=>{
                                return <Option key={item}>{item}</Option>
                            }))
                        }
                    </Select>
                </div>

                <Button type="primary" onClick={this.onSearch}>查询</Button>
                <Button type="primary" ghost onClick={this.onReset}>重置</Button>
            </div>
        );
    }
}

export default SearchForm;