import React,{Component} from 'react';
import { Input, Button } from 'antd';

class SearchForm extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            org_code:'M2019061406340968'
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
        const { org_code } = this.state;

        return (
            <div className="ql-search-div">
                <div>
                    <label className="label-red">商铺编码</label>
                    <Input
                        style={{width:150}}
                        placeholder="请输入商铺编码"
                        value={org_code}
                        onChange={(e)=>this.setState({org_code:e.target.value})}
                    />
                </div>
                <Button type="primary" onClick={this.onSearch}>查询</Button>
                <Button type="primary" ghost onClick={this.onReset}>重置</Button>
            </div>
        );
    }
}

export default SearchForm;